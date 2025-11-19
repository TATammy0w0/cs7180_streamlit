import streamlit as st
from utils.constants import GENDER_MAP, OPTIONAL_FIELDS, TF_MAP, REQUIRED_FIELDS

def create_basic_info_section():
    """Create the Basic Information section of the form."""
    st.subheader("Basic Information")
    
    validation_errors = st.session_state.get('validation_errors', {})
    
    st.pills(
            "\* Gender at Birth",
            options=GENDER_MAP.keys(),
            format_func=lambda option: GENDER_MAP[option],
            selection_mode="single",
            key=REQUIRED_FIELDS["Gender"]
        )
    if REQUIRED_FIELDS["Gender"] in validation_errors and st.session_state.get(REQUIRED_FIELDS["Gender"]) is None:
        st.error(f"⚠️ {validation_errors[REQUIRED_FIELDS['Gender']]} is required")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.number_input("\* Age (years)", 
                       value=None,
                       min_value=1, 
                       step=1, 
                       key=REQUIRED_FIELDS["Age"])
        if REQUIRED_FIELDS["Age"] in validation_errors and st.session_state.get(REQUIRED_FIELDS["Age"]) is None:
            st.error(f"⚠️ {validation_errors[REQUIRED_FIELDS['Age']]} is required")

        st.number_input("\* Weight (kg)", 
                       value=None,
                       min_value=1.0, 
                       step=0.1, 
                       format="%.1f", 
                       key=REQUIRED_FIELDS["Weight"])
        if REQUIRED_FIELDS["Weight"] in validation_errors and st.session_state.get(REQUIRED_FIELDS["Weight"]) is None:
            st.error(f"⚠️ {validation_errors[REQUIRED_FIELDS['Weight']]} is required")
        
        st.selectbox("\* Race", 
                      options=["Mexican American", "Other Hispanic", "Non-Hispanic White", "Non-Hispanic Black", "Non-Hispanic Asian", "Other Race/Multiracial"],    
                      index=None,
                      key=REQUIRED_FIELDS["Race"])
        if REQUIRED_FIELDS["Race"] in validation_errors and st.session_state.get(REQUIRED_FIELDS["Race"]) is None:
            st.error(f"⚠️ {validation_errors[REQUIRED_FIELDS['Race']]} is required")

    with col2:     
        st.number_input("\* Height (cm)", 
                       value=None,
                       min_value=1.0, 
                       step=0.1, 
                       format="%.1f", 
                       key=REQUIRED_FIELDS["Height"])
        if REQUIRED_FIELDS["Height"] in validation_errors and st.session_state.get(REQUIRED_FIELDS["Height"]) is None:
            st.error(f"⚠️ {validation_errors[REQUIRED_FIELDS['Height']]} is required")

        st.number_input("\* Waist Circumference (cm)", 
                       value=None,
                       min_value=1.0, 
                       step=0.1, 
                       format="%.1f", 
                       key=REQUIRED_FIELDS["Waist"])
        if REQUIRED_FIELDS["Waist"] in validation_errors and st.session_state.get(REQUIRED_FIELDS["Waist"]) is None:
            st.error(f"⚠️ {validation_errors[REQUIRED_FIELDS['Waist']]} is required")
        
        st.selectbox("Annual Family Income", 
                      options=["Less than $30k", "$30k to less than $45k", "$45k to less than $60k", "$60k to less than $120k", "$120k or more"],    
                      index=None,
                      key=OPTIONAL_FIELDS["Annual Family Income"])

def create_lifestyle_factors_section():
    """Create the Lifestyle Factors section of the form."""
    st.subheader("Lifestyle Factors")
    
    validation_errors = st.session_state.get('validation_errors', {})

    st.write("##### * Physical Activity")
    st.selectbox(
        "On average, how much time do you spend on sedentary activities (e.g., sitting, reclining, watching TV) everyday?",
        options=["Less than 1 hour", "1-2 hours", "2-4 hours", "4-6 hours", "6-8 hours", "8-10 hours", "More than 10 hours"],
        index=None,
        key=REQUIRED_FIELDS["Physical Activity"]
    )
    if REQUIRED_FIELDS["Physical Activity"] in validation_errors and st.session_state.get(REQUIRED_FIELDS["Physical Activity"]) is None:
        st.error(f"⚠️ {validation_errors[REQUIRED_FIELDS['Physical Activity']]} is required")

    st.write("##### * Smoking History")
    st.pills(
        "Have you ever smoked 100 cigarettes in life?",
        options=TF_MAP.keys(),
        format_func=lambda option: TF_MAP[option],
        selection_mode="single",
        key=REQUIRED_FIELDS["Smoking History"]
    )
    if REQUIRED_FIELDS["Smoking History"] in validation_errors and st.session_state.get(REQUIRED_FIELDS["Smoking History"]) is None:
        st.error(f"⚠️ {validation_errors[REQUIRED_FIELDS['Smoking History']]} is required")
    
    # Always render the follow-up question
    st.selectbox(
        "How often do you currently smoke?",
        options=["Every day", "Some days", "Not at all"],
        index=None,
        key=REQUIRED_FIELDS["Smoking Frequency"]
    )
    if REQUIRED_FIELDS["Smoking Frequency"] in validation_errors and st.session_state.get(REQUIRED_FIELDS["Smoking Frequency"]) is None:
        st.error(f"⚠️ {validation_errors[REQUIRED_FIELDS['Smoking Frequency']]} is required")

    # Alcohol consumption section
    st.write("##### * Alcohol Consumption")
    st.selectbox(
        "How often do you currently drink alcohol?",
        options=["Never", "Less than 1 day per month", "1-2 days per month", "3-4 days per month", "2-3 days per week", "4-5 days per week", "Nearly every day/Everyday"],
        index=None,
        key=REQUIRED_FIELDS["Alcohol"]
    )
    if REQUIRED_FIELDS["Alcohol"] in validation_errors and st.session_state.get(REQUIRED_FIELDS["Alcohol"]) is None:
        st.error(f"⚠️ {validation_errors[REQUIRED_FIELDS['Alcohol']]} is required")

def create_lab_values_section():
    """Create the Laboratory Values section of the form."""
    st.subheader("Laboratory Values")
    
    _bp_section()
    
    other_col1, other_col2 = st.columns(2)
    with other_col1:
        st.number_input("HbA1c (%)", 
                   value=None,
                   min_value=0.0, 
                   max_value=100.0,
                   step=0.1, 
                   format="%.1f", 
                   help="Normal: <5.7%",
                   key=OPTIONAL_FIELDS["HbA1c"])
        
        st.number_input("Triglycerides (mg/dL)", 
                   value=None,
                   min_value=0.0, 
                   step=0.1, 
                   format="%.1f", 
                   help="Normal: <150 mg/dL",
                   key=OPTIONAL_FIELDS["Triglycerides"])
        
        st.number_input("LDL Cholesterol (mg/dL)", 
                   value=None,
                   min_value=0.0, 
                   step=0.1, 
                   format="%.1f", 
                   help="Optimal: <100 mg/dL",
                   key=OPTIONAL_FIELDS["LDL Cholesterol"])

        st.number_input("Total Cholesterol (mg/dL)", 
                   value=None,
                   min_value=0.0, 
                   step=0.1, 
                   format="%.1f", 
                   help="Desirable: <200 mg/dL",
                   key=OPTIONAL_FIELDS["Total Cholesterol"])
        
        st.number_input("Alanine aminotransferase (ALT) (U/L)",
                   value=None,
                   min_value=0.0, 
                   step=0.1, 
                   format="%.1f", 
                   help="Normal: 7-56 U/L",
                   key=OPTIONAL_FIELDS["ALT"])

    with other_col2:
        st.number_input("Fasting Glucose (mg/dL)", 
                   value=None,
                   min_value=0.0, 
                   step=0.1, 
                   format="%.1f", 
                   help="Normal: 70-99 mg/dL",
                   key=OPTIONAL_FIELDS["Fasting Glucose"])

        st.number_input("FVC (mL)", 
                   value=None,
                   min_value=0.0, 
                   step=0.1, 
                   format="%.1f", 
                   help="Typical: 3,500-4,500 mL",
                   key=OPTIONAL_FIELDS["FVC"])

        st.number_input("HDL Cholesterol (mg/dL)", 
                   value=None,
                   min_value=0.0, 
                   step=0.1, 
                   format="%.1f", 
                   help="Normal: 40-59 mg/dL",
                   key=OPTIONAL_FIELDS["HDL Cholesterol"])
        
        st.number_input("Uric Acid (mg/dL)", 
                   value=None,
                   min_value=0.0, 
                   step=0.1, 
                   format="%.1f", 
                   help="Normal: 3.5-7.2 mg/dL",
                   key=OPTIONAL_FIELDS["Uric Acid"])

def create_medical_history_section():
    """Create the Medical History section of the form."""
    st.subheader("Medical History")
    
    validation_errors = st.session_state.get('validation_errors', {})

    st.write("##### * Cancer History")
    st.pills(
        "Have you ever been told you had any kind of cancer?",
        options=TF_MAP.keys(),
        format_func=lambda option: TF_MAP[option],
        selection_mode="single",
        key=REQUIRED_FIELDS["Cancer History"]
    )
    if REQUIRED_FIELDS["Cancer History"] in validation_errors and st.session_state.get(REQUIRED_FIELDS["Cancer History"]) is None:
        st.error(f"⚠️ {validation_errors[REQUIRED_FIELDS['Cancer History']]} is required")

    st.write("##### * Angina History")
    st.pills(
        "Have you ever been told you had angina/angina pectoris?",
        options=TF_MAP.keys(),
        format_func=lambda option: TF_MAP[option],
        selection_mode="single",
        key=REQUIRED_FIELDS["Angina History"]
    )
    if REQUIRED_FIELDS["Angina History"] in validation_errors and st.session_state.get(REQUIRED_FIELDS["Angina History"]) is None:
        st.error(f"⚠️ {validation_errors[REQUIRED_FIELDS['Angina History']]} is required")

    st.write("##### * COPD History")
    st.pills(
        "Have you ever been told you had COPD, emphysema, or chronic bronchitis?",
        options=TF_MAP.keys(),
        format_func=lambda option: TF_MAP[option],
        selection_mode="single",
        key=REQUIRED_FIELDS["COPD History"]
    )
    if REQUIRED_FIELDS["COPD History"] in validation_errors and st.session_state.get(REQUIRED_FIELDS["COPD History"]) is None:
        st.error(f"⚠️ {validation_errors[REQUIRED_FIELDS['COPD History']]} is required")

    st.write("##### * Arthritis History")
    st.pills(
        "Have you ever been told you had arthritis?",
        options=TF_MAP.keys(),
        format_func=lambda option: TF_MAP[option],
        selection_mode="single",
        key=REQUIRED_FIELDS["Arthritis History"]
    )
    if REQUIRED_FIELDS["Arthritis History"] in validation_errors and st.session_state.get(REQUIRED_FIELDS["Arthritis History"]) is None:
        st.error(f"⚠️ {validation_errors[REQUIRED_FIELDS['Arthritis History']]} is required")

    st.write("##### * Metal Objects")
    st.pills(
        "Do you have any metal objects inside your body?",
        options=TF_MAP.keys(),
        format_func=lambda option: TF_MAP[option],
        selection_mode="single",
        key=REQUIRED_FIELDS["Metal Objects"]
    )
    if REQUIRED_FIELDS["Metal Objects"] in validation_errors and st.session_state.get(REQUIRED_FIELDS["Metal Objects"]) is None:
        st.error(f"⚠️ {validation_errors[REQUIRED_FIELDS['Metal Objects']]} is required")

    st.write("##### Diabetes History")
    st.pills(
        "Have you ever been told you had diabetes?",
        options=TF_MAP.keys(),
        format_func=lambda option: TF_MAP[option],
        selection_mode="single",
        key=OPTIONAL_FIELDS["Diabetes History"]
    )

    st.write("##### High Blood Pressure History")
    st.pills(
        "Have you ever been told you had high blood pressure?",
        options=TF_MAP.keys(),
        format_func=lambda option: TF_MAP[option],
        selection_mode="single",
        key=OPTIONAL_FIELDS["High Blood Pressure History"]
    )

def _bp_section():
    # Systolic Blood Pressure Section
    st.markdown("Systolic Blood Pressure Readings (mmHg)", unsafe_allow_html=False, help="Please provide four readings.")
    sbp_col1, sbp_col2, sbp_col3, sbq_col4 = st.columns(4)
    
    with sbp_col1:
        st.number_input("Systolic Blood Pressure 1",
                       value=None,
                       min_value=0.0, 
                       step=1.0, 
                       format="%.1f", 
                       label_visibility="collapsed",
                       key=OPTIONAL_FIELDS["Systolic Blood Pressure 1"])
    
    with sbp_col2:
        st.number_input("Systolic Blood Pressure 2", 
                       value=None,
                       min_value=0.0, 
                       step=1.0, 
                       format="%.1f", 
                       label_visibility="collapsed",
                       key=OPTIONAL_FIELDS["Systolic Blood Pressure 2"])
    
    with sbp_col3:
        st.number_input("Systolic Blood Pressure 3", 
                       value=None,
                       min_value=0.0, 
                       step=1.0, 
                       format="%.1f", 
                       label_visibility="collapsed",
                       key=OPTIONAL_FIELDS["Systolic Blood Pressure 3"])

    with sbq_col4:
        st.number_input("Systolic Blood Pressure 4", 
                       value=None,
                       min_value=0.0, 
                       step=1.0, 
                       format="%.1f", 
                       label_visibility="collapsed",
                       key=OPTIONAL_FIELDS["Systolic Blood Pressure 4"])

    # Diastolic Blood Pressure Section
    st.markdown("Diastolic Blood Pressure Readings (mmHg)", unsafe_allow_html=False, help="Please provide four readings.")
    dbp_col1, dbp_col2, dbp_col3, dbp_col4 = st.columns(4)

    with dbp_col1:
        st.number_input("Diastolic Blood Pressure 1",
                       value=None,
                       min_value=0.0, 
                       step=1.0, 
                       format="%.1f", 
                       label_visibility="collapsed",
                       key=OPTIONAL_FIELDS["Diastolic Blood Pressure 1"])
    
    with dbp_col2:
        st.number_input("Diastolic Blood Pressure 2", 
                       value=None,
                       min_value=0.0, 
                       step=1.0, 
                       format="%.1f", 
                       label_visibility="collapsed",
                       key=OPTIONAL_FIELDS["Diastolic Blood Pressure 2"])
    
    with dbp_col3:
        st.number_input("Diastolic Blood Pressure 3",
                        value=None,
                        min_value=0.0, 
                        step=1.0, 
                        format="%.1f", 
                        label_visibility="collapsed",
                        key=OPTIONAL_FIELDS["Diastolic Blood Pressure 3"])

    with dbp_col4: 
        st.number_input("Diastolic Blood Pressure 4",
                        value=None,
                        min_value=0.0,    
                        step=1.0, 
                        format="%.1f", 
                        label_visibility="collapsed",
                        key=OPTIONAL_FIELDS["Diastolic Blood Pressure 4"])