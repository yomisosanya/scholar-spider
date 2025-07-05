import asyncio, re
from collections.abc import Awaitable
from enum import auto, Enum
from typing import AnyStr, Dict, List, Union
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
            browser = playwright.chromium.launch()
        case BrowserChoice.firefox:
            browser = playwright.firefox.launch()
        case BrowserChoice.webkit:
            browser = playwright.webkit.launch()

async def create_page(browser: Browser, incognito: bool = False) -> Awaitable[Page]:
    """
    Helper function for creating a new Page object 
    """
    if incognito:
        context: BrowserContext = await browser.new_context()
        return context.new_page()
    else:
        return browser.new_page()

async def visit(*, uri: str, page: Page) -> Awaitable[Union[Response, None]]:
    """
    A light-weight fetch that returns Response object 
    and tries not to open unecessary files
    """
    pattern: re.Pattern[AnyStr] = re.compile('')
    # don't load unneccesary files
    await page.route(pattern, lambda route: route.abort())
    return page.goto(uri=uri, wait_until='domcontentloaded')

async def search(page: Page, text: str) -> Awaitable[Locator]:
    selector: str = 'imput[name="q"]'
    await page.fill(selector, text)
    await page.press(selector, 'Enter')
    result_selector: str = 'div.gs_ri'
    await page.wait_for_selector(result_selector, timeout=10000)
    return page.locator(result_selector)

async def parse_result(items: Locator) -> Awaitable[Dict[str, str]]:
    values: Dict[str, str] = {}
    results: List[Locator] = items.all()
    async for result in results:
        title: Locator = await result.locator('div.gs_rt')
        # resolve title
        author: Locator = await result.locator('div.ge_a')
        # resolve author
        abstract: Locator = await result.locator('div.gs_rs')
        # resolve abstract
        citations: Locator = await result.get_by_role('link', name='Cited by')
        # resolve citation
        year: Locator = await result.locator('.gs_age')
        # resolve year
        url: Locator = await result.locator('h3.gs_rt a')
        values['url'] = await url.get_attribute('href') or ''
    return values

async def main():
    async with async_playwright as app:
        browser: Browser = await create_browser(BrowserChoice.chromium, app)
        uri: str = 'https://scholar.google.com'
        page: Page = await create_page(browser) 
        res: Response = await visit(uri=uri, page=page) 
        if res is None:
            # error message
            return
        query: str = 'hpcc cuny'
        results = await search(page, query)
        await parse_result(results)
        # clean up
        browser.close()

if __name__ == '__main__': 
    asyncio.run(main())