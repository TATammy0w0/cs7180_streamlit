import streamlit as st
import streamlit_shadcn_ui as ui

st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

# shadow ui component example
with ui.card(key="card1"):
    ui.element("span", children=["Email"], className="text-gray-400 text-sm font-medium m-1", key="label1")
    ui.element("input", key="email_input", placeholder="Your email")

    ui.element("span", children=["User Name"], className="text-gray-400 text-sm font-medium m-1", key="label2")
    ui.element("input", key="username_input", placeholder="Create a User Name")
    ui.element("button", text="Submit", key="button", className="m-1")