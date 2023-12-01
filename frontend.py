# import libraries
import streamlit as st
from PIL import Image
import os
import datetime


# backend imports
import requests
from bs4 import BeautifulSoup
import json
from random import randint
from openai import OpenAI







# logo images
logo_image = Image.open(os.path.join(os.path.dirname(__file__), 'logo.PNG'))
kevin_image = Image.open(os.path.join(os.path.dirname(__file__), 'kevin.png'))
bryan_image = Image.open(os.path.join(os.path.dirname(__file__), 'bryan.PNG'))
chase_image = Image.open(os.path.join(os.path.dirname(__file__), 'chase.PNG'))


# set up layout
col1, col2, col3 = st.columns([1.3, 1.3, 1.3])

# setup columns
with col1:
    st.write('')
    st.write('')
    st.image(logo_image, width=230)

with col2:
    st.title('Precedent Parser')  # Adjusted column widths

with col3:
    st.write('')
    team_col = st.columns([1])

    # initialize a state variable to keep track of the toggle state
    team_open = st.session_state.get('team_open', False)

    # display the Team button with dropdown arrow
    if team_open:
        team_button = st.button('Team \u25B2')  # Upwards pointing arrow when open
    else:
        team_button = st.button('Team \u25BC')  # Downwards pointing arrow when closed

    if team_button:
        team_open = not team_open
        st.session_state.update({'team_open': team_open})

    if team_open:
        with col1:
            st.image(chase_image, width=200)
            st.write('My name is Chase Gillis. I am currently a Junior at NYU majoring Computer Science and minoring in Data Science!')
        with col2:
            st.write('')
            st.write('')
            st.write('')
            st.image(bryan_image, width=200)
            st.write('My name is Bryan Ko. I am currently a Freshman at NYU majoring Computer Science and Data Science, and minoring in Game Design!')
        with col3:
            i = 0
            while i < 7:
                st.write('')
                i += 1
            st.image(kevin_image, width=200)
            st.write('My name is Kevin Dong. I am currently a Freshman at NYU majoring Math and Computer Science, and minoring in Data Science!')

# main content section
st.header('What cases are you looking for?')

# search bar
keywords = st.text_area('Enter keywords:', height=100)

# date and state filters
st.subheader('Filter by date and state:')

col1, col2, col3 = st.columns(3)
current_date = datetime.date.today()
with col1:
    after_date = st.date_input('After date:', min_value=datetime.date(1776, 1, 1), max_value=current_date)
with col2:
    before_date = st.date_input('Before date:', min_value=datetime.date(1776, 1, 1), max_value=current_date)
with col3:
    jurisdiction = st.selectbox('US state:', ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'District of Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'])





# backend code

SCRAPEOPS_API_KEY = ""

def get_headers_list():
    response = requests.get('http://headers.scrapeops.io/v1/browser-headers?api_key=' + SCRAPEOPS_API_KEY)
    json_response = response.json()
    return json_response.get('result', [])

def get_random_header(header_list):
    random_index = randint(0, len(header_list) - 1)
    return header_list[random_index]

header_list = get_headers_list()



def search_cases(keywords, jurisdiction=None):
    base_url = 'https://www.courtlistener.com/?type=o&q=contract%20law&type=o&order_by=score%20desc&stat_Precedential=on&filed_after=11%2F15%2F2020&filed_before=12%2F01%2F2023&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag'
    search_url = ""
    #keywords
    if(len(keywords)>0):
        search_url+= keywords
    search_url+= "&type=o&order_by=score%20desc&stat_Precedential=on"
    if(len(after_date)>0):
        search_url += "&filed_after=11%2F15%2F2020"
    #this can be broken if user makes before come after
    if (len(before_date) > 0):
        search_url += "&filed_after=11%2F15%2F2020"
    match jurisdiction:
        case "Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'District of Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'])":
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
        case


    response = requests.get(search_url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error: {response.status_code}")
        return None

bigArrayTest = []

for i in range(len(result["results"])):
    response = requests.get(
        url="https://www.courtlistener.com/api/rest/v3/opinions/" + (str(result["results"][i]["id"])) + "/?format=json",
        headers=get_random_header(header_list))
    data = response.json()
    bigArrayTest.append(data["html_with_citations"])


client = OpenAI(api_key="")

response = client.chat.completions.create(
    model="gpt-4-1106-preview",
    messages=[{"role": "user",
               "content": "Based on the Given court opinion(ignore the HTML format), [" + bigArrayTest[
                   0] + "], Use the most relevant inputted case information to write a one-sentence strategy that the winning lawyer used so that a new lawyer can mimic it"}])
message = response.choices[0].message.content
print(message)





# submit button
if st.button('Search'):
