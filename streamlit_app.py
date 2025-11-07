import streamlit as st
from input_form import three_diseases_input_form

st.title("🩺 Multi-Disease Risk Prediction")
st.write(
    "Help you understand your health risks from your health report, head over to [placeholder link](https://docs.streamlit.io/)."
)

three_diseases_input_form()