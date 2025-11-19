from utils.constants import ALCOHOL_CONSUMPTION_RANGE, FAIMILY_INCOME_MAP, PHYSICAL_ACTIVITY_MAP, RACE_MAP,REQUIRED_FIELDS, OPTIONAL_FIELDS, SMOKING_FREQUENCY_MAP


def compute_bmi(weight_kg, height_cm):
    if weight_kg is None or height_cm is None or height_cm == 0:
        return None
    try:
        height_m = float(height_cm) / 100.0
        bmi = float(weight_kg) / (height_m ** 2)
        return round(bmi, 2)
    except Exception:
        return None


def format_post_data(required_features, optional_features):
    """Format the collected form values into the expected POST data structure."""
    data = {}
    
    # Add required fields
    for field_name in required_features.keys():
        value = required_features.get(field_name)
        data[field_name] = value
    
    # Add optional fields
    for field_name in optional_features.keys():
        value = optional_features.get(field_name)
        data[field_name] = value
    
    return data


def validate_form_input(st):
    """Validate all required form inputs. Returns dict mapping field keys to human-readable labels for missing fields."""
    missing_fields = {}
    
    for field_name, field_key in REQUIRED_FIELDS.items():
        value = st.session_state.get(field_key)

        if value is None:
            missing_fields[field_key] = field_name

    return missing_fields


def collect_form_values(st, required_fields_map, optional_fields_map):
    
    field_pending_processing = {"Weight", "Height", "Race", "Annual Family Income", "Smoking Frequency", "Alcohol", "Physical Activity"}

    # Add all required fields
    for field_name in REQUIRED_FIELDS.keys():
        # safety check
        key = REQUIRED_FIELDS[field_name]
        if key in st.session_state:
            value = st.session_state.get(key)

        if field_name in field_pending_processing:
            # Handled separately below
            continue
        else:
            required_fields_map.update(key, value)
    
    # Add all optional fields (None if not provided)
    for field_name in OPTIONAL_FIELDS.keys():
        key = OPTIONAL_FIELDS[field_name]
        if key in st.session_state:
            value = st.session_state.get(key)
        
        if field_name in field_pending_processing:
            # Handled separately below
            continue
        else:
            optional_fields_map.update(key, value)

    _update_bmi(required_fields_map, st)
    _update_race_field(required_fields_map, st)
    _update_family_income_field(optional_fields_map, st)
    _update_smoking_fields(required_fields_map, st)
    _update_alcohol_field(required_fields_map, st)
    _update_physical_activity_field(required_fields_map, st)


# helper functions
def _update_bmi(fields_map, st):
    """Update the BMI value in the required fields map based on weight and height."""
    weight = st.session_state.get(REQUIRED_FIELDS["Weight"])
    height = st.session_state.get(REQUIRED_FIELDS["Height"])
    bmi = compute_bmi(weight, height)

    fields_map.update("BMXBMI", bmi)


def _update_smoking_fields(fields_map, st):
    # Add smoking-related fields (SMQ020 and SMQ040)
    smoked_200 = st.session_state.get(REQUIRED_FIELDS["Smoking History"])
    smoking_frequency = st.session_state.get(REQUIRED_FIELDS["Smoking Frequency"], "")
    
    # SMQ040: Current smoking frequency
    # Only set if user answered "Yes" (1) to smoking 100 cigarettes
    if smoked_200 == 1:
        # User smoked 100 cigarettes - map their current frequency
        fields_map.update("SMQ040", SMOKING_FREQUENCY_MAP.get(smoking_frequency))
    else:
        # Code 0 used to indicate 'never/currently not smoking' per earlier conventions
        fields_map.update("SMQ040", 0)

def _update_alcohol_field(fields_map, st):
    _update_field_with_mapping(True, fields_map, "Alcohol", ALCOHOL_CONSUMPTION_RANGE, st)

def _update_physical_activity_field(fields_map, st):
    _update_field_with_mapping(True, fields_map, "Physical Activity", PHYSICAL_ACTIVITY_MAP, st)

def _update_race_field(fields_map, st):
    _update_field_with_mapping(True, fields_map, "Race", RACE_MAP, st)

def _update_family_income_field(fields_map, st):
    _update_field_with_mapping(False, fields_map, "Annual Family Income", FAIMILY_INCOME_MAP, st)

def _update_field_with_mapping(is_required, fields_map, field_name, mapping_dict, st):
    """Update a field in the fields map using a provided mapping dictionary."""
    nhanes_key = REQUIRED_FIELDS[field_name] if is_required else OPTIONAL_FIELDS[field_name]
    user_input = st.session_state.get(nhanes_key, "")
    mapped_value = mapping_dict.get(user_input)
    fields_map.update(nhanes_key, mapped_value)