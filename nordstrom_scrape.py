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
    'nord-request-id': "aa135ac7-b2bd-4a46-bc33-d0ab7cca3f7e",
    'Nord-SearchAPI-Version': "1",
    'CardMember': "Non-CardMember",
    'VisitorStatus': "New Customer",
    'LoyaltyLevel': "non-member",
    'feature-flags': "isanniversarypreviewenabled",
    'nord-country-code': "US",
    'tracecontext': "e553b28f-ab27-4220-9e16-211372502ac7",
    'identified-bot': "False",
    'experiments': '{"experiments":[{"n":"OOSRecs","ns":"ns-zps1k","v":"Default"},{"n":"SSCancel","ns":"ns-e9fad","v":"SSCancel"},{"n":"Webp","ns":"ns-psr1c","v":"WebP"},{"n":"globalgrid1","ns":"ns-m4n62","v":"Default"},{"n":"ic1ss","ns":"ns-wxskw","v":"Default"},{"n":"nb2k5","ns":"ns-a97b4","v":"ToggleColor"},{"n":"retry-card","ns":"ns-oyx47","v":"retry-card"},{"n":"ob0gi","ns":"ns-jflxa","v":"phase3"}],"user_id":"94f5239b-e996-40b7-bb61-1e1f73477d55"}',
    'X-y8S6k3DB-f': "A9oIFINzAQAAoKk7hj5_opA3TjAX1UfbZEaEIl3jaTpeM8b-kwCNj2U5KhSDAXvJQ1WcuBAEwH8AADQwAAAAAA==",
    'X-y8S6k3DB-b': "yvdhjs",
    'X-y8S6k3DB-c': "AIABDoNzAQAAolAaKOvpdfXHEVxxqAZRT_aISWt7oq4OI8X6azoGoTCe9dg6",
    'X-y8S6k3DB-d': "AAaihIjBDKGNgUGASZAQhISy1WI6BqEwnvXYOiPT0RQSNP1	UAAWYJjbyOzC8E0qpO_px2vw",
    'X-y8S6k3DB-z': "q",
    'X-y8S6k3DB-a': "Ch-1NUOM_96gi6lopgmbghCDpf1gxZULTzDleeJkn3zt-g5fa3tCoLy0fwGoV577rVuodBExcZvaAfspsw6CLg0oM7=I1hKIH67Fyriasb2uB=S3f3SBbZn6rzSU5kojGgKG-=SWNz90l_vTGni0YkC9UJk_ejLQ=X2LzR9VCo8AZHMEq8DEGzBKrpw200dHDSgBDBloXrV5dXidt3NlYTxowFIucT1exXn0y9Z9HbFNZW83RklYvRNn_BbL1hjzeY1R1xnyHA5Thzvp=sUHStWQvxC6QJtCR1jPE_RPye9U2mFCoxAokXl9O1fH7pRgPOzW1xIJ0ez5YpBx1Q9j3CuF3M9BChSNJjetrKSZkUL3nHheteZ8s85vlnQjPMQ00z7cCpfgtlBzmw5di-du56NcXNJHM8tAv2rM2a0=fHQUW9km1NJNa-ZA_DfJlGVhBNj-9FHfytqrz7XRg-CQ=NErJx3IssO6x6=tn0LYs02WL_9rImReBXHwrPSH-QJUZqqnkA_vvHQQY_pjzj9b0z18PjobJBN1BOEL2f2FPb5AOgI5ITFT9Dhsq5-UmNSs7=YdpVBiB9kmXpP_RBkdFJn0IBd_wpXnM9zN-kaoZi2LN8vXBQvkEppR6z5Um_HZNRCg-Del-iAJI_qO7__=jL_BB-aIav5yyCcITbwszog76JAEqDGr9=bgKCGOF9VO=-1XVjN2T1E2KxzjjflTPuGjq3YVWT8L67Q0JZdURvBR=A1m5QnI8pDYIZSnnEGNynjcswPerQna3oS3WNqdym52sRYnHjOZFIR5FwvUqSENq0iudCHB3stIOICJVU2pDsDT8bI1ir8eHHYwobFoDiqG=SNk_s3T9c36CyfrxbORu1t2huqM-_wu_v2ZvqGoarHvkez-daOT5M-k3q5muB8DJ9oJgaqUYPpNe2-6=IwkZclK1qcaaI1oR2ov0qO_biWAT=Om_zavr7=vR8Tz7V0oRcHxaUk7IKSwcEl7dT1OtRAt_qbwWVVxPPr9DUHBhXjukjMUBi_=Y9uPRx9bXIB=lvUcBW8Ko5E9QQQKBR-2cmufaszPpBHEJ3JCGzTmMYqrRGv07R=7nWq97M=_QFj=RTx-nFlkEcnkQH726t0FwMDgbh-tfb59Ub3NaFWDjUhw8Bo2ISmNkYySYmhvb5=72HtDZLMkqNE2pwKruIoKcDEMPgd8yfRo7P0omS8RkmbYrxfBFSqll1c02CHRASKcRyVd6=mjSDowym39cucoDxIhsj1aYLS_joQVyy0Sl7eaXsINV5KzVgV159xgZOu_CyCwDOJOeDSRjMCvUc9Rp_3LxbjBEdUp0C1M3d=hIbsh=rsS7IEjjAUeuJRtrThdrVXGAHCSNKEqKAD3ystqtDHGTlhm9sqMTdjGckwndN=jYp7g1J12W9y9TfvKxQwraV6-nWIVsADKQrJdXAE6WhGs1NdzIZDBNwwGttjTNb1KuywWMYbtWAd36p3krXQI9JgnSnCS=GsAsbYRxrUI3r_ZOZ2RE3uIRpm12CcJRHk1Kt5WUNvLkx=MwLaoHdvno1uO5pGEu0faTaLy5YjKoyqn9wYmCax93-=6b6gykjz8ECWqJ2ekbBOnt621kDJwgvXZN6nK=MxxTXeM1jU6gt_VhkakShPGyCI1NCnCsPbxTgX-ZVD6flcl1_=U8egTYuD2aIio0-Pcr9rGrgxbwp2-X8u7xY9Y1tPn79QH5==I2oKosKU3xHp7=p8Y6NKJaaqsh2wGRLGBtxXtSlwAm5hUu-pdugTQUgqmQl-7v0NdtVXYuPhp1uDqFAiBFtOXGozTxL-KpQV_noTBVSAE-U0F3hjR_=N=M_hwHy1ONbv-oXD1s61Rt0gJboHGGCPJsbLZGTwQq=GEZtvVMATA=PofvbJhYEaZ-jHA3RlqLK8iKgYyRWXAJycNXVCf=GacI6MdVwOkzPvMRD9L=VTXRfNiCc9FOqcdM3UlYmO_g2ZPWJOpNzRu-apWR0Xzp8Z=C0E27KS7YOapmFmDYT8J89RI8nmfE8YDjBVj01sNYyLBDE77hnL7Vym2sK_KThd6uKjClD8iTDC=eu07SGLUj6PaskHcoZOGU1aOiAY0GZYJBh1=BkUDClyxIP7-gzcxI8jWm8KE3hrHcJ50bsDTFDj8FZp=D=FzHeBLch3SbjYPmWeFqfmXjLWwf2N2It01w-YNbB9riABxsdNdGQuUcsNQ-7mK0MXh2MwUVqGC_DwEwelv9o8=D7uTGJFX2zedkiJW=0wCUkIjSGuU_L8xp6g07yttZlP2E20vu2bUvRlRLYP=0humsMC6U=aS8sKgqWg=lgd1NqKre016GscMMwowd5cTOjccVHoVRh1vb1VJz1WxJ-J7gc7_bSh=Mw=evlqaUMoBUouHXcpgt3A2Xai2jvZ0Hcbh1Mksv_IYcJ_j9MIvKCzfwVWxt8mtB-Gk1xEDczqnX6Y5xBd5k189vQgZm_25oNYgceWuflQ8gyyoRSaEDiSDVUrgj_31mC8xlt0-TnTfAGNswBPoILEOdmzk1WuRxDGMiH2eJnNXImY2f8nLbceIEug9XZntEL3AruwN9wm5EHsioY_dYRUteg1MWCxreTJTUIbWUiKLFNZUpnzPTIjigZx2mkrNRVTyWQVpLFIK1sPKMF7KW7Zn6ukYLC=ovZF5CK8x5jzEwkFO9vbQP2ZnkZHHH8sM9hhqGWTXyy0jP_J78ChYZl0aAtk8bHphNN9LucOM=jnKBxnYnGJdXi0FQzDQ2qySONTOfi52CbkLnWGfTXnnxdzNQsQCtY22I87Jvaf6nAiqMpVGq9lR8ASsM2bNT6YfEaGaZ1OWW2k6CT2m1Nh11IR67mUiWMh1jLvxiJezUf56sdXIzZVXhuayaMLcWhZjkmWdlKjh3q02C7Ei0=HMzSg1qHEW_EttByhnKdQQ1VsNHU8c6usNOocAqFP2Q2WzPERY85BszfLVxcnAjfIKVipEUBKC5TXdYtPdUifdHlRVlO8YBLcRenJ_W8joyCYPNVx9oMYrj-6tVsiIeh7mQMLQz21u_z_Xh7GhzLr=IgMR71aXBsLhYzaTJAFxW007p2OcmvxY3gBsWj_vs8kZMlgM2j==KcwFt8_MpmTbUha7yNgZFGCoZDKCBu3Te-Nv0YB91oG0IaEk1fqZGlEx3lKu==yc8BOqJRN6wruJ=BUfJYRtZoU2hNzm5TvxFKrPWVTT81eaiMb9VMiJz9wEAHGoq7FYZEHQv9nvL2BeUtrTk3Gsy1JiL10FHvEdMCktQGYvSfuBacgYIcsW_f3YrZkBVNUPilV0nO=T7Bi8B_dj7MI3ezogZTSjWrfq7nQzBpq9rDia5uHb7CWAfn=bS22nP6FmXaw52MkFmAQJY-cKQ35Tv920yOmfpFyGL970Ta5wFmTyZLOx0Oa7=rW2e=_bZzlegYFclUWGt8p3PeVDcw1n3NR3Kmx-VSXeNmHnp-IEa8WK5deauMF9JPfgyUNSorStVtlo93vqjYhScJk3LajeJqeTmpADc7LZKfS7EPV6K065sYlPRNLKDpx82j6h9S0fP00Rtyo3UCfimkQBNVQdIGVRLcqRnu=c_MVpU9STw3hHqqyqeHpE0-a51vKk-oHyjpUP0_rF6w_97zHPRaCaqasePDWtbDPDbV7hK_R-EuFpYV2NjdgNL6=iswwzXfoWjLtdEuhSfb=cREKUbGM0UjU0EeHDWFNv5001NP7rQTMXh1vzkxwoKZapIi5T_iSkJf=YLpRwqBMMN2GXluktG-dg1Hkx=crcvTO_dsaMRIf0NJ_OXoS",
    'Connection': "keep-alive",
    'Cookie': "Ad34bsY56=AINWuQlzAQAAbt9X6O8-vsDizAntLFlG3v8denAg-BhFhE6cQx8rH6wtRYlA|1|1|75bc52c6dd91d9103f98a0a8717aab40cbc40433; GeoLocationZipCode=undefined; internationalshippref=preferredcountry=US&preferredcurrency=USD&preferredcountryname=United%20States; no-track=ccpa=false; nordstrom=bagcount=0&firstname=&ispinned=False&isSocial=False&shopperattr=||0|False|-1&shopperid=7f5aba7891044c62a9eb3f597e7de020&USERNAME=; nui=firstVisit=2020-07-01T09%3A33%3A29.111Z&geoLocation=&isModified=false&lme=false; shoppertoken=shopperToken=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI3ZjVhYmE3ODkxMDQ0YzYyYTllYjNmNTk3ZTdkZTAyMCIsImF1ZCI6Imd1ZXN0IiwiaXNzIjoibm9yZHN0cm9tLWd1ZXN0LWF1dGgiLCJleHAiOjE5MDkxMjg4MDksInJlZnJlc2giOjE1OTM2MTA0MDksImp0aSI6IjQ1ZjMxNTA1LTM3YWQtNDdhYi1iMTE4LTU2MWI5MjI1Y2IzZCIsImlhdCI6MTU5MzU5NjAwOX0.gPIkU6p3zbXLdu8UWHZDObXmevm6VuxfWLijpxcekWfZhNlPjBA-DLYxayqxFIIZiSa1NXUoS0XQPm92OOf4Mc62Ro9GvzMsOd9aslaKOOCPqtX5O-J5imZhR69kiF7X9P7sAusHM2lkXVX3eLlpPkHmMI4vJYmc--og0LQ61-WlFSKAmlX1BX2nE-EdD-MTQTsP2-8CuFFEe_Qg3F5UnItaGNmGNkMwvhrprfgDvBpY9uunCvcjFP5D8XlWXDhjmDGsyOo7xW36dSAWB4wcbhlH1Nmz4iqWaDU12dSpLdlSknCvh9VPG_lh8GObYmI4u2SrSXRweIgvefnO9OIPJQ; experiments=ExperimentId=94f5239b-e996-40b7-bb61-1e1f73477d55; forterToken=761bfccfe1e340128355a278f4877f2f_1595631994763__UDF43_6; _gcl_au=1.1.1283531583.1593596010; _ga=GA1.1.607543142.1593596011; _ga_XWLT9WQ1YB=GS1.1.1595631995.16.1.1595632003.0; rkglsid=h-744534289e8add047fe1010017309b96_t-1595632004; storemode=postalCode=&selectedStoreIds=&storesById=&localMarketId=&localMarketsById=; storeprefs=|100|||2020-07-24T23:06:36.190Z; ftr_ncd=6; _sp_id.c229=94f5239b-e996-40b7-bb61-1e1f73477d55.1593596012100.87.1593596012100.1593596012100.1c89f27a-0eef-445c-9700-714e142abd2c; _fbp=fb.1.1593596015553.1949864893; client=viewport=2_SMALL; shopping-bag-migration=shopperId=7f5aba7891044c62a9eb3f597e7de020&isMigrated=true; Bd34bsY56=AIwlFINzAQAA7BMFXGOLdMY7hqUlhVM2F_n-6gH6s09haulPwiivDvTOfSdV; _pin_unauth=dWlkPVpHSXdNak0wWWpNdFpqaGlOQzAwWldZMkxUazJOMll0T0RSaFlXVXdPR1UwWVRBeQ; rfx-forex-rate=currencyCode=USD&exchangeRate=1&quoteId=0; session=FILTERSTATE=&RESULTBACK=&RETURNURL=http%3A%2F%2Fshop.nordstrom.com&SEARCHRETURNURL=http%3A%2F%2Fshop.nordstrom.com&FLSEmployeeNumber=&FLSRegisterNumber=&FLSStoreNumber=&FLSPOSType=&gctoken=&CookieDomain=&IsStoreModeActive=0; usersession=CookieDomain=nordstrom.com&SessionId=7c8a6db7-3195-4979-9228-3b9b1f199537; _4c_mc_=f32b3743-668b-4841-99a1-3a2c206ac42f; minibag=MiniBagHash=1595631997266; buynow=isRegistered=true&isQualified=false; _sp_ses.c229=*; Ad34bsY56_dc=%7B%22c%22%3A%20%22alB3ZzdtcUJENFpSODNyVA%3D%3DX-l_XNrz-2Zxbl2h8Kg-f4z363eBSO5W6U5m41tNSuarKB5pSGUip5eeLPjA3cyAdEKGS4VPRtL2N5L9vYrDw9qVlr4Mig%3D%3D%22%2C%20%22dc%22%3A%200%2C%20%22mf%22%3A%200%7D; _gid=GA1.2.1391794317.1595631999; _gat_UA-107105548-1=1; _uetsid=523f02f414e7ea5290137fcc934899eb; _uetvid=63697fb958606a9ba3c9b84cd3e27301",
    'TE': "Trailers",
    'cache-control': "no-cache",
    'Postman-Token': "63cfca6e-12fa-41bc-a784-634af7b0f91c"
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