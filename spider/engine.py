#
from base import SitePage

import asyncio
from collections.abc import Awaitable
from typing import List, Optional, override

from playwright.async_api import Locator, Page, Response

__all__ = ['Scholar']


class Scholar(SitePage):

    _url = 'https://scholar.google.com'
    input_id = '#gs_hdr_tsi'
    submit_id = '#gs_hdr_tsi'
    result_class = 'div.gs_ri'

    @override
    def __init__(self, page: Page, res: Response):
        super().__init__(page, res)
        # self._page = page
        # self.response = res
        # self._query = None 
    
    @override
    @property
    def page(self) -> Page:
        return self._page

    @override
    def get_page(self):
        return self._page

    @override
    @classmethod
    def get_url(cls):
        return cls._url

    
    @override
    async def search(self,
                      query,
                      delay = 5
                      ) -> List[Locator]:
        """
        """
        match query:     
            case q if isinstance(q, str):
                # queury 
                match q:
                    case '':
                        return []
                    case x if x == self._query:
                        return self._first
                    case _:
                        #
                        self._first = None
                        self._others = None
                        page: Page = self._page
                        input: Locator = page.locator('#gs_hdr_tsi')
                        await input.press_sequentially(query, delay=delay)
                        submit: Locator = page.locator('#gs_hdr_tsb')
                        await submit.click()
                        await asyncio.sleep(0)
                        await page.wait_for_load_state('domcontentloaded')
                        result_page: Locator = page.locator('div.gs_ri')

                        await page.wait_for_load_state('load')
                        self._first: List[Locator] = await result_page.all()
                        return self._first
            case e:
                # all other types are rejected
                raise AttributeError(name='query must be a string, {} found'.format(type(e)))
    
    @override
    async def other_pages(self):
        """
        """
        if self._others is None:
            pass
        #

    @override
    @staticmethod
    async def parse_each(node: Locator):
        """
        """
        await asyncio.sleep(0)
        link: Locator = node.locator('h3.gs_rt a')
        title: str = await link.all_inner_texts()
        yield 'title', title
        url: str = await link.get_attribute('href') or ''
        yield 'url', url
        authors: List[str] = await node.locator('div.gs_a').all_inner_texts() or []
        yield 'authors', authors
        summary: List[str] = await node.locator('div.gs_rs').all_inner_texts() or []
        yield 'summary', summary
        citedby: List[str] = await node.get_by_role('link', name='Cited by').all_inner_texts() or []
        yield 'cite-by', citedby

