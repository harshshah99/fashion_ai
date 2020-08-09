import pandas as pd
import torch 
import torchvision 
import os
from collections import OrderedDict
import numpy as np
from urllib.request import urlopen
from PIL import Image
import numpy as np
import pickle
from torchvision import transforms as T
import gc
import json

name_key = {
	'men_tshirts' : 'Tshirts',
	'men_casual_shirts' : 'Shirts',
	'women_western_dress' : 'Western Dress',
	'women_tops_tshirts' : 'Tops and Tshirts',
	'women_jumpsuits' : 'Jumpsuits',
	'women_ethnic_dress' : 'Ethnic Dress'
}


def dataframe_to_json(dataframe,csv_name,trend_or_upcom,gender):
	trial_df  = dataframe
	if gender=='men':
		folder_name = 'Men'
	else:
		folder_name = 'Women'
	trial_df = trial_df.rename(columns = {"imageUrl":"imageLink","PAGE_URL_COMPLETE":"productLink"})
	trial_df = trial_df[['productLink','name','imageLink']]
	trial_df['name'] = trial_df['name'].apply(lambda x : x.replace("'",""))
	json_file = trial_df.to_json(orient='records',lines=True)
	json_file = json_file.splitlines()
	json_file = [json.loads(ele) for ele in json_file]
	json_file = str(json_file).replace("'",'"')
	csv_name = name_key.get(csv_name)
	file = open('http_server/data/' + trend_or_upcom + '/' + folder_name + '/' + csv_name + '.json','w')
	file.write(json_file)
	file.close()

device = 'cuda' if torch.cuda.is_available() else 'cpu' #CHECK IF GPU IS AVAILABLE
final_data_path = 'data_files/final_data/'
trending_data_path  = 'trend_reference/Trending/'
upcoming_data_path = 'trend_reference/Upcoming/'
MAX_PRODUCTS_PER_VERTICAL = 50  #Calculating image embeddings for more than 300-400 of URLs is very time consuming and memeory intensive. Since all the images are in URL format and not downloaded, They can't be loaded in parallel using from torch.utils.data import DataLoader so we need to reduce overall products size.

PATH_TO_PRETRAINED_VGG = '/home/harsh_shah/Downloads/vgg16_pretrained.pth' # Change this path to path of pretrained CGG model
vgg_model = torchvision.models.vgg16() #load VGG16 empty model from torchvision library
pretrained_vgg = torch.load(PATH_TO_PRETRAINED_VGG) #load the pretrained VGG16 deepfashion model


#The prtrained model has a diffferent naming convention , where key for each layer of VGG16 is of form 'backbone.features.0.weight' while original VGG16 conatins keys of form 'features.0.weight'. So we need to remove the 'backbone.' from the pretrained keys
new_state_dict = OrderedDict()
for k, v in pretrained_vgg['state_dict'].items():
	name = k.replace('backbone.','') # remove 'backbone.' from the prtrained model state_dict
	new_state_dict[name]=v


vgg_model.load_state_dict(new_state_dict,strict= False) #This model contains some extra layers which we don't need and is also  missing a few layers from the original  state dict of VGG16. So we set 'strict=False' to handle this missing and  extra layers and only load weights off layers availablle in pretrained model

partial_model = vgg_model.features[:27] #we don't need the complete model, only upto last or second last hidden layer to get an embeddding of our image
partial_model =  partial_model.cuda() if torch.cuda.is_available() else partial_model.cuda()
print('\nVGG16 with DEEPFASHION loaded : \n',partial_model)
print('USING DEVICE  : ', device) #show which device we are using - CPU or CUDA

for csv_file in os.listdir(final_data_path):
	print(csv_file)
	gender_value = csv_file.split('_')[0]
	complete_file_name = csv_file.split('.csv')[0]
	product_df = pd.read_csv(final_data_path + csv_file)
	product_df.drop(columns='Unnamed: 0')
	product_df = product_df.drop_duplicates(subset='PAGE_URL_COMPLETE',keep='first')
	trending_df = product_df[product_df['Trending']]
	non_trending_df = product_df[~product_df.index.isin(trending_df.index)]
	"""
	print(len(trending_df))
	print(len(non_trending_df))
	print(len(product_df))
	total_rows = MAX_PRODUCTS_PER_VERTICAL - len(trending_df) #ALL TRENDING PRODUCTS WILL BE IN FINAL DATAFRAME as they are more valued than other products
	current_rows = len(non_trending_df) #ALL PRODUCTS OTHER THAN TRENDING
	fraction = float(total_rows/current_rows) #THIS FRACTION WILL BE USED TO DOWNSAMPLE CURRENT DATAFRAME WHILE MAINTINING FREQUENCY DISTRIBUTION OF WEBSITES SAME
	"""
	fraction = float(MAX_PRODUCTS_PER_VERTICAL/len(non_trending_df))

	downsampled_df = non_trending_df.groupby('Site').apply(pd.DataFrame.sample, frac=fraction).reset_index(drop=True) #downsample the large datframe while mainting frequeny distribution of products across websites 
	final_df = downsampled_df.append(trending_df) #NOW EACH DATAFRAME IS OF SIZE equal to MAX_PRODUCTS_PER_VERTICAL(default = 300)

	del product_df
	del trending_df
	del non_trending_df
	del downsampled_df #RELEASE MEMORY OF UNUSED DATAFRAMES

	image_urls = final_df['imageUrl'].to_list()
	url = ''
	count = 0
	embeddding = []
	X = torch.Tensor(100,100)
	out = torch.Tensor(100,100)
	with torch.no_grad():
		for url in image_urls:
			torch.cuda.empty_cache()
			del out
			del X
			img = Image.open(urlopen(url))
			print(url , count)
			count = count + 1
			#image = Image.open(img)
			try:
				transform = T.Compose([T.Resize((224, 224)), T.ToTensor()])
				X = transform(img).unsqueeze(dim=0).to(device)
				torch.cuda.empty_cache()
				out = partial_model(X)
				embeddding.append(out.cpu().numpy())
				gc.collect()
				torch.cuda.empty_cache()
				print(embeddding[0].shape)
			except Exception as e:
				print(e)
				embeddding.append(np.ndarray(shape=(1,512,14,14)))
				X = torch.Tensor(100,100)
				out = torch.Tensor(100,100)
	print(len(embeddding))
	print(len(final_df))
	embeddding = np.array(embeddding)
	
	trend_embeddings = []
	count = 0
	for trend_img in os.listdir(trending_data_path + csv_file.split('.csv')[0]):
		img_path = trending_data_path + csv_file.split('.csv')[0] + '/' + trend_img
		img = Image.open(img_path)
		with torch.no_grad():
			torch.cuda.empty_cache()
			del out
			del X
			count = count + 1
			print(img_path)
			#image = Image.open(img)
			try:
				transform = T.Compose([T.Resize((224, 224)), T.ToTensor()])
				X = transform(img).unsqueeze(dim=0).to(device)
				torch.cuda.empty_cache()
				out = partial_model(X)
				trend_embeddings.append(out.cpu().numpy())
				gc.collect()
				torch.cuda.empty_cache()
				print(trend_embeddings[0].shape)
			except Exception as e:
				print(e)
				trend_embeddings.append(np.ndarray(shape=(1,512,14,14)))
				X = torch.Tensor(100,100)
				out = torch.Tensor(100,100)

	trend_embeddings = np.array(trend_embeddings)

	embed_distance = []

	for image_emb in embeddding:
		dist = 0.0
		for trend_emb in trend_embeddings:
			dist = dist + np.linalg.norm(trend_emb - image_emb)
		embed_distance.append(dist)
	
	final_df['distance'] = embed_distance
	final_df = final_df.sort_values(by='distance',ascending=True)
	dataframe_to_json(dataframe=final_df, csv_name=complete_file_name,trend_or_upcom='Trending',gender=gender_value)

	upcoming_embeddings = []
	count = 0
	for upcom_img in os.listdir(upcoming_data_path + csv_file.split('.csv')[0]):
		img_path = upcoming_data_path + csv_file.split('.csv')[0] + '/' + upcom_img
		img = Image.open(img_path)
		with torch.no_grad():
			torch.cuda.empty_cache()
			del out
			del X
			count = count + 1
			print(img_path)
			#image = Image.open(img)
			try:
				transform = T.Compose([T.Resize((224, 224)), T.ToTensor()])
				X = transform(img).unsqueeze(dim=0).to(device)
				torch.cuda.empty_cache()
				out = partial_model(X)
				upcoming_embeddings.append(out.cpu().numpy())
				gc.collect()
				torch.cuda.empty_cache()
				print(upcoming_embeddings[0].shape)
			except Exception as e:
				print(e)
				upcoming_embeddings.append(np.ndarray(shape=(1,512,14,14)))
				X = torch.Tensor(100,100)
				out = torch.Tensor(100,100)

	upcoming_embeddings = np.array(upcoming_embeddings)

	upcoming_embed_distance = []

	for image_emb in embeddding:
		dist = 0.0
		for upc_emb in upcoming_embeddings:
			dist = dist + np.linalg.norm(upc_emb - image_emb)
		upcoming_embed_distance.append(dist)
	
	final_df['upcom_distance'] = upcoming_embed_distance
	final_df = final_df.sort_values(by='upcom_distance',ascending=True)
	dataframe_to_json(dataframe=final_df, csv_name=complete_file_name,trend_or_upcom='Upcoming',gender=gender_value)




