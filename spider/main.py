import asyncio
from typing import List
from browse import BrowserChoice, create_browser, create_page, parse_groups, search, visit
from playwright.async_api import async_playwright, Browser, Locator, Page, Response

async def app(*, query: str) -> None:
    """
    """
    async with async_playwright() as context:
        browser: Browser = await create_browser(BrowserChoice.chromium, context)
        assert browser is not None, 'browser was not created'
        uri: str = 'https://scholar.google.com'
        page: Page = await create_page(browser)
        assert page is not None, 'a page was not created'
        res: Response = await visit(uri=uri, page=page)
        assert res is not None, 'possible network connection problems'
        # continue only after the DOM loads
        await page.wait_for_load_state('domcontentloaded')
        results: List[Locator] = await search(page, text=query)
        assert len(results) > 0, 'search did not return any locator'
        output = await parse_groups(results)
        # display output
        print(output)

if __name__ == '__main__':
    query: str = 'hpcc cuny'
    asyncio.run(app(query=query))