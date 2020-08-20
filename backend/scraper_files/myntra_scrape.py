"""
myntra_scrape.py

CLass myntra_products(category) - Contains scrape_new() and scrape_popular() which scrape NEW and POPULAR products  of given 'category'
dataframe_handling() - Cleans scraped Data and Stores them in 'data_files/scraped_data/' with PROPER NAMING FORMAT
"""



import requests
import json
import pandas as pd

##LOAD MYNTRA links into a variable used for scraping

def dataframe_handling(df1,category,website_name,unique_column_name,domain_name,url_column_name,name_tag):
	"""
	Parameters : 
	df1 : Datframe of SCraped Products to clean and save
	category : vertical name ie. men_tshirts or women_jumpsuits - USED to name the file while saving
	website_name : Name of website in CAPITAL. eg . MYNTRA or KOOVS - USED to name the file while saving
	unique_column_name : Every dataframe has a unique_column_name which can be used to find duplicate rows and hence drop these rows  to avoid duplicate products in the dataset 
	domain_name : Every site has a domain name like 'www.myntra.com/' or 'www.koovs.com'
	url_column_name : Every dataframe will have a column which stores the PARTIAL URL of the product's page on the Website. domain_name + Entry in url_column_name = Entry in column name
		eg : 'www.myntra.com/'[domain_name] + 'Tshirts/HM/-HM-Men-Black-Solid-Cotton-T-shirt/12125410/buy'[a specific row from url_column_name in this case landingPageUrl]
	name_tag : 'new' or 'popular' to name the file while saving 



	EVERY product on an ecommerce webite has a few attributes common like :  an id which is unique for each product, a key which contains the URL for the said product, the domain name and so on.
	This function takes in a datframe of products scraped from Website and does the following:
		1)resets the index ie. creates a new index say from 0 to 99 for 100 scraped products
		2)df_clean.drop_duplicates(subset = unique_column_name,keep='first') - This drops duplicate rows.
			For every website, since the product_id or a similar column which contains unique value for eah product is used to drop any duplicate entries in our scraped data.
		3) Websites usuallly store only the partial link to a product page. In this case the column "landingPageUrl" contains string like : 'Tshirts/HM/-HM-Men-Black-Solid-Cotton-T-shirt/12125410/buy' while  the actual link for this product will be 'www.myntra.com/Tshirts/HM/-HM-Men-Black-Solid-Cotton-T-shirt/12125410/buy'
		df_clean['PAGE_URL_COMPLETE'] = df_clean[url_column_name].apply(lambda x : domain_name + str(x))
		This creates a column called PAGE_URL_COMPLETE which  appends the landingPageUrl to 'www.myntra.com/'(domain_name).
		4) df_name = website_name  + '_' + name_tag + '_' + category + '.csv' - NAME ALL SCRAPED DATAFILES IN SPECIFIC FORMAT
			{WEBSITE-NAME}_{NAME-TAG}_{CATEGORY}.csv
			WEBSITE-NAME : MYNTRA,KOOVS,ASOS, etc
			NAME-TAG : 'new' or 'popular'
			CATEGORY : 'men_tshirts' , 'men_casual_shirts', 'women_jumpsuits' and so on 
	"""
	df_clean = df1.reset_index(drop=True)
	df_clean = df_clean.drop_duplicates(subset = unique_column_name,keep='first')
	df_clean['PAGE_URL_COMPLETE'] = df_clean[url_column_name].apply(lambda x : domain_name + str(x))
	df_name = website_name  + '_' + name_tag + '_' + category + '.csv'  
	df_clean.to_csv('data_files/' + 'scraped_data/' + df_name)
	print(df_clean)
	return df_clean,df_name


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
	page_list = [('&o=' + str(max(0,100*j - 1))) for j in range(0,int(num_of_results/100))] #changes '&o=0' to '&o=99' in URL string accroding to given num_of_results 
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
			product_api_link_new.append(product_api_link_new[0].replace('&o=0',i)) #for every string in page_list, this loop modifies the base link (https://www.myntra.com/web/v2/search/men-tshirts?p=1&sort=new&rows=100&o=0) to include results from other pages (https://www.myntra.com/web/v2/search/men-tshirts?p=1&sort=new&rows=100&o=99)
		new_dataframe = pd.DataFrame() #initializes empty dataframe
		for page_link in product_api_link_new[1:]: #goes through all generated links for given number of results
			response = requests.get(url=page_link, headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0'})
			data = response.json() #gets the JSON response from API request above
			product_list = data.get('products') #in the JSON scraped from Myntra API , all the products on that page are stored in the key 'products'
			new_dataframe	= new_dataframe.append(pd.DataFrame.from_records(product_list)) #convert list of JSON to dataframe using pandas.DataFrame.from_records()
			for i in product_list:
				print(i)
				#output the scraped product in terminal

			print("\n\n\n----------------------------------------------------------------------------------------\n\n\n") 

		new_dataframe = new_dataframe.reset_index(drop=True)
		#print(new_dataframe)
		return new_dataframe,'new'
			
	def scrape_popular(self):
		"""
		Logic for extracting products from Myntra API is same as above funvtion "scrape_new()"
		To get New products the link is : https://www.myntra.com/web/v2/search/men-tshirts?p=1&sort=new&rows=100&o=0 - MEANS first 100 products
		To get Popular ptoducts the link is : https://www.myntra.com/web/v2/search/men-tshirts?p=1&sort=popularity&rows=100&o=0 - MEANS first 100 "POPULAR" products
		this code below ------> product_api_link_popular[0] = product_api_link_popular[0].replace('sort=new','sort=popularity') replaces 'new' with 'popularity' int the URL which allows us to scrape POPULAR products instead of NEW
		returns a dataframe containing scraped data	of that given category, in this case a dataframe containing 100 MOST POPULAR men_tshirts from Myntra
		"""
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
				

			

with open('category_wise_links/myntra_links.json') as f: #get all VERTICALS and their corresponsing URL which we will use to scrape from myntra_links.json in folder 'category_wise_links'
	products = json.load(f)
product_names = products.keys() #contains vertical names like men_tshirts and women_jumpsuits as seen in myntra_links.json file


for pname in product_names: #This loop goes thorugh each vertical present in myntra_links.json ie. first  men_tshirts, them men_casual_shirts and so on.....
	print(pname)
	temp_myntra_object = myntra_products(pname) #creates a myntra_products obeject  of category=pname(for ek for first iteration a myntra_products('men_tshirts') will be created,then myntra_products('men_casual_shirts') and so on for all verticals)
	
	new_df,tag_new = temp_myntra_object.scrape_new() #calls scrape_new() from above created object, returns dataframe containing 100 of the latest products of given category(pname) as listed on MYNTRA
	popular_df,tag_popular = temp_myntra_object.scrape_popular() # like scrape new, scrape_popular() returns dataframe containing 100 of the MOST POPULAR products of given category(pname) as listed on MYNTRA
	
	final_new,_= dataframe_handling(df1 = new_df, category = pname, website_name = 'MYNTRA', unique_column_name = 'productId', domain_name = 'www.myntra.com/', url_column_name = 'landingPageUrl' , name_tag = tag_new)
	#Above statement call dataframe_handling on new_df, ie. it cleans and stores all new products for given category/vertical in a CSV with appropriate naming : for eg. NEW Men's Tshirts on Myntra will be saved in "data_files/scraped_data/MYNTRA_new_men_tshirts.csv"
	print('\n\n\n\n')
	popular_new,_ = dataframe_handling(df1 = popular_df, category = pname, website_name = 'MYNTRA', unique_column_name = 'productId', domain_name = 'www.myntra.com/', url_column_name = 'landingPageUrl' , name_tag = tag_popular)
	#Above statement call dataframe_handling on popular_df, ie. it cleans and stores all popular products for given category/vertical in a CSV with appropriate naming : for eg. POPULAR Men's Tshirts on Myntra will be saved in "data_files/scraped_data/MYNTRA_popular_men_tshirts.csv"

print('finish') #IF THE CODE PRINTS FINISH WITHOUT ANY ERROR MEANS IT RAN SUCCESFULLY