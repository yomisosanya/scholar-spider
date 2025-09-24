import asyncio
from playwright.async_api import async_playwright, Browser, Locator
from base import BaseBrowser, BrowserChoice, SitePage
from engine import Scholar
from typing import List



async def _visit_site(sitepage: SitePage, 
                     choice: BrowserChoice = BrowserChoice.chromium):
    async with async_playwright() as playwright:
        match choice:
            case BrowserChoice.chromium:
                browser: Browser = await playwright.chromium.launch()
            case BrowserChoice.firefox:
                browser: Browser = await playwright.firefox.launch()
            case BrowserChoice.webkit:
                browser: Browser = await playwright.webkit.launch()
            case _: 
                raise AttributeError(name='BrowserChoice type expected {} found'.format(type(choice)))
        async with BaseBrowser(browser) as helper:
            return sitepage.visit(helper.browser)


async def _search_site(site: SitePage, query: str):
    res: List[Locator] = await site.search(query=query)
    results: List = await site.parse_list(res)
    return results

async def async_search(query: str, 
                       sitepage: SitePage, 
                       choice: BrowserChoice = BrowserChoice.chromium):
    """
    """
    site: SitePage = await _visit_site(sitepage, choice)
    results: List = await _search_site(site, query)
    return results


async def async_search_list(queries: List[str], 
              sitepage: SitePage, 
              choice: BrowserChoice = BrowserChoice.chromium):
    """
    """ 
    site: SitePage = await _visit_site(sitepage, choice)
    for query in queries:
        results: List = await _search_site(site, query)
        yield results
        
def search(query: str, 
           sitepage: SitePage, 
           choice: BrowserChoice = BrowserChoice.chromium):
    """
    """
    return asyncio.run(async_search(query=query, sitepage=sitepage, choice=choice))

def google_search(query: str, choice: BrowserChoice = BrowserChoice.chromium):
    """
    """
    return search(query=query, choice=choice, sitepage=Scholar)
