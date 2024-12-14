import os
import requests
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
from dotenv import load_dotenv


load_dotenv()

class PageAccessibilityToolInput(BaseModel):
    """Input schema for PageAccessibilityTool."""
    url: str = Field(..., description="The URL of the website to analyze.")

class PageAccessibilityTool(BaseTool):
    name: str = "Page Accessibility Tool"
    description: str = (
        "Fetches Page Accessibility data for a given URL. Useful for analyzing web page accessibility."
    )
    args_schema: Type[BaseModel] = PageAccessibilityToolInput

    def _run(self,url:str) -> str:
        """Run method for the Page Accessibility tool."""

        if not url:
            return "No URL provided to analyze."
        
        base_api_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
        try:
            # Construct API call URL
            api_url = f"{base_api_url}?url={url}&category=accessibility&key={os.getenv("PAGE_INSIGHTS_API_KEY")}"
            
            # Make the GET request
            response = requests.get(api_url)
            response.raise_for_status()  # Raise an error for HTTP issues
            json_data=response.json()
            
            json_data=json_data["lighthouseResult"]["audits"]
            lighthouseResult_audits_keystokeep_reduced = {"aria-roles","tabindex", "th-has-data-cells","aria-valid-attr","target-size","form-field-multiple-labels","input-image-alt","meta-refresh","managed-focus","image-alt","interactive-element-affordance","skip-link","logical-tab-order","html-xml-lang-mismatch","empty-heading","meta-viewport","color-contrast","focus-traps","html-has-lang","visual-order-follows-dom","bypass","offscreen-content-hidden"} 

            json_data= {
                key: value
                for key, value in json_data.items()
                if key in lighthouseResult_audits_keystokeep_reduced
            }
            # Return JSON as a formatted string
            return json_data
        
        except requests.exceptions.RequestException as e:
            return f"An error occurred while fetching PageAccesibility data: {e}"
