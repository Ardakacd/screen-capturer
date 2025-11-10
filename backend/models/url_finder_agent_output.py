from pydantic import BaseModel, Field

class URLFinderOutput(BaseModel):
    confirm_navigation_text: str = Field(..., description="A short string confirming the navigation to the verified URL.")