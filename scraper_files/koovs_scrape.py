import json
import pandas as pd
import requests
import os


def dataframe_handling(df1,category,website_name,unique_column_name,domain_name,url_column_name,name_tag):
	df_clean = df1.reset_index(drop=True)
	df_clean = df_clean.drop_duplicates(unique_column_name,keep='first')
	df_clean['url_given'] = df_clean[url_column_name].apply(lambda x : x[0].get('href'))
	df_clean['PAGE_URL_COMPLETE'] = df_clean['url_given'].apply(lambda x : domain_name + str(x))
	df_name = website_name  + '_' + name_tag + '_' + category + '.csv'  
	df_clean.to_csv('data_files/' + 'scraped_data/' + df_name)
	print(df_clean)
	return df_clean,df_name


class koovs_products:
	# https://www.koovs.com/jarvis-service/v1/product/listing/complete?href=https%3A%2F%2Fwww.koovs.com%2Fmen%2Ft-shirts-and-polo-shirts%2F&page-size=100&sort=latest

	num_of_results = 100 #Not used anywhere, just for reference 

	def __init__(self,category):
		self.category = category

	def scrape_new(self):
		with open('category_wise_links/koovs_links.json') as f:
			koovs_links = json.load(f)
		
		product_api_link_new = koovs_links.get(self.category)
		response = requests.get(url=product_api_link_new, headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0'})
		data = response.json()
		product_list = data.get('data')[0].get('data')
		new_dataframe	= pd.DataFrame.from_records(product_list) 
		for i in product_list:
			print(i)
			print('\n')

			print("\n\n\n----------------------------------------------------------------------------------------\n\n\n")

		new_dataframe = new_dataframe.reset_index(drop=True)

		return new_dataframe,'new'
			
	def scrape_popular(self):
		with open('category_wise_links/koovs_links.json') as f:
			koovs_links = json.load(f)
		product_api_link_popular = koovs_links.get(self.category)
		product_api_link_popular = product_api_link_popular.replace('sort=latest','sort=relevance')
		print(product_api_link_popular)
		
		response = requests.get(url=product_api_link_popular, headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0'})
		data = response.json()
		product_list = data.get('data')[0].get('data')
		popular_dataframe	= pd.DataFrame.from_records(product_list)
		for i in product_list:
			print(i)
			print('\n')

			print("\n\n\n----------------------------------------------------------------------------------------\n\n\n")

		popular_dataframe = popular_dataframe.reset_index(drop=True)

		return popular_dataframe,'popular'
				

with open('category_wise_links/koovs_links.json') as f:
	products = json.load(f)

product_names = products.keys()


for pname in product_names:
	print(pname)
	temp_koovs_object = koovs_products(pname)
	
	new_df,tag_new = temp_koovs_object.scrape_new()
	popular_df, tag_popular = temp_koovs_object.scrape_popular()

	final_new,_ = dataframe_handling(df1 = new_df, category= pname, website_name= 'KOOVS', unique_column_name = 'id', domain_name = 'www.koovs.com', url_column_name = 'links', name_tag = tag_new)
	final_popular,_ = dataframe_handling(df1 = popular_df, category= pname, website_name= 'KOOVS', unique_column_name = 'id', domain_name = 'www.koovs.com', url_column_name = 'links', name_tag = tag_popular)