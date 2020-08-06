import pandas as pd
import os
import yaml
import json
import time
import pickle
import re
import warnings
warnings.filterwarnings('ignore')

scraped_files_path = 'data_files/scraped_data/'
output_files_path = 'data_files/final_data/'

#---------------------------------------------------------------------------------#
"""
config.yml is read and all verticals and sites present in it are loaded.
NOTE : To include the vertical and Site in final ranking, make sure they are present in config.yml
"""

with open('config.yml') as f:
	config_data = yaml.load(f,Loader=yaml.FullLoader)

sites = config_data.get('sites')
verticals = config_data.get('verticals')

#---------------------------------------------------------------------------------#

with open ('colors.pkl', 'rb') as fp:
	colors_list = pickle.load(fp)

colors_list = [color.lower() for color in colors_list]


def asos_color_finder(product_name):
	for color in colors_list:
		if color in product_name.split():
			return color
	
	return 'Error'

def url_regex(json_string):
	regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
	urls = re.findall(regex,json_string)   
	links = []
	for link in urls:
		links.append(link[0])
	return links

def myntra_cleaner(csv_path):
	print('myntra : ' ,csv_path)
	vertical = csv_path.split(sep='_',maxsplit=2)[2].split('.csv')[0]
	category = csv_path.split(sep='_',maxsplit=2)[1]
	site = csv_path.split(sep='_',maxsplit=2)[0]
	myntra_data = pd.read_csv(scraped_files_path+csv_path)
	myntra_data_clean = myntra_data[['PAGE_URL_COMPLETE','productName','images','primaryColour','systemAttributes']]
	myntra_data_clean['imageUrl'] = myntra_data_clean['images'].apply(lambda x : url_regex(x)[0])
	myntra_data_clean['Trending'] = myntra_data_clean['systemAttributes'].apply(lambda x : len(x)>2)
	myntra_data_clean.drop(['systemAttributes','images'],axis = 1 , inplace = True)
	myntra_data_clean.rename(columns= {"primaryColour":"color","productName":"name"},inplace=True)
	myntra_data_clean['Site'] = site
	myntra_data_clean['Category'] = category
	return myntra_data_clean


def asos_cleaner(csv_path):
	print('asos : ' ,csv_path)
	vertical = csv_path.split(sep='_',maxsplit=2)[2].split('.csv')[0]
	category = csv_path.split(sep='_',maxsplit=2)[1]
	site = csv_path.split(sep='_',maxsplit=2)[0]
	temp_df = pd.read_csv(scraped_files_path + file)
	asos_data_clean = temp_df[['name','imageUrl','PAGE_URL_COMPLETE','isSellingFast']]
	asos_data_clean['color'] = asos_data_clean['name'].apply(lambda x: asos_color_finder(x))
	asos_data_clean['Site'] = site
	#asos_data_clean['imageUrl'] = asos_data_clean['imageUrl'].apply(lambda x  : [x])
	asos_data_clean.rename(columns = {"isSellingFast":"Trending"},inplace=True)
	asos_data_clean = asos_data_clean[['PAGE_URL_COMPLETE','name','color','imageUrl','Trending','Site']]
	asos_data_clean['Category'] = category
	return asos_data_clean

def ajio_cleaner(csv_path):
	print('ajio : ' ,csv_path)
	vertical = csv_path.split(sep='_',maxsplit=2)[2].split('.csv')[0]
	category = csv_path.split(sep='_',maxsplit=2)[1]
	site = csv_path.split(sep='_',maxsplit=2)[0]
	temp_df = pd.read_csv(scraped_files_path + file)
	ajio_data_clean = temp_df[['PAGE_URL_COMPLETE','name','images']]
	ajio_data_clean['Site'] = site
	ajio_data_clean['Trending'] = False
	if category=='new':
		ajio_data_clean['Trending'][0:10] = True
	else:
		ajio_data_clean['Trending'][0:20] = True
	ajio_data_clean['imageUrl'] = ajio_data_clean['images'].apply(lambda x : url_regex(x)[0])
	ajio_data_clean['color'] = ajio_data_clean['PAGE_URL_COMPLETE'].apply(lambda x : x.split('_')[1])
	ajio_data_clean['Category'] = category
	ajio_data_clean = ajio_data_clean[['PAGE_URL_COMPLETE','name','color','imageUrl','Trending','Site','Category']]
	return ajio_data_clean

def koovs_cleaner(csv_path):
	print('koovs : ' ,csv_path)
	vertical = csv_path.split(sep='_',maxsplit=2)[2].split('.csv')[0]
	category = csv_path.split(sep='_',maxsplit=2)[1]
	site = csv_path.split(sep='_',maxsplit=2)[0]
	temp_df = pd.read_csv(scraped_files_path + file)
	koovs_data_clean = temp_df[['PAGE_URL_COMPLETE','productName','mainColor','imageSmallUrl','isTrending']]
	koovs_data_clean['Site'] = site
	koovs_data_clean['Category'] = category
	koovs_data_clean = koovs_data_clean.rename(columns= {"productName":"name","mainColor":"color","imageSmallUrl":"imageUrl","isTrending":"Trending"})
	koovs_data_clean = koovs_data_clean[['PAGE_URL_COMPLETE','name','color','imageUrl','Trending','Site','Category']]
	koovs_data_clean['color'] = koovs_data_clean['color'].apply(lambda x : x[2:-2])
	return koovs_data_clean


function_index = {
	'MYNTRA' : myntra_cleaner,
	'ASOS' : asos_cleaner,
	'AJIO': ajio_cleaner,
	'AJIO-TRENDS' : ajio_cleaner,
	'KOOVS' : koovs_cleaner
}

def site_cleaner(name,csv_name):
	data = function_index[name](csv_name)
	return data


#---------------------------------------------------------------------------------#
#MAIN LOOP
	
for vertical in verticals:
	print(vertical.upper())
	cumulated_dataframe = pd.DataFrame()
	for file in os.listdir(scraped_files_path):
		if file.split(sep='_',maxsplit=2)[2].split('.csv')[0]==vertical:
			category = file.split(sep='_',maxsplit=2)[1]
			site = file.split(sep='_',maxsplit=2)[0]
			outdir = output_files_path + vertical + '/'
			temp_df = site_cleaner(site,file)
			if(type(temp_df) == type(pd.DataFrame())):
				cumulated_dataframe	= cumulated_dataframe.append(temp_df,ignore_index=True)
	print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
	print(cumulated_dataframe)
	cumulated_dataframe.to_csv(output_files_path + vertical + '.csv')
	print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')


#---------------------------------------------------------------------------------#
