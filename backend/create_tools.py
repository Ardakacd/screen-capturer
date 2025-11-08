from helper.perception import Perception
from playwright.async_api import Page
from crewai.tools import tool
from typing import Dict
import asyncio
from datetime import datetime
import os
from functools import wraps
import json
from helper.take_screenshot import take_screenshot

def create_tools(page: Page, id_number: str):
    """
    Create synchronous tools that wrap async Playwright operations.
    These tools can be safely called from CrewAI's thread-based execution model.
    """
    
    # Get the event loop that Playwright is running on
    loop = asyncio.get_event_loop()
    
    def async_to_sync(func):
        """Decorator to convert async functions to sync by running them on the main loop."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Schedule the coroutine on the main event loop and wait for result
            future = asyncio.run_coroutine_threadsafe(func(*args, **kwargs), loop)
            return future.result(timeout=30) 
        return wrapper

    perception = Perception()

    @tool("click_element_and_take_screenshot_tool")
    def click_element_and_take_screenshot_tool(selector: str, bbox_x: float, bbox_y: float, bbox_width: float, bbox_height: float):
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
                element = page.locator(selector)
                count = await element.count()

                print('Here is the count: ', count)

                if count == 0:
                    return "No element found please look at capture_ui_snapshot_tool() and try again"

                path = await take_screenshot(page, id_number, tag="before_click", bbox_x=bbox_x, bbox_y=bbox_y,
                                   bbox_width=bbox_width, bbox_height=bbox_height)
                
                if count == 1:
                    await element.first.click(timeout=3000)
                    return f"Clicked element and screenshot saved to path: {path}"


                # 📍 Fallback: Click using bbox center
                click_x = bbox_x + bbox_width / 2
                click_y = bbox_y + bbox_height / 2

                 # Scroll target into view (center it roughly)
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

    
    @tool("fill_input_and_take_screenshot_tool")
    def fill_input_and_take_screenshot_tool(selector: str, bbox_x: float, bbox_y: float, bbox_width: float, bbox_height: float, value: str):
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
                await page.fill(selector, value, timeout=3000)
                path = await take_screenshot(page, id_number, tag="after_fill", bbox_x=bbox_x, bbox_y=bbox_y,
                                   bbox_width=bbox_width, bbox_height=bbox_height)
                return f"Input filled and screenshot saved to path: {path}"
            except Exception as e:
                return f"Input fill failed: {type(e).__name__} - {e}"
        return _fill()

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
                await page.goto(url, wait_until="domcontentloaded", timeout=10000)
                path = await take_screenshot(page, id_number, tag="after_navigate")

                return f"Navigated to {url} and screenshot saved to path: {path}"
            except Exception as e:
                return f"Navigation failed: {type(e).__name__} - {e}"
        return _navigate()

    
    

    @tool("capture_ui_snapshot_tool")
    def capture_ui_snapshot_tool() -> Dict:
        """
        Extract and analyze the UI structure and interactive elements of the current page.
        
        Returns:
            Dict: A structured snapshot containing information about interactive elements,
                  their selectors, labels, types, and hierarchy. Useful for understanding
                  what actions are available on the current page.
        
        Usage: Use this to get a comprehensive understanding of the page structure before
               deciding which elements to interact with. This is particularly useful when
               you need to identify available buttons, inputs, links, or other interactive
               elements without relying on visual inspection.
        """
        @async_to_sync
        async def _capture():
            try:
                await page.wait_for_timeout(600)
                snapshot = await perception.extract_ui_snapshot(page)
                
                # Write snapshot to file with separator for debugging
                os.makedirs("snapshots", exist_ok=True)
                snapshot_file = "snapshots/ui_snapshots_log.txt"
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                with open(snapshot_file, "a", encoding="utf-8") as f:
                    f.write(f"\n{'='*80}\n")
                    f.write(f"SNAPSHOT CAPTURED AT: {timestamp}\n")
                    f.write(f"URL: {snapshot.get('url', 'N/A')}\n")
                    f.write(f"Title: {snapshot.get('title', 'N/A')}\n")
                    f.write(f"{'='*80}\n\n")
                    f.write(json.dumps(snapshot, indent=2, ensure_ascii=False))
                    f.write(f"\n\n{'-'*80}\n")
                
                print(f"Snapshot saved to {snapshot_file}")
                return snapshot
            except Exception as e:
                error_msg = f"Capture UI snapshot failed: {type(e).__name__} - {e}"
                print(error_msg)
                return error_msg
        return _capture()

    return [click_element_and_take_screenshot_tool, fill_input_and_take_screenshot_tool, navigate_page_and_take_screenshot_tool, capture_ui_snapshot_tool]