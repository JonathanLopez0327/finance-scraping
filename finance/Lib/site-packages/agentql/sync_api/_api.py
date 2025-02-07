"""
This module is an entrypoint to AgentQL service
"""

from playwright.sync_api import Page as _Page

from agentql.ext.playwright.sync_api import Page
from agentql.ext.playwright.sync_api._utils_sync import handle_page_crash


def wrap(page: _Page) -> Page:
    """
    Casts a Playwright Sync `Page` object to an AgentQL `Page` type to get access to the AgentQL's querying API.
    See `agentql.ext.playwright.sync_api.Page` for API details.
    """
    page.on("crash", handle_page_crash)
    return Page.create(page)
