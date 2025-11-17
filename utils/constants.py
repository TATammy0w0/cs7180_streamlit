REQUIRED_FIELDS = {
    "Age": "RIDAGEYR",              # Age
    "Gender": "RIAGENDR",           # Gender
    "Weight": "Weight",             # Weight
    "Height": "Height",             # Height
    "Waist": "BMXWAIST",            # Waist circumference
    "Alcohol": "ALQ121",            # Alcohol consumption (days drank in past 12 months)
    "Smoking History": "SMQ020",    # Ever Smoked
    "Smoking Frequency": "SMQ040",  # Current Smoking Status
    "Physical Activity": "PAD680",  # Physical activity
    "Metal Objects": "OSQ230",      # Any metal objects inside body
    "Cancer History": "MCQ500",     # Ever told you had any kind of cancer
    "Angina History": "MCQ160D",    # Ever told you had angina/angina pectoris
    "COPD History": "MCQ160P",      # Ever told you had COPD, emphysema, or chronic bronchitis
    "Arthritis History": "MCQ160A"  # Ever told you had arthritis
}

OPTIONAL_FIELDS = {
    "Systolic Blood Pressure 1": "BPXSY1",  # Systolic Blood Pressure
    "Systolic Blood Pressure 2": "BPXSY2",  # Systolic Blood Pressure
    "Systolic Blood Pressure 3": "BPXSY3",  # Systolic Blood Pressure
    "Systolic Blood Pressure 4": "BPXSY4",  # Systolic Blood Pressure
    "Diastolic Blood Pressure 1": "BPXDI1",  # Diastolic Blood
    "Diastolic Blood Pressure 2": "BPXDI2",  # Diastolic Blood
    "Diastolic Blood Pressure 3": "BPXDI3",  # Diastolic Blood
    "Diastolic Blood Pressure 4": "BPXDI4",  # Diastolic Blood
    "HbA1c": "LBXGH",   # HbA1c
    "Fasting Glucose": "LBXGLU",  # Fasting Glucose
    "Triglycerides": "LBXSTR",  # Triglycerides
    "FVC": "LUXCAPM",  # FVC
    "LDL Cholesterol": "LBDLDL",  # LDL Cholesterol
    "HDL Cholesterol": "LBDHDD",  # HDL Cholesterol
    "Total Cholesterol": "LBXTC",  # Total Cholesterol
    "ALT": "LBXSATSI",  # Alanine aminotransferase
    "Uric Acid": "LBXSUA",  # Uric Acid
    "Diabetes History": "DIQ010",  # Ever told you had diabetes
    "High Blood Pressure History": "BPQ020",  # Ever told you had high blood pressure
}

DERIVED_INPUT_LABELS = {"Weight", "Height"}

REQUIRED_FEATURE_SET = {
    code for label, code in REQUIRED_FIELDS.items()
    if label not in DERIVED_INPUT_LABELS
}
REQUIRED_FEATURE_SET.add("BMXBMI")

OPTIONAL_FEATURE_SET = {
    code for label, code in OPTIONAL_FIELDS.items()
    if label not in DERIVED_INPUT_LABELS
}

TF_MAP = {
    1: "Yes",
    2: "No"
}

GENDER_MAP = {
    1: "Male",
    2: "Female"
}

# Smoking frequency mapping
SMOKING_FREQUENCY_MAP = {
    "": None,
    "Every day": 1,
    "Some days": 2,
    "Not at all": 3,
}

PHYSICAL_ACTIVITY_MAP = {
    "": None,
    "Less than 1 hour": 30,
    "1-2 hours": 90,
    "2-4 hours": 180,
    "4-6 hours": 300,
    "6-8 hours": 420,
    "8-10 hours": 540,
    "More than 10 hours": 720
}

ALCOHOL_CONSUMPTION_RANGE = {
    "": None,
    "Never": 0,
    "Less than 1 day per month": 10,
    "1-2 days per month": 18,
    "3-4 days per month": 42,
    "2-3 days per week": 130,
    "4-5 days per week": 240,
    "Nearly every day/Everyday": 300
}