NOTE : 

ALL Files in this folder 'scraper_files' of the format 'website-name_scrape.py' are responsible for scraping products from that particular 'website-name'

[myntra_scrape.py](myntra_scrape.py) - The code in this file is well documeneted with each step explained clearly

All other scraper scripts like ajio_scrape.py, asos_scrape.py and others, they all follow the same template as [myntra_scrape.py](myntra_scrape.py) so providing comments in each of these would be redundant.

Basic elements common across all scrapers: 

1) class myntra_products(category) [or website_products(category) in general] : 
	- Contains an init method which initilizes category variable with one provided above
	- scrape_new() and scrape_popular() are functions of above class which scrape new and popular products respectively from given website
	- datframe_handling() - Above scraped data is cleaned, modified and savedcas csv with appropriate naming format [here](../data_files/scraped_data)
	- for each website-name_scrape.py there is a webite-name_links.json [here](../category_wise_links)
	  For eg myntra_scrape.py uses [myntra_links.json](../category_wise_links/myntra_links.json) to refer and scrape vericals

Only things that differ across scrapers are :
	- How their URL changes when showing 'NEW' and 'POPULAR' products for eg. "sort=new" in URL results in products sorted by TIME/DATE ADDED
	- How the URL changes when we look at more number of products.for eg URL for scraping 100 products and next 100 products may differ in "&p=1" and "&p=2"
	- Name of the column which has unique entry for each products(similar to a PRIMIARY KEY)