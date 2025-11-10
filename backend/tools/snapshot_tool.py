from playwright.async_api import BrowserContext
from crewai.tools import tool
from typing import Dict
import asyncio
from helper.perception import Perception
from helper.async_utils import create_async_to_sync_decorator
from helper.page_helper import get_current_page


def create_snapshot_tool(context: BrowserContext, loop: asyncio.AbstractEventLoop):
    """Factory function to create capture_ui_snapshot_tool with context bound."""
    
    perception = Perception()
    
    # Create the async_to_sync decorator bound to this event loop
    async_to_sync = create_async_to_sync_decorator(loop)

    @tool("capture_ui_snapshot_tool")
    def capture_ui_snapshot_tool() -> Dict:
        """
        Extract and analyze the UI structure and interactive elements of the current page.
        IMPORTANT: This tool always captures a fresh snapshot and never returns cached results.
        
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
                page = await get_current_page(context)
                await page.wait_for_load_state("domcontentloaded")
                await page.wait_for_timeout(600)
                snapshot = await perception.extract_ui_snapshot(page)
                
                return snapshot
            except Exception as e:
                error_msg = f"Capture UI snapshot failed: {type(e).__name__} - {e}"
                return error_msg
        return _capture()
    
    return capture_ui_snapshot_tool

