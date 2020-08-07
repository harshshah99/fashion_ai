# flipgrid

Code and Files for Fashion Intelligence Systems

- [x] Myntra
- [x] Ajio 
- [x] Ajio Trends
- [x] Koovs
- [ ] NordStrom   
- [x] Asos

There is an issue with Nordtsrom. A cookie header which expires after approximately 12hrs needs to supplied for code to work.

[Sraper Files](scraper_files/):

All files in scraper_files contain code for scraping their respective Websites.
For eg. [myntra_scrape.py](scraper_files/myntra_scrape.py) is used to scrape data from Myntra. 


[Site links json Files](categrory_wise_links):

Each json contains keys for product verticals and the specfic key has a value which is the API url we use to scrape the website.
For. eg  in [myntra_links.json](categrory_wise_links/myntra_links.json) the key "men_tshirts" has a value  https://www.myntra.com/web/v2/search/men-tshirts?p=2&sort=new&rows=100&o=0 which is used to scrape Tshirts for Men from Myntra.
