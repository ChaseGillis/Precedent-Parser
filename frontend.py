import streamlit as st
from PIL import Image
import os


# logo image
logo_image = Image.open(os.path.join(os.path.dirname(__file__), 'logo.PNG'))


# site heading
st.title('Precedent Parser')
st.sidebar.image(logo_image, use_column_width=True)


# navigation buttons
st.sidebar.button('About')
st.sidebar.button('Team')


# main content section
st.header('What cases are you looking for?')


# search bar
search_term = st.text_input('Enter keywords:', '')


# date and state filters
st.subheader('Filter by date and state:')


col1, col2, col3 = st.columns(3)
with col1:
  after_date = st.date_input('After date:')
with col2:
  before_date = st.date_input('Before date:')
with col3:
  us_state = st.selectbox('US state:', ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'District of Columbia', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'])


# submit button
if st.button('Search'):
  pass
