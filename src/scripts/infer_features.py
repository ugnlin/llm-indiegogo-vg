import pandas as pd
from dotenv import load_dotenv
from src.common.project import Project

load_dotenv()

df = pd.read_csv('../data/scraped/full.csv').drop(columns='Unnamed: 0')
project = Project.load_raw(**df.sample().to_dict(orient='records')[0])

print('inferring features... ', end='')
project.generate_features()
print('done!')

print(project.features.title.value)
print(project.features.category.value)