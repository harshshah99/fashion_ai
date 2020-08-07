"""
ALL files in data_files/scraped_data/ are from different websites meaning they all have different names of columns.
For the final ranking, to avoid bias towards products from a particular site, the scraped_data is cleaned and stored in data_files/final_data
What this script does is : 

1) Read all verticals to include in final_app from config.yml
2) For a given vertical, say men_tshirts, use all files present in data_files/scraped_data on men_tshirts(MYNTRA_new_men_tshirts.csv,KOOVS_popular_men_tshirts.csv....) and so on 
3) Clean all CSV's according to which sites they are originally from (MYNTRA CSV's are cleaned using myntra_cleaner, KOOVS using koovs_cleaner and so on)
4) All cleaned CSV's for men_tshirts contain same columns irrespective of their website they were scraped from.
5) For men_tshirts, tshirts from MYNTRA,KOOVS,AJIO.... etc are all cleaned and stored in a dataframe
6) Finally we have a men_tshirts.csv in data_files/final_data , which contains tshirts scraped from all websites with same columns

These above steps are repeated for all verticals just like men_tshirts.
CSV of format vertical-name.csv is saved in data_files/final_data which can be used for ranking the products.
"""


import pandas as pd
import os
import yaml
import json
import time
import pickle
import re
import warnings
warnings.filterwarnings('ignore')

scraped_files_path = 'data_files/scraped_data/' #path for all files scraped from different websites
output_files_path = 'data_files/final_data/'  #path where we will save all the CSV files from scraped_data after cleaning them with code of this file

#---------------------------------------------------------------------------------#
"""
config.yml is read and all verticals and sites present in it are loaded.
NOTE : To include the vertical and Site in final ranking, make sure they are present in config.yml
"""

with open('config.yml') as f:
	config_data = yaml.load(f,Loader=yaml.FullLoader)

config_sites = config_data.get('sites')
verticals = config_data.get('verticals')

#---------------------------------------------------------------------------------#


#colrs.pkl is dataset of popular set of colors which we plan to extract from names of certain products and is used in that
with open ('colors.pkl', 'rb') as fp:
	colors_list = pickle.load(fp)

colors_list = [color.lower() for color in colors_list] 

def asos_color_finder(product_name):
	"""
	product_name in ASOS is of format : ASOS DESIGN Petite chino pants in black
	asos_color_finder() uses colors_list from above and if a color from that list is in the name, we can say that the product's color is that
	for above  example : ASOS DESIGN Petite chino pants in black will return 'black' which is the color of the product
	for products whose color isn't available, it returns 'Error'
	"""
	for color in colors_list:
		if color in product_name.split():
			return color
	
	return 'Error'

def url_regex(json_string):
	""" 
	Parameters: a string full of multple urls
	Returns : a single URL string , the first one from multiple strings in input one
	A REGEX to find URLs from a string fulll of multiple URLs
	some sites have multiple image URLs while others only have one. So we decided to use one image per product
	This function finds and returns the first URL from a string containing multiple URLs
	THE REASON WE CHOOSE FIRST URL FROM A LIST OF MULTIPLE ONES IS BECAUSE WE FOUND THAT THE FIRST URL CONTAINS THE MOST RELAVENT IMAGE FOR A PRODUCT
	"""
	regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
	urls = re.findall(regex,json_string)   
	links = []
	for link in urls:
		links.append(link[0])
	return links

def myntra_cleaner(csv_path):
	"""
	parameters : file path for unclean MYNTRA CSV
	Returns : A dataframe with columns: 'PAGE_URL_COMPLETE','name','color','imageUrl','Trending','Site','Category' in this order
	To see how the cleaning is done refer to any CSV of MYNTRA from data_files/scraped_data . For EG : MYNTRA_new_men_tshirts.csv
	"""
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
	"""
	parameters : file path for unclean ASOS CSV
	Returns : A dataframe with columns: 'PAGE_URL_COMPLETE','name','color','imageUrl','Trending','Site','Category' in this order
	To see how the cleaning is done refer to any CSV of ASOS from data_files/scraped_data . For EG : ASOS_new_men_tshirts.csv
	"""
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
	"""
	parameters : file path for unclean AJIO/AJIO_TRENDS CSV
	Returns : A dataframe with columns: 'PAGE_URL_COMPLETE','name','color','imageUrl','Trending','Site','Category' in this order
	To see how the cleaning is done refer to any CSV of AJIO from data_files/scraped_data . For EG : AJIO_new_men_tshirts.csv
	"""
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
	"""
	parameters : file path for unclean KOOVS CSV
	Returns : A dataframe with columns: 'PAGE_URL_COMPLETE','name','color','imageUrl','Trending','Site','Category' in this order
	To see how the cleaning is done refer to any CSV of KOOVS from data_files/scraped_data . For EG : KOOVS_new_men_tshirts.csv
	"""
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


#function_index:  
#THIS IS USED TO MAP NAME OF CSV TO CORRESPONDING CLEANING FUNTION
#IF A MYNTRA CSV IS ENCOUNTERED IN THE MAIN LOOP(SEE BELOW), THIS FUNCTION INDEX CAN BE USED TO CALL myntra_cleaner to clean that CSV
#IF you add a new website, add the website NAME and the corresponding FUNCTION in function_index
#for example : 'NORDSTROM' : nordstrom_cleaner and create a function nordstrom_cleaner() above using other cleaner functions as base template
function_index = {
	'MYNTRA' : myntra_cleaner,
	'ASOS' : asos_cleaner,
	'AJIO': ajio_cleaner,
	'AJIO-TRENDS' : ajio_cleaner,
	'KOOVS' : koovs_cleaner
}

def site_cleaner(name,csv_name):
	"""
	TAKES IN SITE_NAME as name and csv_name from MAIN LOOP BELOW
	Uses function_index declared above to call corresponsing cleaner according to name of CSV . ie myntra_cleaner() for MYNTRA and koovs_cleaner() for KOOVS
	"""
	data = function_index[name](csv_name)
	return data






#---------------------------------------------------------------------------------#
#MAIN LOOP
	
"""
every file in data_files/scraped_data is of the format : MYNTRA_new_men_tshirts ie. {SITE-NAME}_{CATEGORY}_{VERTICAL}.csv
lets say str1 = '{SITE-NAME}_{CATEGORY}_{VERTICAL}.csv'
str1.split(sep='_',maxsplit=2)[0] will give {SITE-NAME}
str1.split(sep='_',maxsplit=2)[1] will give {CATEGORY} - either 'popular' or 'new'
str1.split(sep='_',maxsplit=2)[2] will give {VERTICAL} - for eg. men_tshirts or women_jumpsuits

This above logic is utilised to append all men_tshirts from different sites AFTER cleaning, to the dataframe cumulated_dataframe
cumulated_dataframe is then written to data_files/final_data
SO for VERTICAL : men_tshirts this  loop will go through all men_tshirts from different sites stored  in data_files/scraped_data,
clean them and make sure all of them have the same columns: 'PAGE_URL_COMPLETE','name','color','imageUrl','Trending','Site','Category' in this order
AND write this dataframe to a CSV of format {VERTICAL}.csv in data_files/final_data
"""
for vertical in verticals: #loop thorugh all verticals in config.yml
	print(vertical.upper())
	cumulated_dataframe = pd.DataFrame() #initialize empty dataframe from each vertical
	for file in os.listdir(scraped_files_path): #list  all files in data_files/scraped_data
		if file.split(sep='_',maxsplit=2)[2].split('.csv')[0]==vertical and file.split(sep='_',maxsplit=2)[0] in config_sites: #only if the vertical and sit are present in config.yml, will they be included in the final CSV
			category = file.split(sep='_',maxsplit=2)[1]
			site = file.split(sep='_',maxsplit=2)[0]
			temp_df = site_cleaner(site,file) #data cleaner called
			if(type(temp_df) == type(pd.DataFrame())): #if a dataframe is returned by the cleaner without any error
				cumulated_dataframe	= cumulated_dataframe.append(temp_df,ignore_index=True) #append the dataframe
	print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
	print(cumulated_dataframe) #after all files of a paricular VERTICAL have been appended to cumulated_dataframe,
	cumulated_dataframe.to_csv(output_files_path + vertical + '.csv') # Write the datframe to CSV in data_files/final_data
	print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')


#---------------------------------------------------------------------------------#
