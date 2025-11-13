import streamlit as st
from constants import REQUIRED_FEATURE_SET, OPTIONAL_FEATURE_SET
from feature_map import FeatureMap
from form_components import create_basic_info_section, create_lab_values_section, create_lifestyle_factors_section, create_medical_history_section
from data_validation import format_post_data, validate_form_input, collect_form_values

required_features_map = FeatureMap(REQUIRED_FEATURE_SET)
optional_features_map = FeatureMap(OPTIONAL_FEATURE_SET)

def three_diseases_input_form():
    with st.form("risk_form"):
        create_basic_info_section()
        create_lifestyle_factors_section()
        create_medical_history_section()
        create_lab_values_section()
        
        submitted = st.form_submit_button(
            "Submit", 
            type="primary",
            use_container_width=True
        )

        if submitted:
            missing_fields = validate_form_input(st)
            collect_form_values(st, required_features_map, optional_features_map)
            data = format_post_data(required_features_map, optional_features_map)
            st.write(data)
            st.write(required_features_map.get("Weight"))

            if missing_fields:
                st.error(f"Please fill in all required fields: {', '.join(missing_fields)}")