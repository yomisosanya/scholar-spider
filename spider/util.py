import asyncio
from playwright.async_api import async_playwright, Browser, Locator
from base import BaseBrowser, BrowserChoice, SitePage
from engine import Scholar
from typing import List


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
    """A coroutine that returns a list of dicts, each dict contain a result 
    field. This coroutine only returns the first page. if you want access to
    the other result pages, use the async_search_all generator
    """
    async with async_playwright() as playwright:
        browser: Browser = await _choose_browser(playwright, choice)
        async with BaseBrowser(browser) as helper:
            #
            site: SitePage = await sitepage.visit(helper.browser)
            results: List = await _search_site(site, query)
            return results
        
async def async_search_all(query: str,
                           sitepage: SitePage,
                           choice: BrowserChoice = BrowserChoice.chromium):
    """An asynchronous generator that returns a list of result pages. 
    Each result page is a list of dicts, each dict is a result field.
    async_search_all is similar to async_search, the later only returns 
    the first page  
    """
    # returns every result page
    async with async_playwright() as playwright:
        browser: Browser = await _choose_browser(playwright, choice)
        async with BaseBrowser(browser) as helper:
            site: SitePage = await sitepage.visit(helper.browser)
            results: List = await _search_site(site, query)
            yield results
            others: List = await site.other_pages()
            for item in others:
                yield await site.parse_list(item)


async def async_search_list(queries: List[str], 
              sitepage: SitePage, 
              choice: BrowserChoice = BrowserChoice.chromium):
    """An asynchronous generator that returns a list of dicts, each dict contain a result 
    field. This coroutine only returns the first page. This coroutine is 
    identical to the async_search except that it takes a list of strings which 
    async_search on takes one string. it only returns the first page of query.
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




