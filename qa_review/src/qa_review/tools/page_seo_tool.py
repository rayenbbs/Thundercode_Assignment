import requests
import os
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

class PageSEOToolInput(BaseModel):
    """Input schema for PageSEOTool."""
    url: str = Field(..., description="The URL of the website to analyze.")

class PageSEOTool(BaseTool):
    name: str = "Page SEO Tool"
    description: str = (
        "Fetches Page SEO data for a given URL. Useful for analyzing web page SEO."
    )
    args_schema: Type[BaseModel] = PageSEOToolInput

    def _run(self,url:str) -> str:
        """Run method for the Page SEO tool."""

        if not url:
            return "No URL provided to analyze."
        
        base_api_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
        try:
            # construct API call URL
            api_url = f"{base_api_url}?url={url}&category=seo&key={os.getenv("PAGE_INSIGHTS_API_KEY")}"
            
            # make the GET request
            response = requests.get(api_url)
            response.raise_for_status()  # raise an error for HTTP issues
            json_data=response.json()
            #filtering the data
            json_data=json_data["lighthouseResult"]["audits"]
           
            # return JSON as a formatted string
            return json_data
        
        except requests.exceptions.RequestException as e:
            return f"An error occurred while fetching PageSpeed data: {e}"
