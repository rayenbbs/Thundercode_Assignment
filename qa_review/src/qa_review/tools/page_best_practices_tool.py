import os
import requests
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

class PageBestPracticesToolInput(BaseModel):
    """Input schema for PageBestPracticesTool."""
    url: str = Field(..., description="The URL of the website to analyze.")

class PageBestPracticesTool(BaseTool):
    name: str = "Page best-practices Tool"
    description: str = (
        "Fetches Page best-practices data for a given URL. Useful for analyzing web page best-practices."
    )
    args_schema: Type[BaseModel] = PageBestPracticesToolInput

    def _run(self,url:str) -> str:
        """Run method for the Page best-practices tool."""

        if not url:
            return "No URL provided to analyze."
        
        base_api_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
        try:
            # Construct API call URL
            api_url = f"{base_api_url}?url={url}&category=best-practices&key={os.getenv("PAGE_INSIGHTS_API_KEY")}"
            
            # Make the GET request
            response = requests.get(api_url)
            response.raise_for_status()  # Raise an error for HTTP issues
            json_data=response.json()
            
            json_data=json_data["lighthouseResult"]["audits"]
            #lighthouseResult_audits_keystokeep_reduced = {"is-on-https","errors-in-console", } 
            #json_data= {
            #    key: value
            #    for key, value in json_data.items()
            #    if key in lighthouseResult_audits_keystokeep_reduced
            #}
            # Return JSON as a formatted string
            return json_data
        
        except requests.exceptions.RequestException as e:
            return f"An error occurred while fetching PageBestPractices data: {e}"
