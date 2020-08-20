import requests
import json
import pandas as pd
import os

##LOAD MYNTRA links into a variable used for scraping

def dataframe_handling(df1,category,website_name,unique_column_name,domain_name,url_column_name,name_tag):
	df_clean = df1.reset_index(drop=True)
	df_clean = df_clean.drop_duplicates(subset = unique_column_name,keep='first')
	df_clean['PAGE_URL_COMPLETE'] = df_clean[url_column_name].apply(lambda x : domain_name + str(x))
	df_name = website_name  + '_' + name_tag + '_' + category + '.csv'  
	df_clean.to_csv('data_files/' + 'scraped_data/' + df_name)
	print(df_clean)
	return df_clean,df_name


class asos_products:
	## ASOS LINK FORMAT FOR REFERENCE 
	## https://www.asos.com/api/product/search/v2/categories/7616?channel=mobile-web&country=US&currency=USD&keyStoreDataversion=j42uv2x-26&lang=en-US&limit=100&offset=0&rowlength=2&sort=freshness&store=US
	num_of_results = 100 #if total number of products is less than this , there will be an error
	def __init__(self,category):
		self.category = category

	def scrape_new(self):
		with open('category_wise_links/asos_links.json') as f:
			asos_links = json.load(f)
		
		product_api_link_new = asos_links.get(self.category).replace('limit=100','limit={}'.format(self.num_of_results))
		response = requests.get(url=product_api_link_new, headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0'})
		data = response.json()
		product_list = data.get('products')
		new_dataframe	= pd.DataFrame.from_records(product_list) 
		for i in product_list:
			print(i)
			print('\n')

		print("\n\n\n----------------------------------------------------------------------------------------\n\n\n")

		new_dataframe = new_dataframe.reset_index(drop=True)

		return new_dataframe,'new'
			
	def scrape_popular(self):
		with open('category_wise_links/asos_links.json') as f:
			asos_links = json.load(f)
		product_api_link_popular = asos_links.get(self.category).replace('limit=100','limit={}'.format(self.num_of_results))
		product_api_link_popular = product_api_link_popular.replace('&sort=freshness','')
		print(product_api_link_popular)
		response = requests.get(url=product_api_link_popular, headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0'})
		data = response.json()
		product_list = data.get('products')
		popular_dataframe	= pd.DataFrame.from_records(product_list) 
		for i in product_list:
			print(i)
			print('\n')

		print("\n\n\n----------------------------------------------------------------------------------------\n\n\n")

		popular_dataframe = popular_dataframe.reset_index(drop=True)

		return popular_dataframe,'popular'
				

			

with open('category_wise_links/asos_links.json') as f:
	products = json.load(f)
product_names = products.keys()


for pname in product_names:
	print(pname)
	temp_asos_object = asos_products(pname)
	
	new_df,tag_new = temp_asos_object.scrape_new()
	popular_df,tag_popular = temp_asos_object.scrape_popular()
	
	final_new,_= dataframe_handling(df1 = new_df, category = pname, website_name = 'ASOS', unique_column_name = 'id', domain_name = 'www.asos.com/us', url_column_name = 'url' , name_tag = tag_new)
	print('\n\n\n\n')
	popular_new,_ = dataframe_handling(df1 = popular_df, category = pname, website_name = 'ASOS', unique_column_name = 'id', domain_name = 'www.asos.com/us', url_column_name = 'url' , name_tag = tag_popular)
	

print('finish')