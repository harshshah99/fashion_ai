# flipgrid

Code and Files for Fashion Intelligence Systems

- [x] Myntra
- [x] Ajio 
- [x] Ajio Trends
- [x] Koovs
- [ ] NordStrom   
- [x] Asos

There is an issue with Nordtsrom. A cookie header which expires after approximately 12hrs needs to supplied for code to work.

## Sraper Files ##

All files [in scraper_files](scraper_files/) contain code for scraping their respective Websites.
For eg. [myntra_scrape.py](scraper_files/myntra_scrape.py) is used to scrape data from Myntra. 


## Site links json Files ##

Each json_file in [category_wise_links](category_wise_links) contains keys for product verticals and the specfic key has a value which is the API url we use to scrape the website.
For. eg  in [myntra_links.json](categrory_wise_links/myntra_links.json) the key "men_tshirts" has a value  https://www.myntra.com/web/v2/search/men-tshirts?p=2&sort=new&rows=100&o=0 which is used to scrape Tshirts for Men from Myntra.

## Config ##

the [config.yml](config.yml) file contains the two important aspects of this app:

1. Websites
2. Product Verticals

From all the files present in [this folder](data_files/scraped_data/), config.yml is resonsible for deciding which verticals and which websites will be used in creating the final data which will be ranked and served to the user.

Running [config_parser.py](config_parser.py) one can see the current config settings, the websites being scraped, the verticals which are included and also available ones which haven't been included. 

## Pretrained DeepFashion Model ##

We have used the vgg16 trained on Attribute prediction to generate embeddings. The link for that model is:

[vgg16_pretrained.pth](https://drive.google.com/file/d/1i7AIdai4f-EAslC2wiRmPzt1vmWxFqS1/view?usp=sharing)

The original link of the model is from here : 
[ MMFASHION - Category and Attribute Prediction(Fine) Global Pooling VGG 16 Model](https://github.com/open-mmlab/mmfashion/blob/master/docs/MODEL_ZOO.md)



After running [data_ranker.py](data_ranker.py) run the following command in terminal:
```bash
sync && echo 3 | sudo tee /proc/sys/vm/drop_caches
```



### Execution Order ###

1. INSTALL python dependencies through pip & [requirements.txt](requirements.txt) or conda & [environment.yml](environment.yml)
	1. For python create a virtual environment and execute this inside the virtual environment:
	```bash
	pip install -r requirements.txt
	```
	2. For anaconda/conda execute this from the main folder:
	```bash
	conda env create --file environment.yml
	```

2. SCRAPING:
	1. From the main folder, execute : 
	```bash
	python run_all_scrapers.py
	```
	2. Check data_files/scraped_data to see if there are   CSV files in it.
	3. To run an indivdual scraper for.eg Myntra:
	```bash
	python scraper_files/myntra_scrape.py
	```

3. DATA CLEANING: 
	1. ALL CSVs in [scraped_data](data_files/scraped_data/) have different column name since they are scraped from different sites.
	2. Before ranking them we need to make sure they all  have same columns so that no paricular site has some kind of bias
	3. From the main folder execute :  
	```bash
	python csv_normalize.py
	```
	4. This will create product vertical CSVs in [data_files/final_data/](data_files/final_data/)
	5. [men_tshirts.csv](men_tshirts.csv) will contain information regarding Tshirts scraped from all sites in [Config](config.yml)

4. RANKING:
	1. Download the [pretrained_vgg](https://drive.google.com/file/d/1i7AIdai4f-EAslC2wiRmPzt1vmWxFqS1/view?usp=sharing) model and place it [models](models/)
	2. From the main folder, execute :  
	```bash
	python data_ranker.py
	```
	3. Data Ranker will use [trend_reference](trend_reference) to compare the scraped products.
	4. [Trending](trend_reference/Trending) contains images of Trending products in given verticals
	5. [Upcoming](trend_reference/Upcoming) contains images of forecasted trends for given product verticals
	6. ALL products are ranked and stored in [here](http_server/data) - in 2 categories : Trending and Upcoming
	7. [Trending](trend_reference/Trending) contains products ranked according to Spring-Summer 2020 ie. Observed Recent Trends
	8. [Upcoming](trend_reference/Upcoming) contains ranked products according to to Fall-Winter 2020 ie. Forecasted Trends

5. Python HTTP Server:
	1. The [http_server](http_server) folder contains data for the website like homepage images and RANKED DATA
	2. Change current working directory to http_server
	```bash
	cd http_server/
	```
	3. From http_server/ folder run: 
	```bash
	python server.py
	```
	4. Above commands hosts the JSON files in [Trending](http_server/data/Trending/Women) and in [Upcoming](http_server/data/Upcoming/Men) to a Local HTTP Server
	5. These JSON files are hosted at PORT 9004 which communicates with React App to display the products