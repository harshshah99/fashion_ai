import os
import time

scraper_files =[scraper for scraper in os.listdir('scraper_files/') if scraper[-3:]=='.py']
print(scraper_files)


file = open('logfile.txt','a')

for scraper in scraper_files:
	print('Executing ',scraper,'..................')
	script_command = 'python' + ' scraper_files/' + scraper
	error_code = os.system(script_command)
	if error_code==0:
		file.writelines(time.ctime() + ':' + scraper + ': Succesful\n')
	else:
		file.writelines(time.ctime() + ':' + scraper + ': Failed\n')
