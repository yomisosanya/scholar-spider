import asyncio, re
from typing import AnyStr
from playwright.async_api import async_playwright, Browser, \
    BrowserContext, BrowserType, Page, Playwright, Response

async def run(browser_choice: BrowserType, uri: str):
    browser: Browser = await browser_choice.launch()
    page: Page = browser.new_page()
    await page.goto(uri=uri)

async def create_page(browser: Browser, incognito: bool = False) -> Page:
    if incognito:
        context: BrowserContext = await browser.new_context()
        page: Page = await context.new_page()
    else:
        page: Page = await browser.new_page()
    return page

async def visit(*, uri: str, page: Page) -> Response:
    pattern: re.Pattern[AnyStr] = re.compile('')
    # don't load unneccesary files
    await page.route(pattern, lambda route: route.abort())
    res: Response = await page.goto(uri=uri, wait_until='domcontentloaded')
    return res