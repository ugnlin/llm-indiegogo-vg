import time

import pandas as pd
from bs4 import BeautifulSoup
from fake_useragent import FakeUserAgent


class KickStarterScraper:
    def __init__(self, base_url: str = "https://www.kickstarter.com/", headers: dict = {}):
        headers['User-Agent'] = FakeUserAgent().chrome
        self.base_url = base_url
        self.headers = headers
        self._last_requested = time.time()

    def _wait(self, delay=5):
        # not utilized - no delay specified in robots.txt but keeping it here in case
        time_since_last_req = time.time() - self._last_requested
        self._last_requested = time.time()
        if time_since_last_req > delay:
            pass
        else:
            time.sleep(delay - time_since_last_req + 0.01)

    def scrape(self) -> pd.DataFrame:
        # scrape those projects!

        results = pd.DataFrame()

        results = pd.concat([results, self.fetch_projects()], ignore_index = True)

        return results

    def fetch_projects(self,
                       raised: int = 0,
                       start_page: int = 100, # from manual inspection - this will get historical projects
                       end_page: int = 200 # and the requests seem to go bad after 200 - this'll be enough data fn
                       ) -> list[str]:

        projects = []
        # for each page of projects...
        for page_number in range(start_page, end_page + 1):
            page = self._get_page(raised, page_number)
            projects_on_page = something

            # for each project in the page...
            for project_page in projects_on_page:
                project = self._get_project(project_page)

            projects.append(project)

        return projects

    def _get_page(self, raised: int, page_number: int) -> BeautifulSoup:
        pass

    def _get_project(self) -> Project:
        pass
