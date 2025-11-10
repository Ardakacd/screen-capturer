from playwright.async_api import BrowserContext
from crewai.tools import tool
import asyncio
from helper.take_screenshot import take_screenshot
from helper.async_utils import create_async_to_sync_decorator
from helper.page_helper import get_current_page


def create_navigate_tool(context: BrowserContext, id_number: str, loop: asyncio.AbstractEventLoop):
    """Factory function to create navigate_page_and_take_screenshot_tool with context and id_number bound."""
    
    # Create the async_to_sync decorator bound to this event loop
    async_to_sync = create_async_to_sync_decorator(loop)

    @tool("navigate_page_and_take_screenshot_tool")
    def navigate_page_and_take_screenshot_tool(url: str):
        """
        Navigate the browser to a specified URL and take a screenshot of the page.
        
        Args:
            url (str): The full URL to navigate to. Must include the protocol (http:// or https://).
                      Example: 'https://www.example.com'
        
        Returns:
            str: Success message with the URL and the screenshot path, or error message if navigation fails.
        
        Usage: Use this to load new pages or navigate to different URLs. The page will wait 
               until DOM content is loaded before considering the navigation complete.
        """
        @async_to_sync
        async def _navigate():
            try:
                page = await get_current_page(context)
                await page.goto(url, wait_until="domcontentloaded", timeout=30000)
                # Wait for dynamic content to settle
                await page.wait_for_timeout(600)
                path = await take_screenshot(page, id_number, tag="after_navigate")
                return f"Navigated to {url} and screenshot saved to path: {path}"
            except Exception as e:
                return f"Navigation failed: {type(e).__name__} - {e}"
        return _navigate()
    
    return navigate_page_and_take_screenshot_tool

