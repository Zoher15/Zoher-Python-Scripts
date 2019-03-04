import extruct
import requests
from pprint import pprint
import requests
import sys
url=sys.argv[1]
r=requests.get(url)
data=extruct.extract(r.text,r.url)
pprint(data['microdata'])
selected=[properties for properties in data['json-ld'] if properties['@type']=='ClaimReview']
pprint(selected)
