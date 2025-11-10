"""
Main tool factory that coordinates the creation of all tools.
Each tool is defined in a separate file in the tools/ directory.
"""

from playwright.async_api import BrowserContext
import asyncio
from tools.click_element_tool import create_click_element_tool
from tools.fill_input_tool import create_fill_input_tool
from tools.navigate_tool import create_navigate_tool
from tools.snapshot_tool import create_snapshot_tool
from tools.web_search_tool import create_web_search_tool


def create_tools(context: BrowserContext, id_number: str):
    """
    Create all tools with browser context and id_number dependencies injected.
    
    This function coordinates the creation of all tools by:
    1. Getting the current event loop
    2. Calling each tool factory with the required dependencies
    3. Returning a list of configured tools ready for use by CrewAI
    
    Args:
        context: Playwright BrowserContext for dynamic page management
        id_number: Unique identifier for this task (used in screenshot paths)
        
    Returns:
        List of configured CrewAI tools
    """
    # Get the event loop that Playwright is running on
    loop = asyncio.get_event_loop()
    
    # Create each tool using its factory function
    click_element_and_take_screenshot_tool = create_click_element_tool(context, id_number, loop)
    fill_input_and_take_screenshot_tool = create_fill_input_tool(context, id_number, loop)
    navigate_page_and_take_screenshot_tool = create_navigate_tool(context, id_number, loop)
    capture_ui_snapshot_tool = create_snapshot_tool(context, loop)
    
    # Create API-based tools (no browser dependencies needed)
    web_search_tool = create_web_search_tool()
    
    return [
        click_element_and_take_screenshot_tool,
        fill_input_and_take_screenshot_tool,
        navigate_page_and_take_screenshot_tool,
        capture_ui_snapshot_tool,
        web_search_tool,
    ]