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

print('___________________________________________________________________________________________________')

for vert in verticals:
	comps = []
	for file in os.listdir('data_files/scraped_data'):
		file_details = file.split(sep='_',maxsplit=2)
		if file_details[2][:-4]==vert:
			comps.append(file_details[0])
	print(vert,'--------',list(set(comps)))
	