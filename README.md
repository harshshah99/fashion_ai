# flipgrid

Code and Files for Fashion Intelligence Systems

- [x] Myntra
- [x] Ajio 
- [x] Ajio Trends
- [x] Koovs
- [ ] NordStrom   
- [x] Asos

There is an issue with Nordtsrom. A cookie header which expires after approximately 12hrs needs to supplied for code to work.

## Sraper Files: ##

All files [in scraper_files](scraper_files/) contain code for scraping their respective Websites.
For eg. [myntra_scrape.py](scraper_files/myntra_scrape.py) is used to scrape data from Myntra. 


[Site links json Files](categrory_wise_links):

Each json contains keys for product verticals and the specfic key has a value which is the API url we use to scrape the website.
For. eg  in [myntra_links.json](categrory_wise_links/myntra_links.json) the key "men_tshirts" has a value  https://www.myntra.com/web/v2/search/men-tshirts?p=2&sort=new&rows=100&o=0 which is used to scrape Tshirts for Men from Myntra.


After running [data_ranker.py](data_ranker.py) run the following command in terminal:
```bash
sync && echo 3 | sudo tee /proc/sys/vm/drop_caches
```

## Pretrained DeepFashion Model: ##

We have used the vgg16 trained on Attribute prediction to generate embeddings. The link for that model is:

[vgg16_pretrained.pth](https://drive.google.com/file/d/1i7AIdai4f-EAslC2wiRmPzt1vmWxFqS1/view?usp=sharing)

The original link of the model is from here : [ MMFASHION - Category and Attribute Prediction(Fine) Global Pooling VGG 16 Model](https://github.com/open-mmlab/mmfashion/blob/master/docs/MODEL_ZOO.md)
