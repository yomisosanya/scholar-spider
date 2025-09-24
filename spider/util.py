import asyncio
from playwright.async_api import async_playwright, Browser, Locator
from base import BaseBrowser, BrowserChoice, SitePage
from engine import Scholar
from typing import List



# async def _Xchoose_browser(pa
#                       context,
#                      choice: BrowserChoice = BrowserChoice.chromium):
#     match choice:
#         case BrowserChoice.chromium:
#             browser: Browser = await playwright.chromium.launch()
#         case BrowserChoice.firefox:
#             browser: Browser = await playwright.firefox.launch()
#         case BrowserChoice.webkit:
#             browser: Browser = await playwright.webkit.launch()
#         case _: 
#             raise AttributeError(name='BrowserChoice type expected {} found'.format(type(choice)))
#     async with BaseBrowser(browser) as helper:
#             return await sitepage.visit(helper.browser)


async def _choose_browser(context, choice):
    match choice:
        case BrowserChoice.chromium:
            return await context.chromium.launch()
        case BrowserChoice.firefox:
            return await context.firefox.launch()
        case BrowserChoice.webkit:
            return await context.webkit.launch()
        case _: 
            raise AttributeError(name='BrowserChoice type expected {} found'.format(type(choice)))
        


async def _search_site(site: SitePage, query: str):
    res: List[Locator] = await site.search(query)
    results: List = await site.parse_list(res)
    return results

async def async_search(query: str, 
                       sitepage: SitePage, 
                       choice: BrowserChoice = BrowserChoice.chromium):
    """
    """
    async with async_playwright() as playwright:
        browser: Browser = await _choose_browser(playwright, choice)
        async with BaseBrowser(browser) as helper:
            #
            site: SitePage = await sitepage.visit(helper.browser)
            results: List = await _search_site(site, query)
            return results


async def async_search_list(queries: List[str], 
              sitepage: SitePage, 
              choice: BrowserChoice = BrowserChoice.chromium):
    """
    """ 
    async with async_playwright() as playwright:
        browser: Browser = await _choose_browser(playwright, choice)
        async with BaseBrowser(browser) as helper:
            site: SitePage = await sitepage.visit(helper.browser)
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
