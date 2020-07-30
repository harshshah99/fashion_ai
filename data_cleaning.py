import pandas as pd
import os
import yaml

scraped_files_path = 'data_files/scraped_data/'

with open('config.yml') as f:
	config_data = yaml.load(f,Loader=yaml.FullLoader)

sites = config_data.get('sites')
verticals = config_data.get('verticals')


def myntra_cleaner():
	files = [file for file in os.listdir(scraped_files_path) if file.split(sep='_',maxsplit=2)[0]=='MYNTRA']
	print(files)

myntra_cleaner()