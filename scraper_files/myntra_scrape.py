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


## MYNTRA LINK FORMAT FOR REFERENCE 
## https://www.myntra.com/web/v2/search/men-tshirts?p=1&sort=new&rows=100&o=0 - MEANS first 100 products
## https://www.myntra.com/web/v2/search/men-tshirts?p=1&sort=new&rows=100&o=99 - MEANS next 100 products


class myntra_products:
	"""
	Initializes by taking in a category eg. men_tshirts
	num_of_results contains how many number of products you want to scrape (default 100)
	page_list - This contains logic for creating a link in case more than 100 products are to be scraped
	ie. 	https://www.myntra.com/web/v2/search/men-tshirts?p=1&sort=new&rows=100&o=0 - MEANS first 100 products
			https://www.myntra.com/web/v2/search/men-tshirts?p=1&sort=new&rows=100&o=99 - MEANS 100-200 products
			https://www.myntra.com/web/v2/search/men-tshirts?p=1&sort=new&rows=100&o=199 - MEANS 200-300 products
	to generate links as given above, page_list creates a list of substrings to be added after base_link 
	scrape_new() - scrapes NEW products for given category , in this case men_tshirts 
	scrape_popular() - scrapes POPULAR products for given category, in this case men_tshirts
	"""
	num_of_results = 100
	page_list = [('&o=' + str(max(0,100*j - 1))) for j in range(0,int(num_of_results/100))] #changes link parameters and  generates URL according to num_of_results
	#notice how first 100 products(https://www.myntra.com/web/v2/search/men-tshirts?p=1&sort=new&rows=100&o=0) and next 100 products(https://www.myntra.com/web/v2/search/men-tshirts?p=1&sort=new&rows=100&o=99) differ only in "&o=0" and "&o=99"
	def __init__(self,category):  #class initializes using a given category
		self.category = category

	def scrape_new(self):
		"""
		Scrapes latest num_of_results products of given category, in this case 100 of the latest men_tshirts as listend on Myntra
		returns a dataframe containing scraped data	of that given category, in this case a dataframe containing 100 latest men_tshirts from Myntra
		"""
		with open('category_wise_links/myntra_links.json') as f: #myntra_links.json contains key-value pairs of format 'category' : 'category_link' .ie {'men_tshirts': 'https://www.myntra.com/web/v2/search/men-tshirts?p=1&sort=new&rows=100&o=0', 'men_casual_shirts':.............}
			myntra_links = json.load(f)
		product_api_link_new = [myntra_links.get(self.category)] 
		for i in self.page_list:
			product_api_link_new.append(product_api_link_new[0].replace('&o=0',i)) #for every string in page_list, this loop modifies the base link (https://www.myntra.com/web/v2/search/men-tshirts?p=1&sort=new&rows=100&o=0) to include results from other pages https://www.myntra.com/web/v2/search/men-tshirts?p=1&sort=new&rows=100&o=99
		new_dataframe = pd.DataFrame() #initializes empty dataframe
		for page_link in product_api_link_new[1:]: #goes through all generated links for given number of results
			response = requests.get(url=page_link, headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0'})
			data = response.json()
			product_list = data.get('products')
			new_dataframe	= new_dataframe.append(pd.DataFrame.from_records(product_list)) 
			for i in product_list:
				print(i)
				print('\n')

			print("\n\n\n----------------------------------------------------------------------------------------\n\n\n")

		new_dataframe = new_dataframe.reset_index(drop=True)
		#print(new_dataframe)
		return new_dataframe,'new'
			
	def scrape_popular(self):
		with open('category_wise_links/myntra_links.json') as f:
			myntra_links = json.load(f)
		product_api_link_popular = [myntra_links.get(self.category)]
		product_api_link_popular[0] = product_api_link_popular[0].replace('sort=new','sort=popularity')
		for i in self.page_list:
			product_api_link_popular.append(product_api_link_popular[0].replace('&o=0',i))
		popular_dataframe = pd.DataFrame()
		print(product_api_link_popular)
		for page_link in product_api_link_popular[1:]:
			response = requests.get(url=page_link, headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0'})
			data = response.json()
			product_list = data.get('products')
			popular_dataframe	= popular_dataframe.append(pd.DataFrame.from_records(product_list)) 
			for i in product_list:
				print(i)
				print('\n')

			print("\n\n\n----------------------------------------------------------------------------------------\n\n\n")

		popular_dataframe = popular_dataframe.reset_index(drop=True)
		#print(popular_dataframe)
		return popular_dataframe,'popular'
				

			

with open('category_wise_links/myntra_links.json') as f:
	products = json.load(f)
product_names = products.keys()


for pname in product_names:
	print(pname)
	temp_myntra_object = myntra_products(pname)
	
	new_df,tag_new = temp_myntra_object.scrape_new()
	popular_df,tag_popular = temp_myntra_object.scrape_popular()
	
	final_new,_= dataframe_handling(df1 = new_df, category = pname, website_name = 'MYNTRA', unique_column_name = 'productId', domain_name = 'www.myntra.com/', url_column_name = 'landingPageUrl' , name_tag = tag_new)
	print('\n\n\n\n')
	popular_new,_ = dataframe_handling(df1 = popular_df, category = pname, website_name = 'MYNTRA', unique_column_name = 'productId', domain_name = 'www.myntra.com/', url_column_name = 'landingPageUrl' , name_tag = tag_popular)
	

print('finish')