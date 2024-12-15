import requests
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

class PageHTTPHeaderToolInput(BaseModel):
    """Input schema for PageHTTPHeaderTool."""
    url: str = Field(..., description="The URL of the website to get HTTP Header from.")

class PageHTTPHeaderTool(BaseTool):
    name: str = "Page HTTP Header extractor Tool"
    description: str = (
        "Fetches Page  HTTP Header  for a given URL. Useful for analyzing web page  HTTP Header ."
    )
    args_schema: Type[BaseModel] = PageHTTPHeaderToolInput
    def _run(self,url:str) -> str:
        """Run method for the Page HTTP Header tool."""

        if not url:
            return "No URL provided to analyze."
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.headers
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
