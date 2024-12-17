import requests
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field


class PageHTMLToolInput(BaseModel):
    """Input schema for PageHTMLTool."""
    url: str = Field(..., description="The URL of the website to get html from.")

class PageHTMLTool(BaseTool):
    name: str = "Page HTML extractor Tool"
    description: str = (
        "Fetches Page HTML for a given URL. Useful for analyzing web page HTML."
    )
    args_schema: Type[BaseModel] = PageHTMLToolInput

    def _run(self,url:str) -> str:
        """Run method for the Page HTML tool."""

        if not url:
            return "No URL provided to analyze."
        
        try:
            # send a GET request to the website
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            # return the HTML content of the website
            return response.text
        except requests.exceptions.MissingSchema:
            return "Invalid URL format. Make sure the URL starts with http:// or https://"
        except requests.exceptions.ConnectionError:
            return "Failed to connect to the website. Please check the URL or your internet connection."
        except requests.exceptions.Timeout:
            return "The request timed out. Try again later."
        except requests.exceptions.HTTPError as e:
            return f"HTTP error occurred: {e}"
        except Exception as e:
            return f"An unexpected error occurred: {e}"
