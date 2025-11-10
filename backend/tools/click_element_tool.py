from playwright.async_api import BrowserContext
from crewai.tools import tool
import asyncio
from helper.take_screenshot import take_screenshot
from helper.async_utils import create_async_to_sync_decorator
from helper.page_helper import get_current_page


def create_click_element_tool(context: BrowserContext, id_number: str, loop: asyncio.AbstractEventLoop):
    """Factory function to create click_element_and_take_screenshot_tool with context and id_number bound."""
    
    # Create the async_to_sync decorator bound to this event loop
    async_to_sync = create_async_to_sync_decorator(loop)

    @tool("click_element_and_take_screenshot_tool")
    def click_element_and_take_screenshot_tool(
        selector: str, 
        bbox_x: float, 
        bbox_y: float, 
        bbox_width: float, 
        bbox_height: float
    ):
        """
        Click an element on the web page using a Playwright selector and take a screenshot of the element.
        
        Args:
            selector (str): A CSS selector, text selector, or other Playwright-compatible selector.
                           Do not make up any selector, use the selector that is already in the snapshot.
                           Be as specific as possible.
                           Examples: "[aria-label='Share'], div[role='button']:has-text('Share'), div[class*='Share']"
            bbox_x (float): The x coordinate of the bounding box of the element.
            bbox_y (float): The y coordinate of the bounding box of the element.
            bbox_width (float): The width of the bounding box of the element.
            bbox_height (float): The height of the bounding box of the element.
        
        Returns:
            str: Success message with the selector clicked and the screenshot path, or error message if the click fails.
        
        Usage: Use this when you need to interact with buttons, links, or clickable elements.
        """
        @async_to_sync
        async def _click():
            try:
                                
                page = await get_current_page(context)
                element = page.locator(selector)
                count = await element.count()


                if count == 0:
                    return "No element found please look at capture_ui_snapshot_tool() and try again"

                path = await take_screenshot(
                    page, id_number, tag="before_click", 
                    bbox_x=bbox_x, bbox_y=bbox_y,
                    bbox_width=bbox_width, bbox_height=bbox_height
                )
                
                # If there is only one element, click it
                if count == 1:
                    await element.first.click(timeout=3000)
                    return f"Clicked element and screenshot saved to path: {path}"

                # If there is more than one element, click the center of the bounding box
                click_x = bbox_x + bbox_width / 2
                click_y = bbox_y + bbox_height / 2

                # Scroll target into view 
                await page.evaluate(
                    """({x, y}) => {
                        window.scrollTo({
                            top: Math.max(y - window.innerHeight / 2, 0),
                            left: Math.max(x - window.innerWidth / 2, 0),
                            behavior: 'instant'
                        });
                    }""",
                    {"x": click_x, "y": click_y}  
                )
                await page.wait_for_timeout(150) 

                await page.mouse.click(click_x, click_y)
                return f"Clicked element and screenshot saved to path: {path}"

            except Exception as e:
                error_msg = f"Click failed: {type(e).__name__} - {e}"
                print(error_msg)
                return error_msg
        return _click()
    
    return click_element_and_take_screenshot_tool

