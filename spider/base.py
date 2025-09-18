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
#   BrowserChoice enum [bc] ---> BaseBrowser.createBrower(bc)
#                                |
#                                V
#                      BaseBrowser instance  [bb] + url string [url]  --->  bb.visit(url) <Playwright.Page>
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


class SitePage(ABC):

    """Base interface for SitePage types
    A SitePage is a wrapper around a Playwright.Page object, that 
    retrieves specific data from the uri it is attached to.
    """

    @abstractmethod
    def __init__(self, page: Page, res: Response) -> Self:
        """
        """

    def __del__(self):
        """
        """
        # page: Page = self.get_page()
        # asyncio.run(page.close())

    # @property
    # @abstractmethod
    # def page(self):
    #     """
    #     """

    @abstractmethod
    def get_page(self):
        """
        """

    # @property
    # @abstractmethod
    # def url(self) -> str:
    #     """The constant url of the page
    #     """

    @classmethod
    @abstractmethod
    def get_url(cls):
        """
        """

    @abstractmethod
    async def search(self, query: str) -> Coroutine[Any, Any, Optional[List[Locator]]]:
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
        return [result for result in await cls.parse_group(nodes)]


    # @final
    @classmethod
    async def visit(cls, 
                    browser: Union[Browser, BrowserContext],
                    incognito: bool = False):
        """
        """
        assert browser is not None, 'NoneType passed instead of Browser to visit()'
        page: Page = await browser.new_page()
        url: str = cls.get_url()
        # print('the value of url is {}'.format(url))
        # assert isinstance(url, str), "{}.url is not a string".format(cls.__name__)
        res: Optional[Response] = await page.goto(url=url, wait_until='domcontentloaded')
        if res:
            return cls(page, res)
    


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

    # @staticmethod
    # async def create(playwright: Playwright, 
    #                  choice: BrowserChoice
    #                  ) -> Self:
    #     """
    #     """
    #     match choice:
    #         case BrowserChoice.chromium:
    #             browser = await playwright.chromium.launch()
    #         case BrowserChoice.firefox:
    #             browser = await playwright.firefox.launch()
    #         case BrowserChoice.webkit:
    #             browser = await playwright.webkit.launch()
    #         case _ :
    #             raise ValueError('illegal parameter: ', choice)
    #     assert browser is not None, 'Browser is not created in BaseBrowser'
    #     return BaseBrowser(browser)




