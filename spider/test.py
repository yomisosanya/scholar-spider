#!/usr/bin/env python

import asyncio
from typing import Dict, Final, List, Tuple
from pathlib import Path

import json 
#
import browse
from browse import create_browser, create_page, parse_groups, \
more_results, nav_url, visit_page
#
from playwright.async_api import async_playwright, Browser, Locator, Page, \
Response

from base import BrowserChoice
from base import BaseBrowser
from engine import Scholar
from util import google_search, search
from view import load_data, store_data, convert_to_csv 

GOOGLE_SCHOLAR_URL: Final[str] = 'https://scholar.google.com'

async def app(*, query: str) -> None:
    """
    
    """
    # TODO: parameter should be a coroutine that returns a list of Locators
    #
    async with async_playwright() as context:
        browser: Browser = await create_browser(BrowserChoice.chromium, context)
        assert browser is not None, 'browser was not created'
        uri: str = GOOGLE_SCHOLAR_URL
        page: Page = await create_page(browser)
        assert page is not None, 'a page was not created'
        res: Response = await visit_page(uri=uri, page=page)
        assert res is not None, 'possible network connection problems'
        await page.wait_for_load_state('domcontentloaded')
        # search only after the DOM is loaded
        results: List[Locator] = await browse.search(page, text=query)
        assert results is not None, 'search returned None instead of a locator'
        assert len(results) > 0, 'search returned an empt list of locators'
        output: List[dict] = await parse_groups(results)
        # display output
        # print(output)
        print(output[2])
        await asyncio.sleep(0)
        nodes: List[Locator] = await more_results(page)
        assert nodes is not None, 'more_result return None instead of an empty list' 
        assert len(nodes) > 0, 'more_results returned an empty list'
        print(len(nodes))
        item: Tuple[ int, str] = await nav_url(nodes[4])
        # print(item)
        print(output)  
        print('\n\n\n\n')
        print(output[2]) 
        

async def new_app(*, query: str) -> None:

    #
    async with async_playwright() as playwright:
        # create browser helper with browser of your choice
        browser: Browser = await playwright.chromium.launch()
        async with BaseBrowser(browser) as helper:
            #
            sch: Scholar = await Scholar.visit(helper.browser)
            headers = await sch.response.headers_array()
            print(headers[:10])
            print('http status code: {}'.format(sch.response.status))
            res: List[Locator] = await sch.search(query=query)
            # assert res is not None, "search return None"
            # assert len(res) != 0, "search returned an empty list"
            # print(res)
            # results = await Scholar.parse_group(res)
            # print([x async for x in results])
            results = await Scholar.parse_list(res)
            print(results)


def print_each(items: List):
    for item in items:
        print(item)
        print('\n')
        return
    
dict_list = [
        {'title': 'A novel algorithm for the detection of protein complexes with the breadth first search0',
         'link': 'https://scholar.google.com/scholar?cluster=13763170924097322219&hl=en&as_sdt=0'},
        {'authors': 'Louis Petingi, Richard Alba, Alexander Tzanov, Robert Alfano, Beth Baron'},
        {'source': 'Bioinformatics (Oxford, England) (2020)'},
        {'link': 'https://doi.org/10.1093/bioinformatics/btaa1017'},
        {'cited by': 'Cited by 10'},
        {'related': 'Related articles'},
        {'all 5': 'All 5 versions'}]


if __name__ == '__main__':
    # query: str = 'alexander tzanov'
    query = ['louis petingi', 'richard alba', 'alexander tzanov', 'robert alfano', 'beth baron']


    # asyncio.run(app(query=query[4]))
    # asyncio.run(new_app(query=query[3]))
    # print(google_search(query))
    # print('\n')
    # result = google_search(query[1])
    # # result = dict_list
    # store_data(result, Path('../target/output.json'))
    data = load_data(Path('../target/output.json'))
    convert_to_csv(data)
