import asyncio, re
from collections.abc import Awaitable, Iterable
from enum import auto, Enum
from typing import AnyStr, Coroutine, Dict, List, Union, Tuple
from playwright.async_api import async_playwright, Browser, \
    BrowserContext, BrowserType, expect, Locator, Page, Playwright, Response

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
    result_selector: str = 'div.gs_ri'
    result: Locator = page.locator('div.gs_ri')
    # await result_page.wait_for(state='attached', timeout=50000)
    # await page.wait_for_selector(result_selector, timeout=50000)
    # await expect(result_page).to_be_attached()
    return await result.all()


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
        title: Tuple[str, str] = 'title', await result.filter(has=result.locator('div.gs_rt')).all_inner_texts() or 'No title'
        seq.append(title)
        print('title written')
        author: Tuple[str, str] = 'author', await result.filter(has=result.locator('div.ge_a')).all_inner_texts() or 'No author'
        seq.append(author)
        abstract = 'abstract', await result.locator('div.gs_rs').all_inner_texts() or 'No abstract'
        seq.append(abstract)
        # values['citations'] = await result.get_by_role('link', name='Cited by').text_content() or ''
        # values['year'] = await result.locator('.gs_age').text_content() or ''
        # values['url'] = await result.locator('h3.gs_rt a').get_attribute('href') or ''
        seq.append(group)
    return seq

def display(item: any, filename: str) -> None:
    with open(filename, 'a') as f:
        print(item, file=f)

async def main() -> None:
    async with async_playwright() as app:
        browser: Browser = await create_browser(BrowserChoice.chromium, app)
        assert browser is not None, 'browser object is None'
        uri: str = 'https://scholar.google.com'
        page: Page = await create_page(browser)
        assert page is not None, 'page object is None'
        res: Response = await visit(uri=uri, page=page) 
        if res is None:
            # error message
            print('Site visit failed')
            return
        else:
            print("Success, status: ", res.status)
        query: str = 'hpcc cuny'
        results: List[Locator] = await search(page, query)
        print('Results obtained')
        # items = await results.all()
        # print('there are ', len(items), ' items')
        # content:List[str] = await items[0].all_inner_texts()
        # print('inner-text count: ', len(content))
        # print(content[:3])
        content: Dict[str, str] = await parse_result(results)
        print('results parsed')
        # clean up
        await browser.close()
        # display(content, 'output.txt')
        print('task completed')

if __name__ == '__main__': 
    asyncio.run(main())