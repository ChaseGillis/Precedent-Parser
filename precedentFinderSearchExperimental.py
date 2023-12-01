import requests 
import requests
from bs4 import BeautifulSoup
import json
from random import randint
from openai import OpenAI






SCRAPEOPS_API_KEY = "[YOUR API KEY]"

# #1. use the search feature to find all the cases according to the filter and keywords
# #2. parse through them to get specifications(cant find the decisions, so just the keywords and jurisdiction should be ok) and store them in arrays e.g: [id, name, decision_date, frontendUrl]
# #3. use a prompt and feed the opinions into chatGPT API, store it in a string
# #4. show this String on the frontend, which i will also build but for now I want some food and sleep  

#scrape ops functions for getting the fake headers
def get_headers_list():
  response = requests.get('http://headers.scrapeops.io/v1/browser-headers?api_key=' + SCRAPEOPS_API_KEY)
  json_response = response.json()
  return json_response.get('result', [])

def get_random_header(header_list):
  random_index = randint(0, len(header_list) - 1)
  return header_list[random_index]




def get_user_agent_list():
  response = requests.get('http://headers.scrapeops.io/v1/user-agents?api_key=' + SCRAPEOPS_API_KEY)
  json_response = response.json()
  return json_response.get('result', [])

def get_random_user_agent(user_agent_list):
  random_index = randint(0, len(user_agent_list) - 1)
  return user_agent_list[random_index]

## Retrieve User-Agent List From ScrapeOps
user_agent_list = get_user_agent_list()
header_list = get_headers_list()


# def search_cases(keywords, jurisdiction=None):
#     base_url = 'https://api.case.law/v1/cases/?search='
#     search_url = base_url + keywords
#     if jurisdiction:
#         search_url += '&jurisdiction=' + jurisdiction + "&full_case=true"
#     response = requests.get(search_url)
#     if response.status_code == 200:
#         data = response.json()
#         return data
#     else:
#         print(f"Error: {response.status_code}")
#         return None


def search_cases(keywords, jurisdiction=None):
    base_url = 'https://api.case.law/v1/cases/?search='
    search_url = "https://www.courtlistener.com/api/rest/v3/search/?q=contract%20law&type=o&order_by=score%20desc&stat_Precedential=on&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
    response = requests.get(search_url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error: {response.status_code}")
        return None



# # experimental
keywords = 'contract law'
jurisdiction = 'ny'

result = search_cases(keywords, jurisdiction)
#print(len(result["results"]))

#response = requests.get("https://www.courtlistener.com/api/rest/v3/opinions/3578215/")
#print(response.status_code)
#data = response.json()
#print(data["html_with_citations"])


bigArrayTest = []

for i in range(len(result["results"])):
  response = requests.get(url = "https://www.courtlistener.com/api/rest/v3/opinions/" + (str(result["results"][i]["id"])) + "/?format=json", headers=get_random_header(header_list))
  data = response.json()
  bigArrayTest.append(data["html_with_citations"])
  print(bigArrayTest[i][0:20])

print(len(bigArrayTest))

  

client = OpenAI(api_key="[YOUR API KEY]")

response = client.chat.completions.create(
  model="gpt-4-1106-preview",
  messages=[{"role": "user", "content": ""}])
message = response.choices[0].message.content
print(message)









# their stuff
# newURL=result['results'][0]['url']
# response = requests.get(newURL)
# print(json.loads(str(BeautifulSoup(response.text,'html.parser'))))

# for i in range(1):
#     response = requests.get(newURL)
#     soup = BeautifulSoup(response.text,'html.parser')
#     newStuff=json.loads(str(soup))
#     newURL = newStuff['frontend_url']
#     print(newStuff)




# new shit with playwright

# from playwright.sync_api import sync_playwright

# storeAllCases = []
# for i in range(50):
#     # go through the frontend url and scrape the opinion
#     #use beautiful soup to get all the <p> and <aside> in the <article class="opinion">
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False, )
#         context = browser.new_context(user_agent=get_random_user_agent(user_agent_list))
#         page = context.new_page()
#         page.goto(result["results"][i]["frontend_url"])
#         html = page.inner_html(".opinion")
#         print(i)
#     #storeAllCases.append([result["results"][i]["id"], result["results"][i]["name"], result["results"][i]["decision_date"], ])


# with sync_playwright() as p:
#     browser = p.chromium.launch(headless=False)
#     context = browser.new_context(user_agent=get_random_user_agent(user_agent_list), )
#     page = context.new_page()
#     for i in range(5):
#         # go through the frontend url and scrape the opinion
#         #use beautiful soup to get all the <p> and <aside> in the <article class="opinion">
#         page.goto("https://www.courtlistener.com/opinion/3424823/general-american-tank-car-corp-v-melville/?type=o&q=car%20crash%20building%20&type=o&order_by=score%20desc&stat_Precedential=on")
#         html = page.inner_html(".opinion")
#         print(html)
#         #storeAllCases.append([result["results"][i]["id"], result["results"][i]["name"], result["results"][i]["decision_date"], ])



# storeAllCases = []

# with sync_playwright() as p:
#     browser = p.chromium.launch(headless=False)
#     context = browser.new_context(user_agent=get_random_user_agent(user_agent_list), )
#     page = context.new_page()
#     page.goto("https://api.case.law/v1/cases/?search=contract%20laws&jurisdiction=ny&full_case=true")
#     html = page.inner_html(".response-info.prettyprint")
#     soup = BeautifulSoup(html,'html.parser')
#     newJson = json.loads(soup.pre.text)
#     print(newJson["results"][0]["casebody"])
       
