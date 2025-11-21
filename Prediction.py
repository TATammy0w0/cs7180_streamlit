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
    "Chronic diseases such as diabetes, high blood pressure, heart disease, and kidney disease remain the leading causes of death in the United States. More than 100 million Americans are currently living with these conditions, and they cost the healthcare system billions of dollars every year."
)
st.write("With our disease prediction app, we aim to change that. By allowing users to input basic biological data, lifestyle information, medical history, and common lab results from routine health checkups, our app can help estimate an individual’s risk of developing diabetes, hypertension, cardiovascular disease (CVD), or chronic kidney disease (CKD).")
st.write("We train our models using the National Health and Nutrition Examination Survey (NHANES) dataset. Data source can be found here: [link](https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/default.aspx?Cycle=2021-2023).")

input_form()