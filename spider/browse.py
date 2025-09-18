import asyncio, re
from collections.abc import Awaitable, Iterable
from enum import auto, Enum
from typing import Any, AsyncGenerator, Coroutine, Dict, Generator, List, Optional, Union, Tuple
from urllib.parse import urlparse
from playwright.async_api import Browser, BrowserContext, BrowserType, Locator, Page, \
Playwright, Response

class BrowserChoice(Enum):
    chromium = auto()
    firefox = auto()
    webkit = auto()


class DataType(Enum):
    single = auto()
    multiple = auto()

async def create_browser(
        choice: BrowserChoice, 
        playwright: Playwright,
        headless: bool = True
        ) -> Browser:
    """
    Creates a browser instance

    :param BrowserChoice choice: The preferred browser
    :param Playwright playwright:
    :param bool headless: 
    :returns: A browser instance
    :rtype Browser

    >>>  async with async_playwright() as playwright:
    >>>     browser = await create_browser(BrowserChoice.webkit, playwright, False)
    """
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

    >>> page = await create_page(browser, True)

    :param Browser browser:
    :param bool incognito:
    :returns:
    :rtype Awaitable[Page]:
    """
    if incognito:
        context: BrowserContext = await browser.new_context()
        return await context.new_page()
    else:
        return await browser.new_page()
 
async def visit_page(*, uri: str, page: Page) -> Awaitable[Optional[Response]]:
    """
    A light-weight fetch that returns Response object 
    and tries not to open unecessary files

    >>> response = await visit(uri='www.example.com', page=page)

    :param str uri:
    :param Page page:
    :returns:
    :rtype Awaitable[Optional[Response]]:
    """
    result: Optional[Response] = await page.goto(url=uri, wait_until='domcontentloaded')
    await asyncio.sleep(0)
    return result

# async def visit(url: str, browser: BrowserChoice = BrowserChoice.chromium):
#     """
#     """
#     match browser:
#         case BrowserChoice.chromium:
#             psss
#         case BrowserChoice.firefox:
#             pass
#         case BrowserChoice.webkit:
#             pass
#         case _ :
#             pass

async def search(page: Page, text: str) -> Awaitable[List[Locator]]:
    """
    Automates the browser the send the query passed to it

    >>> query = 'isaac newton'
    >>> search = aawait search(page, query)

    :param Page page:
    :param str text:
    :returns:
    :rtype Awaitable[List[Locator]]:
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

async def nav_url(link: Locator) -> Optional[Tuple[int, str]]:
    """
    Returns a tuple containing the page number and the page url of the 
    navigation link locator. This tuple represents each result page other than the 
    current result page.

    >>> result_page = await nav_url(locator)
    >>> (output) --> (2, '/result-page/2/')

    :param Locator link: A navigation link element represented by a locator
    :returns: A tuple containing the page number found in the element and the href value of the element
    :rtype: Optional[Tuple[int, str]]
    :raises playwright._impl._errors.TimeoutError: if the locator passed as an argument cannot locate the link's href attribute
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
    Locates the page's breadcrumbs and returns a list of Locators from it

    :param Page page:
    :returns:
    :rtype Coroutine[Any, Any, Optional[List[Locator]]]:
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


async def parse_each(gen: Generator[Tuple[str, Locator], None, None]) -> AsyncGenerator[Tuple[str, List, None]]:
    """
    Generic parser simlar to parse_group
    """
    async for key, node in gen():
        contents: List = await node.all_inner_texts() or []
        yield key, contents

async def parse_group(node: Locator) -> AsyncGenerator[Tuple[str, List[str]], None]:
    """

    :param Locator node:
    :returns:
    :rtype AsyncGenerator[Tuple[str, List[str]], None]:
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

    :param List[Locator] nodes:
    :returns:
    :rtype Coroutine[Any, Any, List[Dict[str, str]]]:
    """
    result = [{k: v async for k, v in parse_group(node)} for node in nodes]
    await asyncio.sleep(0)
    return result


