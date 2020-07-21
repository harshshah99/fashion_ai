import requests
import json
import pandas as pd

##LOAD MYNTRA links into a variable used for scraping

class myntra_products:
	## MYNTRA LINK FORMAT FOR REFERENCE 
	## https://www.myntra.com/web/v2/search/men-tshirts?p=1&sort=new&rows=100&o=0 - MEANS first 100 products
	## https://www.myntra.com/web/v2/search/men-tshirts?p=1&sort=new&rows=100&o=99 - MEANS next 100 products

	num_of_results = 100
	page_list = [('&o=' + str(max(0,100*j - 1))) for j in range(0,int(num_of_results/100))]
	def __init__(self,category):
		self.category = category

	def scrape_new(self):
		with open('myntra_links.json') as f:
			myntra_links = json.load(f)
		product_api_link_popular = [myntra_links.get(self.category)]
		for i in self.page_list:
			product_api_link_popular.append(product_api_link_popular[0].replace('&o=0',i))
		new_dataframe = pd.DataFrame()
		for page_link in product_api_link_popular[1:]:
			response = requests.get(url=page_link, headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0'})
			data = response.json()
			product_list = data.get('products')
			new_dataframe	= new_dataframe.append(pd.DataFrame.from_records(product_list)) 
			for i in product_list:
				print(i)
				print('\n')

			print("\n\n\n----------------------------------------------------------------------------------------\n\n\n")

		new_dataframe = new_dataframe.reset_index(drop=True)

		return new_dataframe
			
	def scrape_popular(self):
		with open('myntra_links.json') as f:
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

		return popular_dataframe
				

			

with open('myntra_links.json') as f:
	products = json.load(f)
product_names = products.keys()


for pname in product_names:
	print(pname)
	temp_myntra_object = myntra_products(pname)
	
	new_df = temp_myntra_object.scrape_new()
	popular_df = temp_myntra_object.scrape_popular()
	
	new_csv_name = 'NEW_MYNTRA_' + pname+'.csv'
	popular_csv_name = 'POP_MYNTRA_' + pname+'.csv'

	final_df_new = new_df.drop_duplicates('productId',keep='first')
	final_df_popular = popular_df.drop_duplicates('productId',keep='first')

	final_df_new['PAGE_URL_COMPLETE'] = final_df_new['landingPageUrl'].apply(lambda x : 'www.myntra.com/' + str(x))
	final_df_popular['PAGE_URL_COMPLETE'] = final_df_popular['landingPageUrl'].apply(lambda x : 'www.myntra.com/' + str(x))

	final_df_new.to_csv('MYNTRA_DATA/'+ new_csv_name)
	final_df_popular.to_csv('MYNTRA_DATA/'+ popular_csv_name)


print('finish')