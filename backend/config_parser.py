import yaml
import os

with open('config.yml') as f:
	config_data = yaml.load(f,Loader=yaml.FullLoader)


print('CONFIG SETTINGS:')
for key in config_data.keys():
	print(key,' : ',config_data.get(key),'\n')

site_name = config_data.get('sites')
verticals = config_data.get('verticals')


for file in os.listdir('data_files/scraped_data'):
	file_details = file.split(sep='_',maxsplit=2)
	if file_details[0] in site_name and file_details[2][:-4] in verticals:
		print(file_details[0],'____________________',file)

print('___________________________________________________________________________________________________','\n')

	
print('LIST OF ALL Verticals available for ranking  are :\n\n')
available_verts = []
for file in os.listdir('data_files/scraped_data'):
	available_verts.append(file.split(sep='_',maxsplit=2)[2][:-4])
available_verts = list(set(available_verts))
for i in available_verts:
	print(i)

print('___________________________________________________________________________________________________\n')
print('LIST of Verticals in Config and Sites which contain those vericals : \n')
#This LOOP shows for a particular product vertical , which all sites have that product available with them
#For example Women Western Dress is present in just ASOS, MYNTRA and KOOVS. Check the output of this file and you will see these 3 listed with women_western_dress
for vert in verticals:
	comps = []
	for file in os.listdir('data_files/scraped_data'):
		file_details = file.split(sep='_',maxsplit=2)
		if file_details[2][:-4]==vert:
			comps.append(file_details[0])
	print(vert,'--------',list(set(comps)))

print('\n')
