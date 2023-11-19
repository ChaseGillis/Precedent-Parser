import requests
from bs4 import BeautifulSoup
import json

'''
source bin/activate
git pull .
git add .
git commit -m “message”
git push
'''

def search_cases(keywords, jurisdiction=None):
    base_url = 'https://api.case.law/v1/cases/?search='
    search_url = base_url + keywords
    if jurisdiction:
        search_url += '&jurisdiction=' + jurisdiction
    response = requests.get(search_url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error: {response.status_code}")
        return None

keywords = 'contract law'
jurisdiction = 'ny'

result = search_cases(keywords, jurisdiction)

newURL=result['results'][0]['url']
response = requests.get(newURL)
print(json.loads(str(BeautifulSoup(response.text,'html.parser'))))

for i in range(1):
    response = requests.get(newURL)
    soup = BeautifulSoup(response.text,'html.parser')
    newStuff=json.loads(str(soup))
    newURL = newStuff['frontend_url']
    print(newStuff)