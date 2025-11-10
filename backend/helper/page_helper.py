"""
Page Helper - Manages browser context and page retrieval.

This module provides utilities for working with Playwright browser contexts
and handling multiple pages/tabs dynamically.
"""

from playwright.async_api import Page, BrowserContext


async def get_current_page(context: BrowserContext) -> Page:
    """
    Get the most recently opened or active page from the browser context.
    
    This is crucial when tools might open new tabs/windows, as we always want
    to work with the latest active page rather than a stale reference.
    
    Args:
        context: Playwright BrowserContext containing all pages
        
    Returns:
        Page: The most recently opened page (last in the list)
        
    Raises:
        RuntimeError: If no pages are found in the context
    """
    pages = context.pages
    print(f"Pages: {pages}")
    if not pages:
        raise RuntimeError("No active page found in browser context.")
    return pages[-1]  # Return the last opened tab

