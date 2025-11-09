import streamlit as st

tf_map = {
    1: "Yes",
    2: "No"
}

def create_basic_info_section():
    """Create the Basic Information section of the form."""
    st.subheader("Basic Information")
    
    gender_map = {
            1: "Male",
            2: "Female"
        }
    st.pills(
            "Gender at Birth",
            options=gender_map.keys(),
            format_func=lambda option: gender_map[option],
            selection_mode="single",
            key="user_gender"
        )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.number_input("Age (years)", 
                       value=None,
                       min_value=0, 
                       step=1, 
                       key="user_age")

        st.number_input("Weight (kg)", 
                       value=None,
                       min_value=0.0, 
                       step=0.1, 
                       format="%.1f", 
                       key="user_weight")

    with col2:     
        st.number_input("Height (cm)", 
                       value=None,
                       min_value=0.0, 
                       step=0.1, 
                       format="%.1f", 
                       key="user_height")
        
        st.number_input("Waist Circumference (cm)", 
                       value=None,
                       min_value=0.0, 
                       step=0.1, 
                       format="%.1f", 
                       key="user_waist")

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

def create_lifestyle_factors_section():
    """Create the Lifestyle Factors section of the form."""
    st.subheader("Lifestyle Factors")

    st.write("### Smoking History")
    smoked_100 = st.pills(
        "Have you ever smoked 100 cigarettes in life?",
        options=tf_map.keys(),
        format_func=lambda option: tf_map[option],
        selection_mode="single",
        key="smoked_100"
    )
    
    # Always render the follow-up question (we'll validate on submit)
    st.selectbox(
        "How often do you currently smoke?",
        options=["", "Every day", "Some days", "Not at all"],
        key="smoking_frequency"
    )

    # Alcohol consumption section
    st.write("### Alcohol Consumption")
    st.slider(
        "How many days per year do you drink any type of alcoholic beverage? (past 12 months)",
        min_value=0,
        max_value=365,
        value=0,
        key="alq121"
    )