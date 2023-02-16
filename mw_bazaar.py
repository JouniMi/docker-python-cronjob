from datetime import datetime
import urllib.request
import urllib.parse
import json
from elasticsearch import Elasticsearch
es = Elasticsearch("http://ES_host:9200")
data = urllib.parse.urlencode({'query': 'get_recent', 'selector': 'time'}).encode()
req = urllib.request.Request('https://mb-api.abuse.ch/api/v1/', data)
response = urllib.request.urlopen(req)
jsonResponse = json.loads(response.read())
for r in jsonResponse["data"]:
    #print(datetime.now())
    r["timestamp"] = datetime.now()
    resp=es.index(index='mw_bazaar',document=r)
    print(resp['result'])
