import json
import time
import html
from copy import deepcopy
from dataclasses import asdict

import cfscrape
import pandas as pd
import requests
from bs4 import BeautifulSoup

from ..common.project import Project


class IGGScraper:
    def __init__(self, base_url: str = "https://www.indiegogo.com"):
        self.scraper = cfscrape.create_scraper()
        self.base_url = base_url
        self.post_headers = {
            "Accept": 'application/json',
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-GB,en;q=0.9,ja-JP;q=0.8,ja;q=0.7,zh-CN;q=0.6,zh;q=0.5,en-US;q=0.4",
            "Content-Length": "221",
            "Content-Type": "application/json",
            "Cookie": "visitor_id=3df2e0113da8d2606e5f3873e832eb8999dde9008f7f93acecb85f2922c37266; _session_id=35bcd990c9b6c80bc1c8888a17bc15ac; x-spec-id=f63b9b313bea40ee99fe478857e26c8f; localCurrencyIsoCode=USD; __stripe_mid=fa430a18-496a-4816-b6f7-b7ac01641b4b071d71; __stripe_sid=126195bb-16b3-4e81-9404-62fa2509219233e0fb; analytics_session_id=a505517a525e2bff7d20c0378d046d1d5c55799978a810430f3bfdc08e3f8a5d; romref=shr-pies; romref_referer_host=www.indiegogo.com; cohort=www.indiegogo.com%7Csch-goog%7Cshr-pies; recent_project_ids=2694008%261119253",
            "Origin": "https://www.indiegogo.com",
            "Referer": "https://www.indiegogo.com/explore/video-games?project_timing=all&sort=trending",
            "Sec-Ch-Ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "\"Windows\"",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "X-Csrf-Token": "63pCVE1IOrzZ5JYVZFax9qbhKCJ0EdI2mjKygVxZ27AM3QglHmyfOw1Hn7uehxtVL+O41R/zq8+NeLk/h4ILHQ=="
        }
        self.get_headers = {
            # "Accept": 'application/json',
            # "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-GB,en;q=0.9,ja-JP;q=0.8,ja;q=0.7,zh-CN;q=0.6,zh;q=0.5,en-US;q=0.4",
            # "Content-Length": "221",
            "Content-Type": "application/json",
            "Cookie": "visitor_id=3df2e0113da8d2606e5f3873e832eb8999dde9008f7f93acecb85f2922c37266; _session_id=35bcd990c9b6c80bc1c8888a17bc15ac; x-spec-id=f63b9b313bea40ee99fe478857e26c8f; localCurrencyIsoCode=USD; __stripe_mid=fa430a18-496a-4816-b6f7-b7ac01641b4b071d71; __stripe_sid=126195bb-16b3-4e81-9404-62fa2509219233e0fb; analytics_session_id=a505517a525e2bff7d20c0378d046d1d5c55799978a810430f3bfdc08e3f8a5d; romref=shr-pies; romref_referer_host=www.indiegogo.com; cohort=www.indiegogo.com%7Csch-goog%7Cshr-pies; recent_project_ids=2694008%261119253",
            # "Origin": "https://www.indiegogo.com",
            "Referer": "https://www.indiegogo.com/explore/video-games?project_timing=all&sort=trending",
            "Sec-Ch-Ua": "\"Not_A Brand\";v=\"8\", \"Chromium\";v=\"120\", \"Google Chrome\";v=\"120\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "\"Windows\"",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            # "X-Csrf-Token": "63pCVE1IOrzZ5JYVZFax9qbhKCJ0EdI2mjKygVxZ27AM3QglHmyfOw1Hn7uehxtVL+O41R/zq8+NeLk/h4ILHQ=="
        }

        self._last_requested = time.time() - 5

    def _wait(self, delay=3):
        # 5s to keep them happy
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
                       start_page: int = 1,
                       end_page: int = 999
                       ) -> list[Project]:

        projects = []
        # for each page of projects...
        for page_number in range(start_page, end_page + 1):
            project_metadata_list = self._get_project_links(page_number)

            # for each project in the page...
            for project_metadata in project_metadata_list:
                project = self._get_project(project_metadata)

                if project:
                    projects.append(project)

            raw_features_list = [asdict(project.raw) for project in projects]

            df = pd.DataFrame(raw_features_list)
            df.to_csv('./data/scraped/full.csv')

        return projects

    def _get_project_links(self, page_number: int) -> list:
        url = f"https://www.indiegogo.com/private_api/graph/query?operation_id=discoverables_query"

        self._wait()
        page_content = json.loads(requests.post(url,
                                    headers = self.post_headers,
                                    params={'operation_id': 'discoverables_query'},
                                    data = json.dumps({"variables":
                                                {"category_main":"Video Games",
                                                 "category_top_level":"Creative Works",
                                                 "feature_variant":"none",
                                                 "page_num":page_number,
                                                 "per_page":12,
                                                 "project_timing":"all",
                                                 "project_type":"campaign",
                                                 "q":None,
                                                 "sort":
                                                 "trending",
                                                 "tags":[]}})
                                    ).content)

        return [item for item in page_content["data"]["discoverables"]]

    def _get_project(self, project_metadata: dict) -> Project | None:
        self._wait()

        res = requests.get(self.base_url + project_metadata['clickthrough_url'], headers=self.get_headers)
        project_id = res.headers['Set-Cookie'].split('recent_project_ids=')[1].split('%')[0].split(';')[0]

        project_desc_html = html.unescape(json.loads(
            requests.get(self.base_url + f'/private_api/campaigns/{project_id}/description',headers = self.get_headers).text
        )['response']['description_html'])
        project_desc = BeautifulSoup(project_desc_html, 'html.parser').get_text(separator=' \n ', strip=True)

        project_faqs_raw = json.loads(requests.post("https://www.indiegogo.com/private_api/graph/query?operation_id=campaign_faqs_query",
                                     headers=self.post_headers,
                                    params = {'operation_id': 'campaign_faqs_query'},
                                    data = json.dumps({"variables":{"project_id": f"{project_id}"}})
                                     ).content)
        faq_pairs = [f"Question: {faq['question']} - Answer: {faq['answer']}" for faq in project_faqs_raw['data']['project']['faqs']]

        try:
            project = Project.create(
                project_id = project_id,
                currency = project_metadata['currency'],
                name = project_metadata['title'],
                description = project_desc,
                faqs = faq_pairs,
                open_date = project_metadata['open_date'],
                close_date = project_metadata['close_date'],
                raised_percent = project_metadata['funds_raised_percent'],
                raised = project_metadata['funds_raised_amount']
            )
            print(project.raw.name)
            return project

        except RuntimeError:
            return None # some sort of unhandled data error - rare




