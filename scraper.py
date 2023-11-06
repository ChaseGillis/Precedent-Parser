import requests
data=json.loads(requests.get('https://nycourts.gov/courthelp/goingtocourt/records.shtml').text)
len(data)