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
        self._page = page
        self.response = res

    # @override
    # @property
    # def page(self):
    #     return type(self)._page

    @override
    def get_page(self):
        return self._page

    # @override
    # @property
    # def url(self):
    #     """Required property
    #     """
    #     return type(self)._url

    @override
    @classmethod
    def get_url(cls):
        return cls._url

    
    @override
    async def search(self, query) -> Optional[List[Locator]]:
        """
        """
        page: Page = self._page
        input: Locator = page.locator('#gs_hdr_tsi')
        await input.press_sequentially(query, delay=10.0)
        submit: Locator = page.locator('#gs_hdr_tsb')
        await submit.click()
        await page.wait_for_load_state('domcontentloaded')
        results: Optional[List[Locator]] = await page.locator('div.gs_ri').all()
        return results
    
    @override
    async def other_pages():
        """
        """

    @override
    @staticmethod
    async def parse_each(node: Locator):
        """
        """
        await asyncio.sleep(0)
        link: Locator = node.locator('h3.gs_rt a')
        title: str = await link.all_inner_texts()
        yield 'title', title
        url: str = 'url', await link.get_attribute('href') or ''
        yield 'url', url
        authors: List[str] = await node.locator('div.gs_a').all_inner_texts() or []
        yield 'authors', authors
        summary: List[str] = await node.locator('div.gs_rs').all_inner_texts() or []
        yield 'summary', summary
        citedby: List[str] = await node.get_by_role('link', name='Cited by').all_inner_texts() or []
        yield 'cite-by', citedby