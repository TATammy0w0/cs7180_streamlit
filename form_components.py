import streamlit as st
from constants import GENDER_MAP, TF_MAP, REQUIRED_FIELDS

def create_basic_info_section():
    """Create the Basic Information section of the form."""
    st.subheader("Basic Information")
    
    st.pills(
            "Gender at Birth",
            options=GENDER_MAP.keys(),
            format_func=lambda option: GENDER_MAP[option],
            selection_mode="single",
            key=REQUIRED_FIELDS["Gender"]
        )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.number_input("Age (years)", 
                       value=None,
                       min_value=0, 
                       step=1, 
                       key=REQUIRED_FIELDS["Age"])

        st.number_input("Weight (kg)", 
                       value=None,
                       min_value=0.0, 
                       step=0.1, 
                       format="%.1f", 
                       key=REQUIRED_FIELDS["Weight"])

    with col2:     
        st.number_input("Height (cm)", 
                       value=None,
                       min_value=0.0, 
                       step=0.1, 
                       format="%.1f", 
                       key=REQUIRED_FIELDS["Height"])
        
        st.number_input("Waist Circumference (cm)", 
                       value=None,
                       min_value=0.0, 
                       step=0.1, 
                       format="%.1f", 
                       key=REQUIRED_FIELDS["Waist"])

def create_lifestyle_factors_section():
    """Create the Lifestyle Factors section of the form."""
    st.subheader("Lifestyle Factors")

    st.write("##### Smoking History")
    st.pills(
        "Have you ever smoked 100 cigarettes in life?",
        options=TF_MAP.keys(),
        format_func=lambda option: TF_MAP[option],
        selection_mode="single",
        key=REQUIRED_FIELDS["Smoking History"]
    )
    
    # Always render the follow-up question
    st.selectbox(
        "How often do you currently smoke?",
        options=["", "Every day", "Some days", "Not at all"],
        key=REQUIRED_FIELDS["Smoking Frequency"]
    )

    # Alcohol consumption section
    st.write("##### Alcohol Consumption")
    st.selectbox(
        "How often do you currently drink alcohol?",
        options=["", "Never", "Less than 1 day per month", "1-2 days per month", "3-4 days per month", "2-3 days per week", "4-5 days per week", "Nearly every day/Everyday"],
        key=REQUIRED_FIELDS["Alcohol"]
    )

def create_lab_values_section():
    """Create the Laboratory Values section of the form."""
    st.subheader("Laboratory Values")
    
    bp_col1, bp_col2 = st.columns(2)
    with bp_col1:
        st.number_input("Systolic Blood Pressure", 
                       value=None,
                       min_value=0.0, 
                       step=1.0, 
                       format="%.1f", 
                       key="user_systolic")
    
    with bp_col2:
        st.number_input("Diastolic Blood Pressure", 
                       value=None,
                       min_value=0.0, 
                       step=1.0, 
                       format="%.1f", 
                       key="user_diastolic")

    st.number_input("HbA1c (%)", 
                   value=None,
                   min_value=0.0, 
                   step=0.1, 
                   format="%.1f", 
                   key="user_hba1c")
