#!/usr/bin/env python

"""
"""

from abc import ABC, abstractmethod
import asyncio
from collections.abc import Awaitable  
from enum import auto, Enum
from typing import Any, AsyncGenerator, Coroutine, Dict, final, List, Optional, overload, Self, Tuple, Union

from playwright.async_api import Browser, BrowserContext, Locator, Page, Playwright, Response


__all__ = ['BrowserChoice', 'BaseBrowser', 'SitePage']

#                                                      State Diagram
#   
#   Browser instance [browser] ---> BaseBrowser.create(browser)
#                                |
#                                V
#                      BaseBrowser instance  [bb] + Playwright.Page page [url]  --->  SitePage.visit(page) <Playwright.Page>
#                                                                                 |
#                                                                                 V
#                                                                       Playwright.Page [page] + Playwright.Response
#                                                                                 |
#                                                                                 V
#                      SitePage instance [site]         <---            SitePage.create(page) <SitePage>
#                      +  query string [query]
#                               |
#                               V
#                      site.search(query) <List> or None
#
#                      

class BrowserChoice(Enum):
    chromium = auto()
    firefox = auto()
    webkit = auto()

class SiteError(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(message)


class SitePage(ABC):

    """Base interface for SitePage types
    A SitePage is a wrapper around a Playwright.Page object, that 
    retrieves specific data from the uri it is attached to.
    """

    @abstractmethod
    def __init__(self, page: Page, res: Response) -> Self:
        """
        """
        self._page = page
        self.response = res
        self._query = None


    @property
    @abstractmethod
    def page(self) -> Page:
        """
        """

    @abstractmethod
    def get_page(self):
        """
        """


    @abstractmethod
    async def search(self,
                      query: str,
                      delay: float = 10
                      ) -> Coroutine[Any, Any, Optional[List[Locator]]]:
        """
        """

    @abstractmethod
    async def other_pages(self) -> List[Locator]:
        """
        """

    @staticmethod
    @abstractmethod
    async def parse_each(node: Locator) -> AsyncGenerator[Tuple[str, List]]:
        """
        """

    @final
    @classmethod
    async def parse_group(cls, nodes: List[Locator]) -> Coroutine[Any, Any, List[Dict]]:
        """
        """
        return ({k: v async for k, v in cls.parse_each(node)} for node in nodes)

    @final
    @classmethod
    async def parse_list(cls, nodes):
        results = await cls.parse_group(nodes)
        return [result async for result in results]


    # @final
    @classmethod
    async def visit(cls, 
                    browser: Union[Browser, BrowserContext],
                    incognito: bool = False,
                    attempts: int = 2,
                    delay: float = 10,
                    verbose: bool = False) -> Optional[Self]:
        """
        """
        assert browser is not None, 'NoneType passed instead of Browser to visit()'
        page: Page = await browser.new_page()
        url: str = cls.get_url()
        # assert isinstance(url, str), "{}.url is not a string".format(cls.__name__)
        for count in range(attempts):
            if verbose:
                print('attempt #{}'.format(count+1))
            res: Optional[Response] = await page.goto(url=url, wait_until='domcontentloaded')
            match res.status:
                case 200:
                    return cls(page, res)
                case 429:
                    raise SiteError(message='status: 429 - Too Many Requests')
                case _:
                    pass
            asyncio.sleep(delay=delay)
                
    

class BaseBrowser:
    """A Helper class that is used to create Playwright.Browsers
    """

    def __init__(self, browser: Browser):
        self._browser = browser

    @property
    def browser(self):
        return self._browser
    
    async def __aenter__(self):
        """
        """
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        """
        if self._browser:
            for context in self._browser.contexts:
                for page in context.pages:
                    await page.close()
                await context.close()
            await self._browser.close()

