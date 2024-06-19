# import frontend libraries
import streamlit as st
from PIL import Image
import os
import datetime

# import backend libraries
import requests
from bs4 import BeautifulSoup
import json
from random import randint
from openai import OpenAI
import re

# API keys


# frontend code
# logo images
logo_image = Image.open(os.path.join(os.path.dirname(__file__), 'logo.PNG'))
kevin_image = Image.open(os.path.join(os.path.dirname(__file__), 'kevin.png'))
bryan_image = Image.open(os.path.join(os.path.dirname(__file__), 'bryan.PNG'))
chase_image = Image.open(os.path.join(os.path.dirname(__file__), 'chase.PNG'))


# Initialize session state for team button
if 'team_open' not in st.session_state:
    st.session_state.team_open = False

# Setup columns
col1, col2, col3 = st.columns([1, 5, 1])

with col1:
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.image(logo_image, width=230)

with col2:
    st.title('Precedent Parser')

with col3:
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    st.write('')
    # Display the Team button with dropdown arrow
    if st.session_state.team_open:
        team_button = st.button('Team \u25B2')
    else:
        team_button = st.button('Team \u25BC')

    # Toggle team_open state when button is clicked
    if team_button:
        st.session_state.team_open = not st.session_state.team_open
        st.experimental_rerun()  # Force a rerun to update the state immediately

# Display team information if team_open is True
if st.session_state.team_open:
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.image(chase_image, width=200)
        st.write('My name is Chase Gillis. I am currently a Junior majoring in Computer Science and minoring in Data Science!')

    with col2:
        st.write('')
        st.write('')
        st.write('')
        st.image(bryan_image, width=200)
        st.write('My name is Bryan Ko. I am currently a Freshman majoring in Computer Science and Data Science, and minoring in Game Design!')

    with col3:
        i = 0
        while i < 6:
            st.write('')
            i += 1
        st.image(kevin_image, width=200)
        st.write('My name is Kevin Dong. I am currently a Freshman majoring in Math and Computer Science, and minoring in Data Science!')

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
    after_date_str = after_date.strftime('%m/%d/%Y')
with col2:
    before_date = st.date_input('Before date:', min_value=datetime.date(1776, 1, 1), max_value=current_date)
    before_date_str = before_date.strftime('%m/%d/%Y')
with col3:
    jurisdiction = st.selectbox('US state:',
                                ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut',
                                 'Delaware', 'District of Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho',
                                 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland',
                                 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana',
                                 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
                                 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania',
                                 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah',
                                 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'])

# backend code
def get_headers_list():
    response = requests.get('http://headers.scrapeops.io/v1/browser-headers?api_key=' + SCRAPEOPS_API_KEY)
    json_response = response.json()
    return json_response.get('result', [])

def get_random_header(header_list):
    random_index = randint(0, len(header_list) - 1)
    return header_list[random_index]

header_list = get_headers_list()

# as per recommendation from @freylis, compile once only
CLEANR = re.compile('<.*?>')

def cleanhtml(raw_html):
    cleantext = re.sub(CLEANR, '', raw_html)
    return cleantext

def search_cases(keywords, jurisdiction=None):
    base_url = 'https://www.courtlistener.com/?type=o&q=contract%20law&type=o&order_by=score%20desc&stat_Precedential=on&filed_after=11%2F15%2F2020&filed_before=12%2F01%2F2023&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag'
    search_url = "https://www.courtlistener.com/api/rest/v3/search/?"
    # keywords
    if (len(keywords) > 0):
        search_url += "q=" + keywords
    search_url += "&type=o&order_by=score%20desc&stat_Precedential=on"
    if (after_date != None):
        year = after_date.strftime("%Y")
        month = after_date.strftime("%m")
        day = after_date.strftime("%d")
        search_url += "&filed_after=" + month + "%2F" + day + "%2F" + year
    # this can be broken if user makes before come after
    if (before_date != None):
        year = before_date.strftime("%Y")
        month = before_date.strftime("%m")
        day = before_date.strftime("%d")
        search_url += "&filed_before=" + month + "%2F" + day + "%2F" + year
    # Have not yet added in ability for other states besides new york yet
    match jurisdiction:
        case "Alabama'":
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
        case 'Alaska':
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
        case 'Arkansas':
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
        case 'California':
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
        case 'Colorado':
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
        case 'Connecticut':
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
        case 'Delaware':
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
        case 'District of Columbia':
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
        case 'Florida':
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
        case 'Georgia':
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
        case 'Hawaii':
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
        case 'Idaho':
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
        case 'Illinois':
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
        case 'Indiana':
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
        case 'Iowa':
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
        case 'Kansas':
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
        case 'Kentucky':
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
        case 'Louisiana':
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
        case 'Maine':
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
        case 'Maryland':
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
        case 'Massachusetts':
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
        case 'Michigan':
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
        case 'Minnesota':
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
        case 'Mississippi':
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
        case 'Missouri':
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
        case 'Montana':
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
        case 'Nebraska':
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
        case 'Nevada':
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
        case 'New Hampshire':
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
        case 'New Jersey':
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
        case 'New Mexico':
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
        case 'New York':
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
        case 'North Carolina':
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
        case 'North Dakota':
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
        case 'Ohio':
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
        case 'Oklahoma':
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
        case 'Oregon':
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
        case 'Pennsylvania':
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
        case 'Rhode Island':
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
        case 'South Carolina':
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
        case 'South Dakota':
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
        case 'Tennessee':
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
        case 'Texas':
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
        case 'Utah':
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
        case 'Vermont':
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
        case 'Virginia':
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
        case 'Washington':
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
        case 'West Virginia':
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
        case 'Wisconsin':
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"
        case 'Wyoming':
            search_url += "&court=nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag"

    print(search_url)
    response = requests.get(search_url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error: {response.status_code}")
        return None

outputMessage = ""
# search button
with col1:
    if st.button('Search'):
        if after_date == before_date:
            outputMessage = 'Please choose a different date'
        else:
            # store all id's in an array
            bigArray = []
            result = search_cases(keywords, jurisdiction)
            # fill the bigArray array with the opinions
            for i in range(len(result["results"])):
                response = requests.get(
                    url="https://www.courtlistener.com/api/rest/v3/opinions/" + (
                        str(result["results"][i]["id"])) + "/?format=json",
                    headers=get_random_header(header_list))
                data = response.json()
                bigArray.append(cleanhtml(data["html_with_citations"]))

            # create a big string that will be put in
            allOpinions = ""
            numberToLimit = int(111111 / len(bigArray)) - 13
            for i in range(len(bigArray)):
                allOpinions += "{OPINION " + str(i + 1) + "}\n"
                allOpinions += bigArray[i] + "\n"

            # if it goes past the word limit, 111111, run it again but this time limit it
            if(len(allOpinions)>= 111111):
                allOpinions = ""
                numberToLimit = int(111111 / len(bigArray)) - 13
                for i in range(len(bigArray)):
                    allOpinions += "{OPINION " + str(i + 1) + "}\n"
                    if len(bigArray[i]) > numberToLimit:
                        # limit it if it's too big
                        allOpinions += bigArray[i][0:numberToLimit] + "...UNFINISHED\n"
                    else:
                        allOpinions += bigArray[i] + "\n"

            # #remove limiter if needed for testing
            # allOpinions += bigArray[i] + "\n"

            #outputMessage = str(len(allOpinions)) + allOpinions
            
            
            client = OpenAI(api_key=OPENAI_API_KEY)

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user",
                           "content": "Based on these Given court opinions stored in the brackets(separated by {OPINION #}) (ignore any HTML format) [" + allOpinions + "] give the name of the inputted case most relevant to the keywords [" + keywords + "] and then use that case information to write a four-sentence strategy that the winning lawyer used so that a new lawyer can mimic it(note that some opinions may be unfinished and will end with:...UNFINISHED). Use direct quotes from the opinion given to support this strategy. The direct quotes don’t count towards the four-sentence limit. If it's impossible to identify the relevant case and provide a strategy with direct quotes, simply respond: No relevant cases based on inputed values. Finally, append the link to the case at the end"
                           }])
            message = response.choices[0].message.content
            outputMessage = message

# reload button
with col2:
    if st.button('Reload'):
        if after_date == before_date:
            outputMessage = 'Please choose a different date'
        else:
            # store all id's in an array
            bigArray = []
            result = search_cases(keywords, jurisdiction)
            # fill the bigArray array with the opinions
            for i in range(len(result["results"])):
                response = requests.get(
                    url="https://www.courtlistener.com/api/rest/v3/opinions/" + (
                        str(result["results"][i]["id"])) + "/?format=json",
                    headers=get_random_header(header_list))
                data = response.json()
                bigArray.append(cleanhtml(data["html_with_citations"]))

            # create a big string that will be put in
            allOpinions = ""
            numberToLimit = int(113600 / len(bigArray)) - 13
            for i in range(len(bigArray)):
                allOpinions += "{OPINION " + str(i + 1) + "}\n"
                if len(bigArray[i]) > numberToLimit:
                    # limit it if it's too big
                    allOpinions += bigArray[i][0:numberToLimit] + "...UNFINISHED\n"
                else:
                    allOpinions += bigArray[i] + "\n"

            outputMessage = str(len(allOpinions)) + allOpinions
            client = OpenAI(api_key=OPENAI_API_KEY)

            response = client.chat.completions.create(
                model="gpt-4-1106-preview",
                messages=[{"role": "user",
                           "content": "Based on these Given court opinions stored in the brackets(separated by {OPINION #}) (ignore any HTML format) [" + allOpinions + "] give the name of the inputted case that is next most relevant to the keywords [" + keywords + "] and then use that case information to write a four-sentence strategy that the winning lawyer used so that a new lawyer can mimic it(note that some opinions may be unfinished and will end with:...UNFINISHED). Use direct quotes from the opinion given to support this strategy. The direct quotes don’t count towards the four-sentence limit. If it's impossible to identify the relevant case or provide a strategy with direct quotes, simply respond: No relevant cases based on inputed values. Finally, append the link to the case at the end"
                           }])
            message = response.choices[0].message.content
            outputMessage = message

st.text_area(label="Result:",
             value="Enter search parameters and press the 'Search' button" if outputMessage == "" else outputMessage,
             height=400, disabled=True, label_visibility="collapsed")
