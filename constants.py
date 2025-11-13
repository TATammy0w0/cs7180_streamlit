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
    "HbA1c": "LBXGH"   # HbA1c
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

# Smoking frequency mapping
SMOKING_FREQUENCY_MAP = {
    "Every day": 1,
    "Some days": 2,
    "Not at all": 3,
}

TF_MAP = {
    1: "Yes",
    2: "No"
}

GENDER_MAP = {
    1: "Male",
    2: "Female"
}

ALCOHOL_CONSUMPTION_RANGE = {
    "Never": 0,
    "Less than 1 day per month": 10,
    "1-2 days per month": 18,
    "3-4 days per month": 42,
    "2-3 days per week": 130,
    "4-5 days per week": 240,
    "Nearly every day/Everyday": 300
}