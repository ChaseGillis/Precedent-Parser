# import libraries
import streamlit as st
from PIL import Image
import os
import datetime

# logo images
logo_image = Image.open(os.path.join(os.path.dirname(__file__), 'logo.PNG'))
kevin_image = Image.open(os.path.join(os.path.dirname(__file__), 'kevin.png'))
chase_image = Image.open(os.path.join(os.path.dirname(__file__), 'chase.PNG'))
bryan_image = Image.open(os.path.join(os.path.dirname(__file__), 'bryan.PNG'))


# set up layout
col1, col2, col3 = st.columns([1.3, 1.3, 1.3])

# setup columns
with col1:
    st.write('')
    st.write('')
    st.image(logo_image, width=220)

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
            st.write('')
            st.write('')
            st.write('')
            st.write('')
            st.write('')
            st.write('')
            st.image(kevin_image, width=200)
            st.write('My name is Kevin Dong. I am currently a Freshman at NYU majoring Math and Computer Science, and minoring in Data Science!')

# main content section
st.header('What cases are you looking for?')

# search bar
search_term = st.text_area('Enter keywords:', height=100)

# date and state filters
st.subheader('Filter by date and state:')

col1, col2, col3 = st.columns(3)
current_date = datetime.date.today()
with col1:
    after_date = st.date_input('After date:', min_value=datetime.date(1776, 7, 4), max_value=current_date)
with col2:
    before_date = st.date_input('Before date:', min_value=datetime.date(1776, 7, 4), max_value=current_date)
with col3:
    us_state = st.selectbox('US state:', ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'District of Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'])

# submit button
if st.button('Search'):
    pass
