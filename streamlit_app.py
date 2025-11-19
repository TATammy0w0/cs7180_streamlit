import streamlit as st
from input.input_form import input_form

# Update last visited page to track page navigation
# This must be done BEFORE input_form() to ensure proper page switch detection
if 'last_visited_page' not in st.session_state:
    st.session_state.last_visited_page = 'main'

# Check if user switched back to main page from another page
current_page = 'main'
page_switched = st.session_state.get('last_visited_page') != current_page

# If user switched pages, clear main page results
if page_switched and st.session_state.get('results_page') == 'main':
    st.session_state.show_results_on_main_page = False
    st.session_state.results_page = None

# Update last visited page
st.session_state.last_visited_page = current_page

st.title("🩺 Multi-Disease Risk Prediction")
st.write(
    "Help you understand your health risks from your health report, head over to [placeholder link](https://docs.streamlit.io/)."
)

input_form()