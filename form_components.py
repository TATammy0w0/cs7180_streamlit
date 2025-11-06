import streamlit as st

def create_basic_info_section():
    """Create the Basic Information section of the form."""
    st.subheader("Basic Information")
    col1, col2 = st.columns(2)
    
    with col1:
        st.number_input("Age (years)", 
                       value=None,
                       min_value=0, 
                       step=1, 
                       key="user_age",
                       help="Required: Enter your age in years")

        st.number_input("Height (cm)", 
                       value=None,
                       min_value=0.0, 
                       step=0.1, 
                       format="%.1f", 
                       key="user_height",
                       help="Required: Enter your height in centimeters")
        
        st.number_input("Waist Circumference (cm)", 
                       value=None,
                       min_value=0.0, 
                       step=0.1, 
                       format="%.1f", 
                       key="user_waist",
                       help="Required: Enter your waist circumference in centimeters")

    with col2:
        st.selectbox("Gender at Birth",
                    options=["", "Male", "Female"],
                    index=0,
                    key="user_gender",
                    help="Required: Select your gender at birth")
        
        st.number_input("Weight (kg)", 
                       value=None,
                       min_value=0.0, 
                       step=0.1, 
                       format="%.1f", 
                       key="user_weight",
                       help="Required: Enter your weight in kilograms")

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
                       key="user_systolic",
                       help="Required: Enter your systolic blood pressure")
    
    with bp_col2:
        st.number_input("Diastolic Blood Pressure", 
                       value=None,
                       min_value=0.0, 
                       step=1.0, 
                       format="%.1f", 
                       key="user_diastolic",
                       help="Required: Enter your diastolic blood pressure")

    st.number_input("HbA1c (%)", 
                   value=None,
                   min_value=0.0, 
                   step=0.1, 
                   format="%.1f", 
                   key="user_hba1c",
                   help="Optional: Enter your HbA1c value if available")