# Constants for form field definitions
REQUIRED_FIELDS = [
    ("Age", "user_age", "years"),
    ("Height", "user_height", "cm"),
    ("Weight", "user_weight", "kg"),
    ("Waist Circumference", "user_waist", "cm"),
    ("Systolic BP", "user_systolic", "mmHg"),
    ("Diastolic BP", "user_diastolic", "mmHg")
]

def ok_float(val):
    """Validate if a value is a positive float."""
    try:
        return float(val) > 0
    except Exception:
        return False

def validate_form_input(st):
    """Validate all required form inputs."""
    # Build required fields dictionary
    required_fields = {
        name: st.session_state.get(key)
        for name, key, _ in REQUIRED_FIELDS
    }
    required_fields["Gender"] = st.session_state.get("user_gender")
    
    # Check required numeric fields
    missing_fields = [
        field for field, value in required_fields.items() 
        if not ok_float(value) if field != "Gender"
    ]
    
    # Check gender selection
    if not st.session_state.get("user_gender"):
        missing_fields.append("Gender")
    
    return missing_fields

def collect_form_values(st):
    """Collect and format all form values."""
    values = {}
    
    # Add required fields
    for name, key, unit in REQUIRED_FIELDS:
        values[f"{name} ({unit})"] = float(st.session_state.get(key))
    
    # Add gender
    values["Gender"] = st.session_state.get("user_gender")
    
    # Add blood pressure as combined value
    sys_bp = values.pop("Systolic BP (mmHg)")
    dia_bp = values.pop("Diastolic BP (mmHg)")
    values["Blood Pressure"] = f"{sys_bp}/{dia_bp}"
    
    # Add optional HbA1c
    hba1c = st.session_state.get("user_hba1c")
    values["HbA1c (%)"] = float(hba1c) if ok_float(hba1c) else "Not provided"
    
    return values