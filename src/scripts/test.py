from src.scraper import IGGScraper
from dataclasses import asdict

import pandas as pd

scraper = IGGScraper()
projects = scraper.fetch_projects()

raw_features_list = [asdict(project.raw) for project in projects]

df = pd.DataFrame(raw_features_list)
df.to_csv('./data/scraped.csv')

