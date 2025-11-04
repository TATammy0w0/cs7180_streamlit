import streamlit as st
import streamlit_shadcn_ui as ui

st.title("🩺 Multi-Disease Risk Prediction")
st.write(
    "Help you understand your health risks from your health report, head over to [placeholder link](https://docs.streamlit.io/)."
)

# shadow ui component example
with ui.card(key="card1"):
    ui.element("span", children=["Your Height (cm)"], className="text-gray-400 text-sm font-medium m-1", key="label1")
    ui.element("input", key="user_height", placeholder="e.g. 170")

    ui.element("span", children=["Your Weight (kg)"], className="text-gray-400 text-sm font-medium m-1", key="label2")
    ui.element("input", key="user_weight", placeholder="e.g. 70.5")

    ui.element("span", children=["Your Age (years)"], className="text-gray-400 text-sm font-medium m-1", key="label3")
    ui.element("input", key="user_age", placeholder="e.g. 25")

    ui.element("button", text="Submit", key="button", className="m-1")