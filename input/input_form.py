import streamlit as st
import requests
from utils.constants import REQUIRED_FEATURE_SET, OPTIONAL_FEATURE_SET
from models.feature_map import FeatureMap
from input.form_components import create_basic_info_section, create_lab_values_section, create_lifestyle_factors_section, create_medical_history_section
from input.data_validation import format_post_data, validate_form_input, collect_form_values

API_BASE_URL = "https://disease-warning-1.onrender.com"
PREDICT_ALL_URL = f"{API_BASE_URL}/prediction/all"

required_features_map = FeatureMap(REQUIRED_FEATURE_SET)
optional_features_map = FeatureMap(OPTIONAL_FEATURE_SET)

def input_form():
    with st.form("risk_form"):
        _draw_forms()
        
        submitted = st.form_submit_button(
            "Submit", 
            type="primary",
            use_container_width=True
        )

        if submitted:
            missing_fields = validate_form_input(st)
            
            if missing_fields:
                # Store missing fields in session state for rendering feedback
                st.session_state['validation_errors'] = missing_fields
                st.error(f"⚠️ Please fill in all required fields highlighted above ({len(missing_fields)} missing)")
            else:
                # Clear any previous validation errors
                st.session_state['validation_errors'] = {}
                collect_form_values(st, required_features_map, optional_features_map)
                input = format_post_data(required_features_map, optional_features_map)
                data = {"input_data": input}

                try:
                    st.write(f"Sending POST request to `{PREDICT_ALL_URL}`...")
                    st.write("JSON Body:")
                    st.json(data)

                    response = requests.post(PREDICT_ALL_URL, json=data)

                    st.write(f"**Received status code: {response.status_code}**")
                    if response.status_code == 200:
                        st.success("Success! 🎉")
                        st.json(response.json())
                    else:
                        st.error("API request failed")
                        st.subheader("Received error details:")
                        try:
                            st.json(response.json())
                        except requests.exceptions.JSONDecodeError:
                            st.text(response.text)

                except requests.exceptions.ConnectionError as e:
                    st.error(f"Connection failed: {e}")

def _draw_forms():
    create_basic_info_section()
    create_lifestyle_factors_section()        
    create_medical_history_section()
    create_lab_values_section()