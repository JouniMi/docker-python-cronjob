import urllib.request
import urllib.parse
import json
from datetime import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch("http://ES_host:9200")
req = urllib.request.Request('https://www.hybrid-analysis.com/api/v2/feed/latest')
req.add_header('api-key', 'hybrid_analysis_api_key')
req.add_header('user-agent', 'Falcon Sandbox')
response = urllib.request.urlopen(req)
jsonResponse = json.loads(response.read())
for r in jsonResponse["data"]:
    #print(r)
    #print(datetime.now())
    r["timestamp"] = datetime.now()
    resp=es.index(index='hybrid_analysis',document=r)
    print(resp['result'])
