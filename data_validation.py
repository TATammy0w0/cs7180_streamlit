from constants import REQUIRED_FIELDS, OPTIONAL_FIELDS, SMOKING_FREQUENCY_MAP

def ok_float(val):
    """Return True if val can be interpreted as a positive float (greater than 0).

    Accepts ints/floats and numeric-like strings. Returns False for None or non-numeric.
    """
    try:
        return float(val) > 0
    except Exception:
        return False


def compute_bmi(weight_kg, height_cm):
    if weight_kg is None or height_cm is None or height_cm == 0:
        return None
    try:
        height_m = float(height_cm) / 100.0
        bmi = float(weight_kg) / (height_m ** 2)
        return round(bmi, 2)
    except Exception:
        return None


def format_post_data(required_values, optional_values):
    """Format the collected form values into the expected POST data structure."""
    data = {}
    
    # Add required fields
    for field_name in required_values.keys():
        if field_name == "Height" or field_name == "Weight":
            continue  # Skip these as they are used to compute BMI
        value = required_values.get(field_name)
        data[field_name] = value
    
    # Add optional fields
    for field_name in optional_values.keys():
        value = optional_values.get(field_name)
        data[field_name] = value
    
    # Compute BMI and add it
    bmi = compute_bmi(required_values.get("Weight"), required_values.get("Height"))
    data["BMXBMI"] = bmi
    
    return data


def validate_form_input(st):
    """Validate all required form inputs."""
    missing_fields = []
    
    for field_name in REQUIRED_FIELDS:
        value = st.session_state.get(REQUIRED_FIELDS[field_name])

        if value is None or not ok_float(value):
            missing_fields.append(field_name)

    return missing_fields

def collect_form_values(st, required_fields_map, optional_fields_map):
    
    # Add all required fields
    for field_name in REQUIRED_FIELDS.keys():
        # safety check
        key = REQUIRED_FIELDS[field_name]
        if key in st.session_state:
            value = st.session_state.get(key)

        if field_name == "Weight" or field_name == "Height" or field_name == "SMQ020" or field_name == "SMQ040":
            # Handled separately below
            continue
        else:
            required_fields_map.update(key, value)
    
    # Add all optional fields (None if not provided)
    for field_name in OPTIONAL_FIELDS.keys():
        key = OPTIONAL_FIELDS[field_name]
        if key in st.session_state:
            value = st.session_state.get(key)
        optional_fields_map.update(key, value)


    required_fields_map.update("BMXBMI", compute_bmi(
        st.session_state.get(REQUIRED_FIELDS["Weight"]),
        st.session_state.get(REQUIRED_FIELDS["Height"])
    ))

    # Add smoking-related fields (SMQ020 and SMQ040)
    smoked_200 = st.session_state.get(REQUIRED_FIELDS["Smoking History"])
    smoking_frequency = st.session_state.get(REQUIRED_FIELDS["Smoking Frequency"], "")
    
    # SMQ020: Ever smoked 100 cigarettes
    required_fields_map.update("SMQ020", smoked_200)  # 1=Yes, 2=No, None=not selected
    
    # SMQ040: Current smoking frequency
    # Only set if user answered "Yes" (1) to smoking 100 cigarettes
    if smoked_200 == 1:
        # User smoked 100 cigarettes - map their current frequency
        required_fields_map.update("SMQ040", SMOKING_FREQUENCY_MAP.get(smoking_frequency))
    else:
        # Code 0 used to indicate 'never/currently not smoking' per earlier conventions
        required_fields_map.update("SMQ040", 0)