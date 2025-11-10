from playwright.async_api import BrowserContext
from crewai.tools import tool
import asyncio
from helper.take_screenshot import take_screenshot
from helper.async_utils import create_async_to_sync_decorator
from helper.page_helper import get_current_page


def create_fill_input_tool(context: BrowserContext, id_number: str, loop: asyncio.AbstractEventLoop):
    """Factory function to create fill_input_and_take_screenshot_tool with context and id_number bound."""
    
    # Create the async_to_sync decorator bound to this event loop
    async_to_sync = create_async_to_sync_decorator(loop)

    @tool("fill_input_and_take_screenshot_tool")
    def fill_input_and_take_screenshot_tool(
        selector: str, 
        bbox_x: float, 
        bbox_y: float, 
        bbox_width: float, 
        bbox_height: float, 
        value: str
    ):
        """
        Fill an input field with the specified text value and take a screenshot of the element.
        
        Args:
            selector (str): A CSS selector, text selector, or other Playwright-compatible selector.
                           Do not make up any selector, use the selector that is already in the snapshot.
                           Be as specific as possible for selector. Always look for whether there is a clash for the selector.
                           Examples: "input[placeholder='Add emails'], input[class*='email']"
            bbox_x (float): The x coordinate of the bounding box of the element.
            bbox_y (float): The y coordinate of the bounding box of the element.
            bbox_width (float): The width of the bounding box of the element.
            bbox_height (float): The height of the bounding box of the element.
            value (str): The text value to fill into the input field.
                Example: "arda@example.com"
        Returns:
            str: Success message with the selector and value and the screenshot path, or error message if filling fails.
        
        Usage: Use this to enter text into input fields, textareas, or contenteditable elements.
        """
        @async_to_sync
        async def _fill():
            try:
                page = await get_current_page(context)
                await page.fill(selector, value, timeout=3000)
                path = await take_screenshot(
                    page, id_number, tag="after_fill", 
                    bbox_x=bbox_x, bbox_y=bbox_y,
                    bbox_width=bbox_width, bbox_height=bbox_height
                )
                return f"Input filled and screenshot saved to path: {path}"
            except Exception as e:
                return f"Input fill failed: {type(e).__name__} - {e}"
        return _fill()
    
    return fill_input_and_take_screenshot_tool

