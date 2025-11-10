"""
Tools package for browser automation.

This package contains individual tool modules that can be used with CrewAI agents.
Each tool is created using a factory pattern to inject dependencies like page and id_number.
"""

from .click_element_tool import create_click_element_tool
from .fill_input_tool import create_fill_input_tool
from .navigate_tool import create_navigate_tool
from .snapshot_tool import create_snapshot_tool
from .web_search_tool import create_web_search_tool

__all__ = [
    'create_click_element_tool',
    'create_fill_input_tool',
    'create_navigate_tool',
    'create_snapshot_tool',
    'create_web_search_tool',
]

