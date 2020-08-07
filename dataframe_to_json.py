#REFERENCE CODE FOR JSON FORMAT ON HTTP SERVER
import pandas as pd
import json


trial_df  = df1[0:10]
trial_df = trial_df[['PAGE_URL_COMPLETE','name','imageUrl']]
json_file = trial_df.to_json(orient='records',lines=True)
json_file = json_file.splitlines()
json_file = [json.loads(ele) for ele in json_file]
json_file = str(json_file).replace("'",'"')
file = open('filename.json','w')
file.write(json_file)
file.close()