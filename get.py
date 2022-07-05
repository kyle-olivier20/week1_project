import requests
import os
import json
import pandas as pd
import csv
import datetime
import dateutil.parser
import unicodedata
import time

os.environ['TOKEN'] = 'AAAAAAAAAAAAAAAAAAAAAFEjeQEAAAAAokV07whI73H\
boXpYPJSzqn1e6Es%3DKss22KvpQqUv1l7CdhPG7SpsKorBJkvlQ7neRHttIo89BQcYYg'


def auth():
    return os.getenv('TOKEN')


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def create_url(keyword, start_date, end_date, max_results=10):
    search_url = "https://api.twitter.com/2/tweets/search/all"
    query_params = {'query': keyword, 'start_time': start_date,\
          'end_time': end_date,
        'max_results': max_results, 'expansions': \
        'author_id,in_reply_to_user_id,geo.place_id',
        'tweet.fields': 'id,text,author_id,\
        in_reply_to_user_id,geo,conversation_id, \
        created_at,lang,public_metrics,referenced_tweets,reply_settings,source',
        'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
        'place.fields': 'full_name,id,country,country_code,geo,name,place_type',
        'next_token': {}}
    return (search_url, query_params)


def connect_to_endpoint(url, headers, params, next_token=None):
    params['next_token'] = next_token
    response = requests.request("GET", url, headers=headers, params=params)
    print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
      raise Exception(response.status_code, response.text)
    return response.json()


bearer_token = auth()
headers = create_headers(bearer_token)
keyword = "xbox lang:en"
start_time = "2021-03-01T00:00:00.000Z"
end_time = "2021-03-31T00:00:00.000Z"
max_results = 15

print(json.dumps(json_response, indent=4, sort_keys=True))
json_response['data'][0]['created_at']
json_response['meta']['result_count']

with open('data.json', 'w') as f:
  json.dump(json_response, f)
df = pd.DataFrame(response['json_response'])
df.to_csv('data.csv')

for i in range(0, len(start_list)):
  count = 0
  max_count = 100
  flag = True
  next_token = None
  while flag:
    if count >= max_count:
      break
    print("-------------------")
    print("Token: ", next_token)
    url = create_url(keyword, start_list[i], end_list[i], max_results)
    json_response = connect_to_endpoint(url[0], headers, url[1], next_token)
    result_count = json_response['meta']['result_count']

    if 'next_token' in json_response['meta']:
      next_token = json_response['meta']['next_token']
      print("Next Token: ", next_token)
      if result_count is not None and result_count > 0 and next_token is not None:
        print("Start Date: ", start_list[i])
        append_to_csv(json_response, "data.csv")
        count += result_count
        total_tweets += result_count
        print("Total # of Tweets added: ", total_tweets)
        print("-------------------")
        time.sleep(5)
    else:
      if result_count is not None and result_count > 0:
        print("-------------------")
        print("Start Date: ", start_list[i])
        append_to_csv(json_response, "data.csv")
        count += result_count
        total_tweets += result_count
        print("Total # of Tweets added: ", total_tweets)
        print("-------------------")
        time.sleep(5)
      flag = False
      next_token = None
    time.sleep(5)
print("Total number of results: ", total_tweets)
