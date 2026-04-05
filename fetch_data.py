import requests
import json
import urllib.parse
api_key = "579b464db66ec23bdd000001db83f20366c64a55576340be90bd1ac4"

try:
    url1 = f"https://api.data.gov.in/catalog/v1?search={urllib.parse.quote('Major Fruits and Vegetables Producing Countries')}&api-key={api_key}&format=json"
    res1 = requests.get(url1).json()
    print("Search 1:", [r['index_name'] for r in res1.get('records', [])])
except Exception as e:
    print(e)

try:
    url2 = f"https://api.data.gov.in/catalog/v1?search={urllib.parse.quote('Area and Production of Vegetables during 2020-21')}&api-key={api_key}&format=json"
    res2 = requests.get(url2).json()
    print("Search 2:", [r['index_name'] for r in res2.get('records', [])])
except Exception as e:
    print(e)
