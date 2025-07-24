import asyncio, re
# from collections import OrderedDict
from collections.abc import Awaitable, Iterable
from enum import auto, Enum
from typing import Any, AsyncGenerator, Coroutine, Dict, List, Optional, Union, Tuple
from urllib.parse import urlparse
from playwright.async_api import Browser, BrowserContext, BrowserType, Locator, Page, \
Playwright, Response

class BrowserChoice(Enum):
    chromium = auto()
    firefox = auto()
    webkit = auto()

async def create_browser(
        choice: BrowserChoice, 
        playwright: Playwright,
        headless: bool = True
        ) -> Browser:
    match choice:
        case BrowserChoice.chromium:
            browser = await playwright.chromium.launch()
        case BrowserChoice.firefox:
            browser = await playwright.firefox.launch()
        case BrowserChoice.webkit:
            browser = await playwright.webkit.launch()
    return browser

async def create_page(browser: Browser, incognito: bool = False) -> Awaitable[Page]:
    """
    Helper function for creating a new Page object 
    """
    if incognito:
        context: BrowserContext = await browser.new_context()
        return await context.new_page()
    else:
        return await browser.new_page()
 
async def visit(*, uri: str, page: Page) -> Awaitable[Optional[Response]]:
    """
    A light-weight fetch that returns Response object 
    and tries not to open unecessary files
    """
    result: Optional[Response] = await page.goto(url=uri, wait_until='domcontentloaded')
    await asyncio.sleep(0)
    return result

async def search(page: Page, text: str) -> Awaitable[List[Locator]]:
    """
    Automates the browser the send the query passed to it
    """
    input: Locator = page.locator('#gs_hdr_tsi')
    await input.press_sequentially(text, delay=10)
    # print('Query input: ', text) 
    submit: Locator = page.locator('#gs_hdr_tsb')
    await submit.click()
    # print('Query submitted')
    await page.wait_for_load_state('domcontentloaded')
    result: Locator = page.locator('div.gs_ri')
    result: List[Locator] = await result.all()
    await asyncio.sleep(0)
    return result

async def nav_url(link: Locator) -> Optional[Tuple[ int, str]]:
    """
    It returns a tuple containing the page number and the page url of the 
    navigation link locator
    """
    if await link.count():
        url: str = await link.get_attribute('href')
        content: str = await link.text_content()
        position: int = re.search(r'\d+', content).group(0)
        path: str = url if bool(urlparse(url).netloc) else ''.join([link.page.url, url])
        return position, path
    return None

async def more_results(page: Page) -> Coroutine[Any, Any, Optional[List[Locator]]]:
    """
    """
    await asyncio.sleep(0)
    parent: Locator = page.locator('#gs_n')
    every: Locator = parent.get_by_role('cell')
    if await every.count():
        # marker: Locator = every.locator('.gs_ico_nav_page')
        links: Locator = every.get_by_role('link', name=re.compile(r'\d+'))
        if await links.count():
            # print('links number: ', await links.count())
            # print(links)
            results: List[Locator] = await links.all()
            await asyncio.sleep(0)
            return results
    return []

async def parse_group(node: Locator) -> AsyncGenerator[Tuple[str, List[str]], None]:
    """
    """
    await asyncio.sleep(0)
    link: Locator = node.locator('h3.gs_rt a')
    title: str = await link.all_inner_texts()
    yield 'title', title
    url: str = 'url', await link.get_attribute('href') or ''
    yield 'url', url
    authors: List[str] = await node.locator('div.gs_a').all_inner_texts() or []
    yield 'authors', authors
    summary: List[str] = await node.locator('div.gs_rs').all_inner_texts() or []
    yield 'summary', summary
    citedby: List[str] = await node.get_by_role('link', name='Cited by').all_inner_texts() or []
    yield 'cite-by', citedby

async def parse_groups(nodes: List[Locator]) -> Coroutine[Any, Any, List[ Dict[ str, str]]]:
    """
    A helper coroutine for parsing a list of query results' locators. It uses parse_group
    on each item on the list
    """
    result = [{k: v async for k, v in parse_group(node)} for node in nodes]
    await asyncio.sleep(0)
    return result


