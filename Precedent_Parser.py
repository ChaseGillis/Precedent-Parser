# import frontend libraries
import streamlit as st
from PIL import Image
import os
import datetime
import numpy as np

# import backend libraries
import requests
from bs4 import BeautifulSoup
import json
from random import randint
from openai import OpenAI
import re


def invert_image(image):
    
    # Convert image to numpy array
    img_array = np.array(image)
    
    # Invert image color
    inverted_array = 255 - img_array
    
    # Convert array back to image
    inverted_image = Image.fromarray(inverted_array.astype('uint8'))
    
    return inverted_image


# frontend code
# logo images
# logo_image = Image.open(os.path.join(os.path.dirname(__file__), 'logo.png'))
#logo_image = invert_image(logo_image)
kevin_image = Image.open(os.path.join(os.path.dirname(__file__), 'kevin.png'))
bryan_image = Image.open(os.path.join(os.path.dirname(__file__), 'bryan.png'))
chase_image = Image.open(os.path.join(os.path.dirname(__file__), 'chase.png'))

# Access the API keys from environment variables
SCRAPEOPS_API_KEY = os.environ['SCRAPEOPS_API_KEY']
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']



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
    st.write('')
    st.write('')

with col2:
    st.title(':orange[PRECEDENT PARSER]')

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
keywords = st.text_area(':white[Enter keywords:]', height=100)

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
    if len(keywords) > 0:
        search_url += f"q={keywords}"

    search_url += "&type=o&order_by=score%20desc&stat_Precedential=on"

    # after_date and before_date
    if after_date is not None:
        after_date_str = after_date.strftime("%m/%d/%Y")
        search_url += f"&filed_after={after_date_str}"

    if before_date is not None:
        before_date_str = before_date.strftime("%m/%d/%Y")
        search_url += f"&filed_before={before_date_str}"

    # jurisdiction
    if jurisdiction:
        state_courts = {
            "Alabama": "almd%20alnd%20alsd%20almd%20almd%20almdb%20alsd%20ald",
            "Alaska": "akd%20akd%20akd%20akd%20akd%20akd%20akd%20akd%20akd%20akd%20akd%20akd%20akd",
            "Arizona": "azd%20azd%20azd%20azd%20azd%20azd%20azd%20azd%20azd%20azd%20azd%20azd%20azd",
            "Arkansas": "ared%20arwd%20ared%20ared%20ared%20ared%20ared%20arwd%20arwd%20arwd%20arwd%20arwd%20arwd",
            "California": "cand%20cacd%20casd%20cand%20cand%20cand%20cand%20cand%20cand%20cand%20cand%20cand%20cand",
            "Colorado": "cod%20cod%20cod%20cod%20cod%20cod%20cod%20cod%20cod%20cod%20cod%20cod%20cod",
            "Connecticut": "ctd%20ctd%20ctd%20ctd%20ctd%20ctd%20ctd%20ctd%20ctd%20ctd%20ctd%20ctd%20ctd",
            "Delaware": "ded%20ded%20ded%20ded%20ded%20ded%20ded%20ded%20ded%20ded%20ded%20ded%20ded",
            "District of Columbia": "dcd%20dcd%20dcd%20dcd%20dcd%20dcd%20dcd%20dcd%20dcd%20dcd%20dcd%20dcd%20dcd",
            "Florida": "fld%20fld%20fld%20fld%20fld%20fld%20fld%20fld%20fld%20fld%20fld%20fld%20fld",
            "Georgia": "gand%20gand%20gand%20gand%20gand%20gand%20gand%20gand%20gand%20gand%20gand%20gand%20gand",
            "Hawaii": "hid%20hid%20hid%20hid%20hid%20hid%20hid%20hid%20hid%20hid%20hid%20hid%20hid",
            "Idaho": "idd%20idd%20idd%20idd%20idd%20idd%20idd%20idd%20idd%20idd%20idd%20idd%20idd",
            "Illinois": "ild%20ilnd%20ilcd%20ild%20ild%20ild%20ild%20ild%20ild%20ild%20ild%20ild%20ild",
            "Indiana": "ind%20ind%20ind%20ind%20ind%20ind%20ind%20ind%20ind%20ind%20ind%20ind%20ind",
            "Iowa": "iad%20iasd%20iasd%20iad%20iad%20iad%20iad%20iad%20iad%20iad%20iad%20iad%20iad",
            "Kansas": "ksd%20ksd%20ksd%20ksd%20ksd%20ksd%20ksd%20ksd%20ksd%20ksd%20ksd%20ksd%20ksd",
            "Kentucky": "kyd%20kyd%20kyd%20kyd%20kyd%20kyd%20kyd%20kyd%20kyd%20kyd%20kyd%20kyd%20kyd",
            "Louisiana": "lad%20lad%20lad%20lad%20lad%20lad%20lad%20lad%20lad%20lad%20lad%20lad%20lad",
            "Maine": "med%20med%20med%20med%20med%20med%20med%20med%20med%20med%20med%20med%20med",
            "Maryland": "mdd%20mdd%20mdd%20mdd%20mdd%20mdd%20mdd%20mdd%20mdd%20mdd%20mdd%20mdd%20mdd",
            "Massachusetts": "mad%20mad%20mad%20mad%20mad%20mad%20mad%20mad%20mad%20mad%20mad%20mad%20mad",
            "Michigan": "mid%20mid%20mid%20mid%20mid%20mid%20mid%20mid%20mid%20mid%20mid%20mid%20mid",
            "Minnesota": "mnd%20mnd%20mnd%20mnd%20mnd%20mnd%20mnd%20mnd%20mnd%20mnd%20mnd%20mnd%20mnd",
            "Mississippi": "msnd%20mssd%20mssd%20msnd%20msnd%20msnd%20msnd%20msnd%20msnd%20msnd%20msnd%20msnd%20msnd",
            "Missouri": "moed%20moed%20moed%20moed%20moed%20moed%20moed%20moed%20moed%20moed%20moed%20moed%20moed",
            "Montana": "mtd%20mtd%20mtd%20mtd%20mtd%20mtd%20mtd%20mtd%20mtd%20mtd%20mtd%20mtd%20mtd",
            "Nebraska": "ned%20ned%20ned%20ned%20ned%20ned%20ned%20ned%20ned%20ned%20ned%20ned%20ned",
            "Nevada": "nvd%20nvd%20nvd%20nvd%20nvd%20nvd%20nvd%20nvd%20nvd%20nvd%20nvd%20nvd%20nvd",
            "New Hampshire": "nhd%20nhd%20nhd%20nhd%20nhd%20nhd%20nhd%20nhd%20nhd%20nhd%20nhd%20nhd%20nhd",
            "New Jersey": "njd%20njd%20njd%20njd%20njd%20njd%20njd%20njd%20njd%20njd%20njd%20njd%20njd",
            "New Mexico": "nmd%20nmd%20nmd%20nmd%20nmd%20nmd%20nmd%20nmd%20nmd%20nmd%20nmd%20nmd%20nmd",
            "New York": "nyed%20nynd%20nysd%20nywd%20nyeb%20nynb%20nysb%20nywb%20ny%20nyappdiv%20nyappterm%20nysupct%20nyfamct%20nysurct%20nycivct%20nycrimct%20nyag",
            "North Carolina": "nced%20nced%20nced%20nced%20nced%20nced%20nced%20nced%20nced%20nced%20nced%20nced%20nced",
            "North Dakota": "ndd%20ndd%20ndd%20ndd%20ndd%20ndd%20ndd%20ndd%20ndd%20ndd%20ndd%20ndd%20ndd",
            "Ohio": "ohnd%20ohnd%20ohnd%20ohnd%20ohnd%20ohnd%20ohnd%20ohnd%20ohnd%20ohnd%20ohnd%20ohnd%20ohnd",
            "Oklahoma": "okwd%20okwd%20okwd%20okwd%20okwd%20okwd%20okwd%20okwd%20okwd%20okwd%20okwd%20okwd%20okwd",
            "Oregon": "ord%20ord%20ord%20ord%20ord%20ord%20ord%20ord%20ord%20ord%20ord%20ord%20ord",
            "Pennsylvania": "pad%20pad%20pad%20pad%20pad%20pad%20pad%20pad%20pad%20pad%20pad%20pad%20pad",
            "Rhode Island": "rid%20rid%20rid%20rid%20rid%20rid%20rid%20rid%20rid%20rid%20rid%20rid%20rid",
            "South Carolina": "scd%20scd%20scd%20scd%20scd%20scd%20scd%20scd%20scd%20scd%20scd%20scd%20scd",
            "South Dakota": "sdd%20sdd%20sdd%20sdd%20sdd%20sdd%20sdd%20sdd%20sdd%20sdd%20sdd%20sdd%20sdd",
            "Tennessee": "tnmd%20tnmd%20tnmd%20tnmd%20tnmd%20tnmd%20tnmd%20tnmd%20tnmd%20tnmd%20tnmd%20tnmd%20tnmd",
            "Texas": "txed%20txnd%20txsd%20txwd%20txed%20txed%20txed%20txed%20txnd%20txsd%20txwd%20txed%20txed",
            "Utah": "utd%20utd%20utd%20utd%20utd%20utd%20utd%20utd%20utd%20utd%20utd%20utd%20utd",
            "Vermont": "vtd%20vtd%20vtd%20vtd%20vtd%20vtd%20vtd%20vtd%20vtd%20vtd%20vtd%20vtd%20vtd",
            "Virginia": "vad%20vad%20vad%20vad%20vad%20vad%20vad%20vad%20vad%20vad%20vad%20vad%20vad",
            "Washington": "wad%20wad%20wad%20wad%20wad%20wad%20wad%20wad%20wad%20wad%20wad%20wad%20wad",
            "West Virginia": "wvsd%20wvsd%20wvsd%20wvsd%20wvsd%20wvsd%20wvsd%20wvsd%20wvsd%20wvsd%20wvsd%20wvsd%20wvsd",
            "Wisconsin": "wid%20wid%20wid%20wid%20wid%20wid%20wid%20wid%20wid%20wid%20wid%20wid%20wid",
            "Wyoming": "wyd%20wyd%20wyd%20wyd%20wyd%20wyd%20wyd%20wyd%20wyd%20wyd%20wyd%20wyd%20wyd",
            "Guam": "gud%20gud%20gud%20gud%20gud%20gud%20gud%20gud%20gud%20gud%20gud%20gud%20gud",
            "Northern Mariana Islands": "mpd%20mpd%20mpd%20mpd%20mpd%20mpd%20mpd%20mpd%20mpd%20mpd%20mpd%20mpd%20mpd",
            "Puerto Rico": "prd%20prd%20prd%20prd%20prd%20prd%20prd%20prd%20prd%20prd%20prd%20prd%20prd",
            "U.S. Virgin Islands": "vid%20vid%20vid%20vid%20vid%20vid%20vid%20vid%20vid%20vid%20vid%20vid%20vid",
        }

        if jurisdiction in state_courts:
            search_url += f"&court={state_courts[jurisdiction]}"

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
            try:
                numberToLimit = int(111111 / len(bigArray)) - 13
            except ZeroDivisionError:
                numberToLimit = 0
                print("Can't divide by 0")
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
            try:
                numberToLimit = int(113600 / len(bigArray)) - 13
            except ZeroDivisionError:
                numberToLimit = 0
                print("Cant divid by 0")
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


# Use st.markdown to style the text content
st.markdown(
    f'<div style="color: white;">Result:</div>',
    unsafe_allow_html=True
)


# Define your text content
text_content = "Enter search parameters and press the 'Search' button" if outputMessage == "" else f"{outputMessage}"

# Define custom CSS style for the outer box and text content
custom_style = """
    <style>
        .custom-box {
            background-color: #282434; /* Green background color */
            padding: 10px; /* Padding around the content */
            border-radius: 5px; /* Rounded corners */
        }
        .custom-text {
            color: white; /* Text color */
        }
    </style>
"""

# Use st.markdown to display the styled outer box and text content
st.markdown(
    f'{custom_style}<div class="custom-box"><div class="custom-text">{text_content}</div></div>',
    unsafe_allow_html=True
)

