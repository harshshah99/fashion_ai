[backend](backend) - Contains Scrapers,Data cleaners,Ranking script and HTTP Server for hosting the final data

[frontend](frontend) - Contains REACT App which fetches data from the HTTP Server and serves to the user 


## Directory Structure ##

```bash
.
├── backend
│   ├── category_wise_links
│   ├── color_files
│   ├── config_parser.py
│   ├── config.yml
│   ├── csv_normalize.py
│   ├── data_files
│   ├── data_ranker.py
│   ├── environment.yml
│   ├── file.json
│   ├── final_try.csv
│   ├── http_server
│   ├── logfile.txt
│   ├── main_script.py
│   ├── models
│   ├── README.md
│   ├── requirements.txt
│   ├── run_all_scrapers.py
│   ├── scraper_files
│   └── trend_reference
├── frontend
│   ├── package.json
│   ├── package-lock.json
│   ├── public
│   ├── README.md
│   ├── similarityScorer.py
│   └── src
└── README.md
```


## How to use ##
 
From [http_server](backend/http_server) execute:

```bash
python server.py
```

And from [frontend](frontend) directory after doing npm install:

```bash
npm start
```


For a more detailed explanation, please see README of [backend](backend/README.md) and [frontend](frontend/README.md) folder. 