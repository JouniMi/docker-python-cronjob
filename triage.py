import urllib.request
import urllib.parse
import json
from datetime import datetime, timedelta
from elasticsearch import Elasticsearch
d = datetime.utcnow() - timedelta(minutes=20)
fromdate = str(d.strftime("%Y-%m-%dT%H:%M:%S"))
req = urllib.request.Request(f'https://tria.ge/api/v0/search?query=from:{fromdate}')
req.add_header('Authorization', 'Bearer <your-api-key>')
response = urllib.request.urlopen(req)
jsonResponse = json.loads(response.read())
es = Elasticsearch("http://<your_elk_server>:9200")
for r in jsonResponse["data"]:
    req = urllib.request.Request(f'https://tria.ge/api/v0/samples/{r["id"]}/summary')
    req.add_header('Authorization', 'Bearer <your-api-key>')
    resp = urllib.request.urlopen(req)
    jsonResp = json.loads(resp.read())
    try:
        doc = {
            'created': jsonResp["created"],
            'completed': jsonResp["completed"],
            'sample': jsonResp["sample"],
            'score': jsonResp["score"],
            'sha256': jsonResp["sha256"],
            'target': jsonResp["target"],
        }
        if f'{jsonResp["sample"]}-behavioral1' in jsonResp["tasks"]:
            doc["behavioral1"] = jsonResp["tasks"][f'{jsonResp["sample"]}-behavioral1']
        if f'{jsonResp["sample"]}-behavioral2' in jsonResp["tasks"]:
            doc["behavioral2"] = jsonResp["tasks"][f'{jsonResp["sample"]}-behavioral2']
        if f'{jsonResp["sample"]}-static1' in jsonResp["tasks"]:
            doc["static1"] = jsonResp["tasks"][f'{jsonResp["sample"]}-static1']
        resp=es.index(index='triage',document=doc)
        print(resp['result'])
    except:
        print("Error in pushing data")
