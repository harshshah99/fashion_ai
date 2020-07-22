import json
import pandas as pd
import requests


def dataframe_handling(df1,category,website_name,unique_column_name,domain_name,url_column_name,name_tag):
	df_clean = df1.reset_index(drop=True)
	df_clean = df_clean.drop_duplicates(unique_column_name,keep='first')
	df_clean['PAGE_URL_COMPLETE'] = df_clean[url_column_name].apply(lambda x : domain_name + str(x))
	df_name = name_tag + '_' + website_name + '_' + category + '.csv'  
	df_clean.to_csv(website_name + '/' + df_name)
	print(df_clean)
	return df_clean,df_name


class ajiotrends_products:
	# https://www.ajio.com/api/category/830216014?fields=SITE&currentPage=0&pageSize=100&format=json&query=%3Anewn&sortBy=newn&gridColumns=3&facets=&advfilter=true PAGE 1 - 100 items
	# https://www.ajio.com/api/category/830216014?fields=SITE&currentPage=1&pageSize=100&format=json&query=%3Anewn&sortBy=newn&gridColumns=3&facets=&advfilter=true PAGE 2 - 100 items

	num_of_results = 200 #Don't exceed 200 since unavaliablity of more products might cause issues
	page_list = ['currentPage=' + str(i) for i in range(0,int(num_of_results/100))]
	
	def __init__(self,category):
		self.category = category

	def scrape_new(self):
		with open('ajiotrends_links.json') as f:
			ajiotrends_links = json.load(f)
		product_api_link_new = [ajiotrends_links.get(self.category)]
		for i in self.page_list:
			product_api_link_new.append(product_api_link_new[0].replace('currentPage=0',i))
		new_dataframe = pd.DataFrame()
		for page_link in product_api_link_new[1:]:
			response = requests.get(url=page_link, headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0'})
			data = response.json()
			product_list = data.get('products')
			new_dataframe	= new_dataframe.append(pd.DataFrame.from_records(product_list)) 
			for i in product_list:
				print(i)
				print('\n')

			print("\n\n\n----------------------------------------------------------------------------------------\n\n\n")

		new_dataframe = new_dataframe.reset_index(drop=True)

		return new_dataframe,'new'
			
	def scrape_popular(self):
		with open('ajiotrends_links.json') as f:
			ajiotrends_links = json.load(f)
		product_api_link_popular = [ajiotrends_links.get(self.category)]
		product_api_link_popular[0] = product_api_link_popular[0].replace('sortBy=newn','sortBy=relevance')
		for i in self.page_list:
			product_api_link_popular.append(product_api_link_popular[0].replace('currentPage=0',i))
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

		return popular_dataframe,'popular'
				

with open('ajiotrends_links.json') as f:
	products = json.load(f)
product_names = products.keys()


for pname in product_names:
	print(pname)
	temp_ajio_object = ajiotrends_products(pname)
	
	new_df,tag_new = temp_ajio_object.scrape_new()
	popular_df, tag_popular = temp_ajio_object.scrape_popular()

	final_new,_ = dataframe_handling(df1 = new_df, category= pname, website_name= 'AJIO_TRENDS', unique_column_name = 'code', domain_name = 'trends.ajio.com', url_column_name = 'url', name_tag = tag_new)
	final_popular,_ = dataframe_handling(df1 = popular_df, category= pname, website_name= 'AJIO_TRENDS', unique_column_name = 'code', domain_name = 'trends.ajio.com', url_column_name = 'url', name_tag = tag_popular)