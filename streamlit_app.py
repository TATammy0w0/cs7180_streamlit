import streamlit as st
from form_components import create_basic_info_section, create_lab_values_section
from data_validation import validate_form_input, collect_form_values

def main():
    """Main application function."""
    st.title("🩺 Multi-Disease Risk Prediction")
    
    with st.form("risk_form"):
        create_basic_info_section()
        create_lab_values_section()
        
        submitted = st.form_submit_button(
            "Submit", 
            type="primary",
            use_container_width=True
        )

        if submitted:
            missing_fields = validate_form_input(st)
            
            if missing_fields:
                st.error(f"Please fill in all required fields: {', '.join(missing_fields)}")
            else:
                values = collect_form_values(st)
                st.success("Successfully submitted!")
                st.write(values)

if __name__ == "__main__":
    main()