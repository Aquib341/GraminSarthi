import requests
import json

api_key = "579b464db66ec23bdd000001db83f20366c64a55576340be90bd1ac4"

res1 = requests.get(f"https://api.data.gov.in/catalog/v1?search=Major+Fruits+and+Vegetables+Producing+Countries&api-key={api_key}&format=json&limit=5").json()
print("Search 1:", [r['index_name'] for r in res1.get('records', [])])

res2 = requests.get(f"https://api.data.gov.in/catalog/v1?search=Area+and+Production+of+Vegetables+during+2020-21&api-key={api_key}&format=json&limit=5").json()
print("Search 2:", [r['index_name'] for r in res2.get('records', [])])
