import asyncio, inspect, re
from collections import OrderedDict
from collections.abc import Awaitable, Iterable
from enum import auto, Enum
from typing import Any, AsyncGenerator, Coroutine, Dict, List, Union, Tuple
from playwright.async_api import async_playwright, Browser, \
    BrowserContext, BrowserType, Locator, Page, Playwright, Response

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
 
async def visit(*, uri: str, page: Page) -> Awaitable[Union[Response, None]]:
    """
    A light-weight fetch that returns Response object 
    and tries not to open unecessary files
    """
    # pattern: re.Pattern[AnyStr] = re.compile('**/*.{png,jpg,jpeg}')
    # # don't load unneccesary files
    # await page.route(pattern, lambda route: route.abort())
    return await page.goto(url=uri, wait_until='domcontentloaded')

async def search(page: Page, text: str) -> Awaitable[List[Locator]]:
    """
    Automates the browser the send the query passed to it
    """
    #TODO: needs work
    input: Locator = page.locator('#gs_hdr_tsi')
    await input.press_sequentially(text, delay=10)
    print('Query input: ', text) 
    submit: Locator = page.locator('#gs_hdr_tsb')
    await submit.click()
    print('Query submitted')
    # result_selector: str = 'div.gs_ri'
    result: Locator = page.locator('div.gs_ri')
    # await result_page.wait_for(state='attached', timeout=50000)
    # await page.wait_for_selector(result_selector, timeout=50000)
    # await expect(result_page).to_be_attached()
    return await result.all()

async def parse_group(node: Locator) -> AsyncGenerator[Tuple[str, List[str]], None]:
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
    return [{k: v async for k, v in parse_group(node)} for node in nodes]



async def parse_result(items: List[Locator]) -> Awaitable[ List[ List[ Tuple[str, str]]]]:
    """
    Parse the HTML node passed to it and returns a dict 
    """
    seq: List[ List[ Tuple[ str, str]]] = []
    for result in items:
        group: List[ Tuple[ str, str]] = []
        await asyncio.sleep(0)
        print('title: ', await result.all_inner_texts())
        # content: str = await result.filter()
        # title doesn't work
        tgroup: Locator = result.locator('h3.gs_rt a')
        title: Tuple[str, str] = 'title', await tgroup.text_content() or 'No title'
        group.append(title)
        print('title written')
        # author doesn't work
        author: Tuple[str, str] = 'author', await result.locator('div.gs_a').all_inner_texts() or []
        group.append(author)
        # abstract works
        abstract = 'abstract', await result.locator('div.gs_rs').all_inner_texts() or []
        group.append(abstract)
        # citation works
        citation = 'citations', await result.get_by_role('link', name='Cited by').all_inner_texts() or []
        group.append(citation)
        # # year doesn't work
        # year = 'year', await result.locator('.gs_age').all_inner_texts() or ''
        # group.append(year)
        # url works
        # url = 'url', await result.locator('h3.gs_rt a').get_attribute('href') or ''
        url = 'url', await tgroup.get_attribute('href') or ''
        group.append(url)
        seq.append(group)
    return seq

def display(item: any, filename: str) -> None:
    with open(filename, 'a') as f:
        print(item, file=f)

# async def main() -> None:
#     async with async_playwright() as app:
#         browser: Browser = await create_browser(BrowserChoice.chromium, app)
#         assert browser is not None, 'browser object is None'
#         uri: str = 'https://scholar.google.com'
#         page: Page = await create_page(browser)
#         assert page is not None, 'page object is None'
#         res: Response = await visit(uri=uri, page=page) 
#         if res is None:
#             # error message
#             print('Site visit failed')
#             return
#         else:
#             print("Success, status: ", res.status)
#         # make sure the page loads fully
#         await page.wait_for_load_state('domcontentloaded')
#         print(await res.headers_array())
#         query: str = 'hpcc cuny'
#         results: List[Locator] = await search(page, query)
#         print('Results obtained')
#         assert len(results) > 0, 'Search returned no locators'
#         # output = await parse_result(results)
#         output = await parse_groups(results)
#         print('/n/n/n')
#         print(output)
#         # items = await results.all()
#         # print('there are ', len(items), ' items')
#         # content:List[str] = await items[0].all_inner_texts()
#         # print('inner-text count: ', len(content))
#         # print(content[:3])
#         # content: List[Dict[str, str]] = await parse_groups(results)
#         # # testing
#         # print('type: ', type(results))
#         # print('size: ', len(results))
#         # print(results)
#         # content = await parse_group(results[0])
#         # print('results parsed')
#         # print(content)
#         # clean up
#         await browser.close()
#         # display(content, 'output.txt')
#         print('task completed')

# if __name__ == '__main__': 
#     asyncio.run(main())