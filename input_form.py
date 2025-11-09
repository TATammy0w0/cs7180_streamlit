import streamlit as st
from form_components import create_basic_info_section, create_lab_values_section, create_lifestyle_factors_section
from data_validation import validate_form_input, collect_form_values

def three_diseases_input_form():
    with st.form("risk_form"):
        create_basic_info_section()
        create_lab_values_section()
        create_lifestyle_factors_section()
        
        submitted = st.form_submit_button(
            "Submit", 
            type="primary",
            use_container_width=True
        )

        if submitted:
            missing_fields = validate_form_input(st)
            
            # Additional validation: if user smoked 100 cigarettes, they must answer frequency
            smoked_100 = st.session_state.get("smoked_100")
            smoking_frequency = st.session_state.get("smoking_frequency", "")
            if smoked_100 == 1 and not smoking_frequency:
                missing_fields.append("Smoking Frequency")
            
            if missing_fields:
                st.error(f"Please fill in all required fields: {', '.join(missing_fields)}")
            else:
                values = collect_form_values(st)
                st.success("Successfully submitted!")
                st.write(values)