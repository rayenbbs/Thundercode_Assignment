import requests
import os
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

class PagePerformanceToolInput(BaseModel):
    """Input schema for PagePerformanceTool."""
    url: str = Field(..., description="The URL of the website to analyze.")

class PagePerformanceTool(BaseTool):
    name: str = "Page Performance Tool"
    description: str = (
        "Fetches Page Performance data for a given URL. Useful for analyzing web page performance."
    )
    args_schema: Type[BaseModel] = PagePerformanceToolInput

    def _run(self,url:str) -> str:
        """Run method for the Page Performance tool."""

        if not url:
            return "No URL provided to analyze."
        
        base_api_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
        try:
            # construct API call URL
            api_url = f"{base_api_url}?url={url}&category=performance&key={os.getenv("PAGE_INSIGHTS_API_KEY")}"
            
            # make the GET request
            response = requests.get(api_url)
            response.raise_for_status()  # raise an error for HTTP issues
            json_data=response.json()
            
            json_data=json_data["lighthouseResult"]["audits"]
            lighthouseResult_audits_keystokeep = {"server-response-time","duplicated-javascript","lcp-lazy-loaded","diagnostics","metrics","bootup-time","network-server-latency","layout-shifts","first-contentful-paint","legacy-javascript","resource-summary","speed-index","interactive","first-meaningful-paint","first-cpu-idle","estimated-input-latency","largest-contentful-paint-element","largest-contentful-paint"} 
            json_data= {
                key: value
                for key, value in json_data.items()
                if key in lighthouseResult_audits_keystokeep
            }
            
            # return JSON as a formatted string
            return json_data
        
        except requests.exceptions.RequestException as e:
            return f"An error occurred while fetching PageSpeed data: {e}"
