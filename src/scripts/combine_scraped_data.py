import pandas as pd
import glob

# Path to the directory containing your CSV files
path = '../data/scraped/'  # Replace with the path to your CSV files
all_files = glob.glob(path + "/scraped*.csv")

# List comprehension to load all CSV files
all_dfs = [pd.read_csv(filename) for filename in all_files]

# Concatenate all DataFrames into one
combined_df = pd.concat(all_dfs, ignore_index=True).drop(columns='Unnamed: 0').drop_duplicates()

combined_df.to_csv('../data/scraped/full.csv')