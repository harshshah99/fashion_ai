import json
import pandas as pd
import requests

nord_headers = {
    'Host': "www.nordstrom.com",
    'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:74.0) Gecko/20100101 Firefox/74.0",
    'Accept': "*/*",
    'Accept-Language': "en-US,en;q=0.5",
    'Accept-Encoding': "gzip, deflate, br",
    'Content-Type': "application/json",
    'Country-Code': "US",
    'Currency-Code': "USD",
    'ExperimentId': "94f5239b-e996-40b7-bb61-1e1f73477d55",
    'IsUserEventQualified': "false",
    'NordApiVersion': "1.0",
    'UserAuthentication': "undefined",
    'UserId': "7f5aba7891044c62a9eb3f597e7de020",
    'UserQualificationType': "-1",
    'IncludeContent': "false",
    'IsMobile': "false",
    'nord-request-id': "0d9825ca-c258-4070-9232-6d4c93d5f22f",
    'Nord-SearchAPI-Version': "1",
    'CardMember': "Non-CardMember",
    'VisitorStatus': "New Customer",
    'LoyaltyLevel': "non-member",
    'nord-country-code': "US",
    'tracecontext': "91328fc9-8f7f-4c7c-9bf3-e9c3abd7997e",
    'identified-bot': "False",
    'experiments': """{"experiments":[{"n":"1ouj9","ns":"ns-99cap","v":"Default"},{"n":"OOSRecs","ns":"ns-zps1k","v":"Default"},{"n":"SSCancel","ns":"ns-e9fad","v":"SSCancel"},{"n":"Webp","ns":"ns-psr1c","v":"WebP"},{"n":"dxfjl","ns":"ns-i35lp","v":"QuickView"},{"n":"globalgrid1","ns":"ns-m4n62","v":"Default"},{"n":"k3k4j","ns":"ns-6gaoa","v":"Default"},{"n":"ln5wu","ns":"ns-by2mg","v":"Displayship"},{"n":"nb2k5","ns":"ns-a97b4","v":"ToggleColor"},{"n":"pw2hb","ns":"ns-i3fbb","v":"lessclicks"},{"n":"retry-card","ns":"ns-oyx47","v":"retry-card"},{"n":"w8zt4","ns":"ns-9w74q","v":"Default"},{"n":"ob0gi","ns":"ns-jflxa","v":"phase3"}],"user_id":"94f5239b-e996-40b7-bb61-1e1f73477d55"}""",
    'X-y8S6k3DB-f': "AzX8ynpzAQAAg8kxOWEsVkpQ7eT6I5dSU4UDpzEnkmPu-HH34RrHl-5HOmZrAXvJQ4ScuBAEwH8AADQwAAAAAA==",
    'X-y8S6k3DB-b': "-bcd9te",
    'X-y8S6k3DB-c': "AACsr3pzAQAAoYYwdldVsq3JfuuXCuZ-WR9zKbhOK9Ugg1VR2aTWLwHfngSe",
    'X-y8S6k3DB-d': "AAaihIjBDKGNgUGASZAQhISy1WKk1i8B354EniPT0RQSNP1UABREHDs8dm4T_XzZGaSoyCM",
    'X-y8S6k3DB-z': "q",
    'X-y8S6k3DB-a': "PC4RCUbk1BbkfuNoHoAy3eBZOFfWeXV3Xw5MW2_OfXUPo5LBZGJl5EVmm_T7CNoG=Zlde8sTTe3Dz53JjNE6SpraH4BdsIcm5nP1jrRMEeWxGDKU2a=w1HijFiwM-h2WWjMUozC5-7uYI27ZS21W5AyUfAKekanfHpsJKutx1Gmem14zDTnnTlSH3adlGG5rm4f7OG1S=ed7=K7juJOD4MCn4_=B_IM_69na1r1HHNMhn1YPQzXhN7d3q5sXWVSTuMD4=ia=ZBRt7MGP1m0OTUe2JVhOm7rSkibqQXcKSYMMQmSTOm1hED9aICJur8nMzCIzFpIS2UF_DssE1jik4bSu1UPazKWEG4G6zPD9h9yr5XybWCEkIF=QpPYlVtMXaKASlHOfxNls6fqok0ll96tlQT=Sli688wtJvrvQII3ALKmpFlPYAFvlabdYm7t9b46cGslxFtRAZH4ikPJCyzBVu=jrKA871sHsrML4otcW9MD=mbydXqz62q-FGvh3zu=Ee0VoDXM2HbnL8pYnS8lbtKOK-daYLK-T4cwDD95Dam_H3DsCOZ9EckMu3WWKdH6KKaFyEMcVijFxnJmdx4cpToFjCJDKUdOrYRhGI3T1h09FBTSvzDGrhYeP0S38Ixus=rEPHRPM9Yh8EwvrI8I36C2YVevOumVtQyOIXo5PZ6bjjcxPU7litnIcJFHf8pPXUhrSII5FhZmIAWROhTshMp4Es0FJUyrWc8HJrLZmG29wIdVxWONGWBXHetm-rr-Y_QyHAX5zBpuMlBve2_vi7_9lsMeLRhwtMDboWwbwTkILzVAIi4XP_vyi9Ik1ZVCrkF5UMD1H5TchYcP1kYwvEOndFpvWlGc5f9Iyf7IqwsC6Xmiw_mL8r_Us5ltrzVe4BsHxocmFMzWVMhU0f7_m66YA-bCHUR1PjldG5d5F4PG5vUNs5tos01neqlhOlssANDb1o2aIUlMcmDRP3eWC71ocAOJUarx7nEnticWfROIOfctlqEH5BlxX8XfDZX=jPkOTL_BPBQkAqWLGHK7558bkExrYdJQ2p00W_hfRhqsHvDlb_tGoSA2_7=ymoOKS1x6FbEPQfaOuTqzN8yECr9nqWN1i9QQCtx_FeRyF=YiIW0n1YYH1P-BOsw7eeI81MuUS7RWTzdjKdakD7OYUDaQK3EP0nptbtiGNOocEt1u_okSFKv5HqfB8VxowmDM75lIOAB-Yx3hQGA2syySb43lvBNsOF-bh-9EMecljv8lUxCa4Mln5wurqMj-0lAvdmT7=y8947_RKJDb3WH_y9=I-hqXa652kKFkXGx7W2p=fK-NGEVn3fzpFUvjSZxixI-kRcp0kjAeJHQxsdV=87sWnbIWiG2qwW2PPm6bKVdTk61cUakzflTReoJT5vm25RSod9usdFcjm3COn0exN33Pab_Z3qlN9S5tu=jSPmJTGXB6DURlQNcmsdRQ1wsnEiyWwrlzll3KozN=R9LhfZk8ZvnoMqK3ARSIi=LAsVNiWFcMZ1-JSsizUhwGIjHUd8n9DnYJdy0ZVhMCX-7mMuRJPi83280cMB2Ef-rrsYR1BL4-65h1iTkai_481yQ8Dsuo6KRkN5P-2djKZysot4Sw5kfLq=TyH1djvasfkh4Ic6s6x1sxKz=MYxkk6Jca2H9EjcMS7TSXXCS-o45zhOEDHaUuQJ97TOYk_5rzuRbrxxvqUItjyB5h8KE2eh9o9ib0bfwZs4LynN_M6wN1WX0O4iFqG0eQG1nYxKDEzmMXX6CjJfnn4v4Aljh-nztmFm4WOFxSsA3P1AxnmI9dS5_jSA7WGR=vwh7JLcjVbB3YPDMsI6zYZAXKiwdAm=EMeAAPh0v9A4Dzvpd4LTn3KswqypJ2AtkB3O8YSNiKY-A9POfRr9Jh3pobpB2inVpebCvLhwuvp0X4aluMfxzl1W8SJvJ7-UIEX7oWLkSBwnnPFqEjvi9wcS5Li2at=FfAGJZ3QZc6lszJo=Z-eUDVWKHd2zvN6YtuiUu71SB7ky4PxIac2973oI85m_h_RiNscrWMTErREY1vrpMnV4Is2biQjp7B2ac2byBNDFrOFT4h8TZxz9BPTL54_bQJqIxnJl6AJqpe6GsCa4=AQb4DhutYtbYe95wUexVJ9UIGR8mZtHLEOP679iNlvA_t_4TRE7h051BaDZxcqJ2RiRE1TQnxXL60XNzrqSMM5EXIq_5NzFZIBm-dqHdxR0Kc23Xdo8DO-l5XxHuCQpFYJFWdaBrJesDd-lTGmBu-1mP4u4Hj8hC8HN3IJN56eFAwVTWD2VuMZW2PKOpyq6_u6AvadkF__ts8z3Y5MSn1eTtL2WEdUfsYCqYPTxeG9qck8xoj_n3rlOb0iwukOkFTavO8stFVuNiON0F1TCehzrly_uNk6qZHzI5YoJI08q9YCqcrSv4Ti3ejeesbksnC4728KqGMOPkwMXKs3TId5bByQEi2kHzCSh=oT4LX3TODwhct5Y0MKeWJw2QiRClZDDOZEOIVY2_i=et8k=xPabtYjXG=83VsvtPDwu=Ltdifye6NXdk4vdWcFzZ3WBZ2Hn4lNFLw5dvwq8Eywp96iqadWM=_aEUSEtHw1COZbODm_1F6OloyTsZTMyDmRb9tBE_QSTamCvL1yWxhcrp6BiKsRuEf9V8dMUMbLIIV_8N6RVif3L6f-fhCTsznuRnJ5YDj1SC_QiKLO=Xsilzbs5PzkdvSyzPBpabKzRj-hv7Z7MHYJMF9HSyCEbAIGyTyVK6UspmyWR95jVFnkRDhduycvJvYh-tJl7HIWZbiOvLuXWarKDEflCv9f_zU2ahVj_XzRwvfTta3-ANXBZYfG0TMTCUbf2cXFOunLGLhe-yMEZ9=OWV4uIZYs8xnnWFbBGFaf4dCliiXGxsYopUfse35saWTo1AvGNkxWBH03_JmJ9TEjyx6=MF=CD0_6QyB9M0=4YkRDtpNmGj6oXYYD0YLrfvR2U4GTOBlhhwh_530ChdAKi=sILGTCpH5KacYnPGEq=U5iVdowCWnqc9ZReWvlLece-xCXGT46G-qab-0Ip7RQiKiAazuZx-25Q5kOPy__xp7Lx-l0bh1tIBIwc2k6eS0Sy1GvXlpQvuhWeM7iNfeCX6JeAAddJu1Q_DlkWzzlhqX2vxWRhc-kebvvmErqfx4PEbUzW8m_8kIXxY-9QsMCwtocouztBST0uM0RDtsZaY=YK16Bks2UPihdPchoGPM8t71NboZV=wkrpet9ld9iaUfTRlQevCZ0IsGoHeaPRj2eVsfoYRaB4xlH-lvitEB8Asf6c0Et6Z7P5aJVGZKFWatLnTbXD2T2co189xQ338MeIx6IxLfIm8c9Yk-xeHL-4wMz8GC63euiWLdUp=_Xsx-u3PFAENXwXW=h0qKkf_XG7hJFLd7HY13-ym1It_dPnmLX=kLvMcsOmB-1ZaG5FFms5hBBq4oRr-11Ci5uedkUy=5Q4QOv9-tBTBdwqwNGkfzK9bJLfovqeN6XycB978ZeHhtBwF=BjoPO0CFrttQFdW1XXYmRZzXPe-cc79ViT2L5ls7Y8Rkp84P-WUblctTpRy-HcLyBmY7aA7EXY5ZUuYXa3ohOrcp7BwCvPVmjGYYmb8losF-m1O=rcHQkxQCQm9sa0-mQsVu-XAN0pizJOuk7JAB1f=r19sWZVyJ28GPBuuXCOexmyRnutDAHHmd=3uxxyFVBtrxQ=TQlFHXpwVza3pufJbvHdfOoEm-9q4EoENoJLBAGcEb9wpAp=mkbaJTMNCaGGlqJEzQe6Bj_6jaqfS0RjLjM9SEp",
    'Connection': "keep-alive",
    'Cookie': "Ad34bsY56=AINWuQlzAQAAbt9X6O8-vsDizAntLFlG3v8denAg-BhFhE6cQx8rH6wtRYlA|1|1|75bc52c6dd91d9103f98a0a8717aab40cbc40433; GeoLocationZipCode=undefined; internationalshippref=preferredcountry=US&preferredcurrency=USD&preferredcountryname=United%20States; no-track=ccpa=false; nordstrom=bagcount=0&firstname=&ispinned=False&isSocial=False&shopperattr=||0|False|-1&shopperid=7f5aba7891044c62a9eb3f597e7de020&USERNAME=; nui=firstVisit=2020-07-01T09%3A33%3A29.111Z&geoLocation=&isModified=false&lme=false; shoppertoken=shopperToken=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3ZjVhYmE3ODkxMDQ0YzYyYTllYjNmNTk3ZTdkZTAyMCIsImF1ZCI6Imd1ZXN0IiwiaXNzIjoibm9yZHN0cm9tLWd1ZXN0LWF1dGgiLCJleHAiOjE5MDkxMjg4MDksInJlZnJlc2giOjE1OTM2MTA0MDksImp0aSI6IjQ1ZjMxNTA1LTM3YWQtNDdhYi1iMTE4LTU2MWI5MjI1Y2IzZCIsImlhdCI6MTU5MzU5NjAwOX0.gPIkU6p3zbXLdu8UWHZDObXmevm6VuxfWLijpxcekWfZhNlPjBA-DLYxayqxFIIZiSa1NXUoS0XQPm92OOf4Mc62Ro9GvzMsOd9aslaKOOCPqtX5O-J5imZhR69kiF7X9P7sAusHM2lkXVX3eLlpPkHmMI4vJYmc--og0LQ61-WlFSKAmlX1BX2nE-EdD-MTQTsP2-8CuFFEe_Qg3F5UnItaGNmGNkMwvhrprfgDvBpY9uunCvcjFP5D8XlWXDhjmDGsyOo7xW36dSAWB4wcbhlH1Nmz4iqWaDU12dSpLdlSknCvh9VPG_lh8GObYmI4u2SrSXRweIgvefnO9OIPJQ; experiments=ExperimentId=94f5239b-e996-40b7-bb61-1e1f73477d55; forterToken=761bfccfe1e340128355a278f4877f2f_1595492989703__UDF43_6; _gcl_au=1.1.1283531583.1593596010; _ga=GA1.1.607543142.1593596011; _ga_XWLT9WQ1YB=GS1.1.1595492990.11.1.1595493033.0; rkglsid=h-744534289e8add047fe1010017309b96_t-1595493034; storemode=postalCode=&selectedStoreIds=&storesById=&localMarketId=&localMarketsById=; storeprefs=|100|||2020-07-23T08:29:50.734Z; ftr_ncd=6; _sp_id.c229=94f5239b-e996-40b7-bb61-1e1f73477d55.1593596012100.9.1593596012100.1593596012100.c15ff1d5-4212-493f-bb37-592428858954; _fbp=fb.1.1593596015553.1949864893; client=viewport=2_SMALL; shopping-bag-migration=shopperId=7f5aba7891044c62a9eb3f597e7de020&isMigrated=true; Bd34bsY56=AJ-uy3pzAQAASVpJOLFdFbG1Q9NdNXJv8Cap0embD3E3rjvWhfgRLdFBo0Jv; _pin_unauth=dWlkPVpHSXdNak0wWWpNdFpqaGlOQzAwWldZMkxUazJOMll0T0RSaFlXVXdPR1UwWVRBeQ; rfx-forex-rate=currencyCode=USD&exchangeRate=1&quoteId=0; session=FILTERSTATE=&RESULTBACK=&RETURNURL=http%3A%2F%2Fshop.nordstrom.com&SEARCHRETURNURL=http%3A%2F%2Fshop.nordstrom.com&FLSEmployeeNumber=&FLSRegisterNumber=&FLSStoreNumber=&FLSPOSType=&gctoken=&CookieDomain=&IsStoreModeActive=0; usersession=CookieDomain=nordstrom.com&SessionId=10468a5c-6751-4711-90c0-4ccc4d50edd9; _4c_mc_=f2893906-ef44-49c7-97c7-83c0de83ac40; buynow=isRegistered=true&isQualified=false; minibag=MiniBagHash=1595492992369; _sp_ses.c229=*; Ad34bsY56_dc=%7B%22c%22%3A%20%22enM0MDVVekNGY2VLVTFZeQ%3D%3DChgEWGCRCb0whUCjMW1oBFiHYwlQXbrPDnsGf_X8Y-tuMv739rsBnCflDdwEy1cdHcfV3cILU5CLgImatcc5VFHmH0SPaA%3D%3D%22%2C%20%22dc%22%3A%200%2C%20%22mf%22%3A%200%7D; _gid=GA1.2.882073062.1595492994; _gat_UA-107105548-1=1; _uetsid=a5dea527a8db92fee8ce958a100446a8; _uetvid=63697fb958606a9ba3c9b84cd3e27301",
    'TE': "Trailers",
    'cache-control': "no-cache",
    'Postman-Token': "2047ca0b-b7c6-4c64-b927-7f7a5de80566"
    }

def dataframe_handling(df1,category,website_name,unique_column_name,domain_name,url_column_name,name_tag):
	df_clean = df1.reset_index(drop=True)
	df_clean = df_clean.drop_duplicates(unique_column_name,keep='first')
	df_clean['PAGE_URL_COMPLETE'] = df_clean[url_column_name].apply(lambda x : domain_name + str(x))
	df_name = name_tag + '_' + website_name + '_' + category + '.csv'
	df_clean.to_csv(website_name + '/' + df_name)
	print(df_clean)
	return df_clean,df_name


class nordstrom_products:
	# https://www.nordstrom.com/api/browse/query/browse/men/clothing/tshirts?top=100&breadcrumb=Home%2FMen%2FClothing%2FT-Shirts %26 Tank Tops&origin=topnav&sort=Newest&offset=0 100 tshirts NEWEST

	num_of_results = 100 #Not used anywhere, just for reference 

	def __init__(self,category):
		self.category = category

	def scrape_new(self):
		with open('nordstrom_links.json') as f:
			nordstrom_links = json.load(f)
		
		product_api_link_new = nordstrom_links.get(self.category)
		response = requests.get(url=product_api_link_new, headers = nord_headers)
		data = response.json()
		product_list = data.get('productsById')
		new_dataframe	= pd.DataFrame.from_records(product_list).transpose() 
		for i in product_list:
			print(i)
			print('\n')

			print("\n\n\n----------------------------------------------------------------------------------------\n\n\n")

		new_dataframe = new_dataframe.reset_index(drop=True)

		return new_dataframe,'new'
			
	def scrape_popular(self):
		with open('nordstrom_links.json') as f:
			nordstrom_links = json.load(f)
		product_api_link_popular = nordstrom_links.get(self.category)
		product_api_link_popular = product_api_link_popular.replace('&sort=Newest','')
		print(product_api_link_popular)
		
		response = requests.get(url=product_api_link_popular, headers =nord_headers)
		data = response.json()
		product_list = data.get('productsById')
		popular_dataframe	= pd.DataFrame.from_records(product_list).transpose()	
		for i in product_list:
			print(i)
			print('\n')

			print("\n\n\n----------------------------------------------------------------------------------------\n\n\n")

		popular_dataframe = popular_dataframe.reset_index(drop=True)

		return popular_dataframe,'popular'
				

with open('nordstrom_links.json') as f:
	products = json.load(f)

product_names = products.keys()


for pname in product_names:
	print(pname)
	temp_nordstrom_object = nordstrom_products(pname)
	
	new_df,tag_new = temp_nordstrom_object.scrape_new()
	popular_df, tag_popular = temp_nordstrom_object.scrape_popular()

	final_new,_ = dataframe_handling(df1 = new_df, category= pname, website_name= 'NORDSTROM', unique_column_name = 'id', domain_name = 'www.nordstrom.com', url_column_name = 'productPageUrl', name_tag = tag_new)
	final_popular,_ = dataframe_handling(df1 = popular_df, category= pname, website_name= 'NORDSTROM', unique_column_name = 'id', domain_name = 'www.nordstrom.com', url_column_name = 'productPageUrl', name_tag = tag_popular)