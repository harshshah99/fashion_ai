"""
This script runs all scrapers in the folder "scraper_files" and writes the result succesful or failed in logfile.txt
The data scraped from all websites will get stored in data_files/scraped_data in form of CSV.
"""

import os
import time

scraper_files =[scraper for scraper in os.listdir('scraper_files')]

file = open('logfile.txt','a')

for scraper in scraper_files:
	print('Executing ',scraper,'..................')
	script_command = 'python' + ' scraper_files/' + scraper
	error_code = os.system(script_command)
	if error_code==0:
		file.writelines(time.ctime() + ':' + scraper + ': Succesful\n')
	else:
		file.writelines(time.ctime() + ':' + scraper + ': Failed\n')

file.close()


