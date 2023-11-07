import requests
from bs4 import BeautifulSoup
soup=BeautifulSoup(requests.get('https://case.law/docs/site_features/api#api-base').text)
links=[a['href'] for a in soup.find_all('a', {'class':'gnt_m_th_a'})]
news=''
for l in links:
    url='https://case.law/docs/site_features/api#api-base'+l
    soup=BeautifulSoup(requests.get(url).text)
    title = soup.find_all('h1',{'class':'gnt_ar_hl'})[0].text
    author= soup.find_all('a',{'class':'gnt_ar_by_a gnt_ar_by_a__fi'})[0].text
    date=' '.join(soup.find_all('div',{'class':'gnt_ar_dt'})[0]['aria-label'].split()[4:7])
    news+=title + ',' +author + ',' + date + ',' + url + '\n'

#data=json.loads(requests.get('https://nycourts.gov/courthelp/goingtocourt/records.shtml').text)