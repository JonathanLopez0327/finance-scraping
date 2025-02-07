"""
This module is an entrypoint to AgentQL service
"""

from typing import Any, Coroutine, Union

from playwright.async_api import Page as _Page

from agentql.ext.playwright.async_api import Page
from agentql.ext.playwright.async_api._utils_async import handle_page_crash


async def wrap_async(page: Union[Coroutine[Any, Any, _Page], _Page]) -> Page:
    """
    Casts a Playwright Async `Page` object to an AgentQL `Page` type to get access to the AgentQL's querying API.
    See `agentql.ext.playwright.async_api.Page` for API details.
    """
    if isinstance(page, Coroutine):
        page = await page  # type: ignore

    page.on("crash", handle_page_crash)

    return await Page.create(page)
