"""
Async utility functions for tools.

This module provides utilities for converting async functions to sync,
enabling async Playwright operations to work with CrewAI's thread-based execution model.
"""

import asyncio
from functools import wraps
from typing import Callable, Any


def create_async_to_sync_decorator(loop: asyncio.AbstractEventLoop, timeout: int = 30) -> Callable:
    """
    Create an async_to_sync decorator bound to a specific event loop.
    
    This decorator allows async functions to be called synchronously by scheduling
    them on the main event loop and waiting for the result. This is necessary because
    CrewAI runs tools in a separate thread using asyncio.to_thread().
    
    Args:
        loop: The event loop where async operations should run (usually the Playwright loop)
        timeout: Maximum seconds to wait for the operation to complete (default: 30)
        
    Returns:
        A decorator function that converts async functions to sync
        
    """
    def async_to_sync(func: Callable) -> Callable:
        """
        Decorator to convert an async function to sync by running it on the main loop.
        
        Args:
            func: The async function to wrap
            
        Returns:
            A synchronous wrapper function
        """
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Schedule the coroutine on the main event loop and wait for result
            future = asyncio.run_coroutine_threadsafe(func(*args, **kwargs), loop)
            return future.result(timeout=timeout)
        return wrapper
    
    return async_to_sync

