import os

scraper_files =[file for file in os.listdir() if file[-9:]=='scrape.py']

for file in scraper_files:
	print('Executing ',file,'..................')
	script_command = 'python' + ' ' + file
	os.system(script_command)
