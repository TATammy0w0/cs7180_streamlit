# Constants for form field definitions
REQUIRED_FIELDS = [
    ("RIDAGEYR", "user_age"),
    ("Height", "user_height"),
    ("Weight", "user_weight"),
    ("BMXWAIST", "user_waist"),
    ("RIAGENDR", "user_gender"),
    ("ALQ121", "alq121"),
]

OPTIONAL_FIELDS = [
    ("Systolic Pressure", "user_systolic"),
    ("Diastolic Pressure", "user_diastolic"),
    ("LBXGH", "user_hba1c"),
]

# Smoking frequency mapping
SMOKING_FREQUENCY_MAP = {
    "Every day": 1,
    "Some days": 2,
    "Not at all": 3,
}

def ok_float(val):
    """Validate if a value is a positive float."""
    try:
        return float(val) > 0
    except Exception:
        return False

def validate_form_input(st):
    """Validate all required form inputs."""
    missing_fields = []
    
    for field_name, field_key in REQUIRED_FIELDS:
        value = st.session_state.get(field_key)
        
        if value is None or not ok_float(value): 
            missing_fields.append(field_name)
    
    return missing_fields

def collect_form_values(st):
    """Collect and format all form values."""
    values = {}
    
    # Add all required fields
    for field_name, field_key in REQUIRED_FIELDS:
        value = st.session_state.get(field_key)
        # Convert to float for numeric fields, keep as-is for Gender (1 or 2)
        if field_name == "Gender":
            values[field_name] = value  # Will be 1 (Male) or 2 (Female)
        else:
            values[field_name] = float(value) if value is not None else None
    
    # Add all optional fields (None if not provided)
    for field_name, field_key in OPTIONAL_FIELDS:
        value = st.session_state.get(field_key)
        values[field_name] = float(value) if ok_float(value) else None
    
    # Add smoking-related fields (SMQ020 and SMQ040)
    smoked_100 = st.session_state.get("smoked_100")  # Integer from pills (1=Yes, 2=No, None=not selected)
    smoking_frequency = st.session_state.get("smoking_frequency", "")
    
    # SMQ020: Ever smoked 100 cigarettes
    values["SMQ020"] = smoked_100  # 1=Yes, 2=No, None=not selected
    
    # SMQ040: Current smoking frequency
    # Only set if user answered "Yes" (1) to smoking 100 cigarettes
    if smoked_100 == 1:
        # User smoked 100 cigarettes - map their current frequency
        values["SMQ040"] = SMOKING_FREQUENCY_MAP.get(smoking_frequency)
    elif smoked_100 == 2:
        # User never smoked 100 cigarettes - default to 0
        values["SMQ040"] = 0
    else:
        # User didn't answer the smoking history question
        values["SMQ040"] = None
    
    return values