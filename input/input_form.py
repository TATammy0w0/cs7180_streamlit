import streamlit as st
import requests
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.constants import REQUIRED_FEATURE_SET, OPTIONAL_FEATURE_SET
from models.feature_map import FeatureMap
from input.form_components import create_basic_info_section, create_lab_values_section, create_lifestyle_factors_section, create_medical_history_section
from input.data_validation import format_post_data, validate_form_input, collect_form_values
from utils.display import convert_api_response_to_display_format

# 支持环境变量配置，本地开发时设置为 http://localhost:8000
API_BASE_URL = os.getenv("API_BASE_URL", "https://disease-warning-1.onrender.com")
PREDICT_ALL_URL = f"{API_BASE_URL}/prediction/all"

required_features_map = FeatureMap(REQUIRED_FEATURE_SET)
optional_features_map = FeatureMap(OPTIONAL_FEATURE_SET)

def input_form():
    with st.form("risk_form"):
        _draw_forms()
        
        submitted = st.form_submit_button(
            "Submit", 
            type="primary",
            use_container_width=True
        )

        if submitted:
            missing_fields = validate_form_input(st)
            
            if missing_fields:
                # Store missing fields in session state for rendering feedback
                st.session_state['validation_errors'] = missing_fields
                st.error(f"⚠️ Please fill in all required fields highlighted above ({len(missing_fields)} missing)")
            else:
                # Clear any previous validation errors
                st.session_state['validation_errors'] = {}
                collect_form_values(st, required_features_map, optional_features_map)
                input = format_post_data(required_features_map, optional_features_map)
                data = {"input_data": input}
                st.error(f"Please fill in all required fields: {', '.join(missing_fields)}")
            else:
                with st.spinner("Processing your health data..."):
                    collect_form_values(st, required_features_map, optional_features_map)
                    input = format_post_data(required_features_map, optional_features_map)
                    data = {"input_data": input}

                    try:
                        response = requests.post(PREDICT_ALL_URL, json=data, timeout=30)

                        if response.status_code == 200:
                            api_response = response.json()
                            
                            # Convert API response to frontend format
                            converted_response = _convert_api_to_frontend_format(api_response)
                            
                            # Convert to display format
                            display_data = convert_api_response_to_display_format(converted_response)
                            
                            # Save to session state
                            st.session_state.prediction_done = True
                            st.session_state.risk_scores = display_data["risk_scores"]
                            st.session_state.risk_factors_by_disease = display_data["risk_factors_by_disease"]
                            st.session_state.factor_recommendations_map = display_data["factor_recommendations_map"]
                            st.session_state.comparison_data = display_data["comparison_data"]
                            st.session_state.comparison_data_by_disease = display_data["comparison_data_by_disease"]
                            st.session_state.selected_disease = None
                            
                            # Redirect to results page
                            st.success("✅ Prediction completed! Redirecting to results...")
                            st.switch_page("pages/Prediction_Results.py")
                        else:
                            st.error("API request failed")
                            try:
                                error_data = response.json()
                                st.json(error_data)
                            except requests.exceptions.JSONDecodeError:
                                st.text(response.text)

                    except requests.exceptions.ConnectionError as e:
                        st.error(f"Connection failed: {e}. Please make sure the backend service is running.")
                    except requests.exceptions.Timeout:
                        st.error("Request timed out. Please try again.")
                    except Exception as e:
                        st.error(f"An error occurred: {str(e)}")

def _convert_api_to_frontend_format(api_response):
    """
    Convert API response format to frontend expected format.
    
    API format:
    {
        "model_routing": {...},
        "ckd": {
            "prediction": 0,
            "confidence": 0.99,
            "risk": 0,
            "shap": {
                "increasing_risk": [...],
                "decreasing_risk": [...]
            },
            "population_comparison": {...}
        },
        ...
    }
    
    Frontend format:
    {
        "diseases": [
            {
                "disease_name": "CKD",
                "disease_type": "ckd",
                "risk_score": 0,
                "confidence_score": 0.99,
                "status": "LOW RISK",
                "top_risk_factors": [...],
                "population_comparison": {...}
            },
            ...
        ]
    }
    """
    diseases = []
    
    # Disease name mapping
    disease_name_map = {
        "ckd": "CKD",
        "diabetes": "Diabetes",
        "hypertension": "Hypertension",
        "cvd": "CVD"
    }
    
    # Risk level mapping
    def get_risk_status(risk_score):
        if risk_score >= 70:
            return "HIGH RISK"
        elif risk_score >= 30:
            return "MODERATE RISK"
        else:
            return "LOW RISK"
    
    # Process each disease in the API response
    for disease_key, disease_data in api_response.items():
        if disease_key == "model_routing" or "error" in disease_data:
            continue
        
        disease_name = disease_name_map.get(disease_key, disease_key.upper())
        risk_score = disease_data.get("risk", 0)
        confidence = disease_data.get("confidence", 0.0)
        status = get_risk_status(risk_score)
        
        # Convert SHAP data to risk factors
        top_risk_factors = []
        shap_data = disease_data.get("shap", {})
        
        # Process increasing risk factors
        increasing_risk = shap_data.get("increasing_risk", [])
        for factor in increasing_risk:
            feature = factor.get("feature", "")
            importance = factor.get("importance", 0)
            modifiable = factor.get("modifiable", False)
            recommendation = factor.get("recommendation", "")
            value = factor.get("value")
            
            # Format feature name (convert code to readable name)
            feature_name = _format_feature_name(feature)
            factor_value = _format_feature_value(feature, value) if value is not None else ""
            
            top_risk_factors.append({
                "factor_name": feature_name,
                "factor_type": feature,
                "factor_value": factor_value,
                "raw_value": value,
                "is_modifiable": modifiable,
                "contribution_score": abs(importance) * 100,  # Convert to percentage-like score
                "category": "exam" if modifiable else "demographic",
                "recommendation": recommendation,  # Include recommendation from API
                "is_increasing_risk": True,  # Mark as increasing risk
                "importance": importance  # Keep original importance value
            })
        
        # Process decreasing risk factors (these are protective factors)
        decreasing_risk = shap_data.get("decreasing_risk", [])
        for factor in decreasing_risk:
            feature = factor.get("feature", "")
            importance = factor.get("importance", 0)
            modifiable = factor.get("modifiable", False)
            recommendation = factor.get("recommendation", "")
            value = factor.get("value")
            
            feature_name = _format_feature_name(feature)
            factor_value = _format_feature_value(feature, value) if value is not None else ""
            
            top_risk_factors.append({
                "factor_name": feature_name,
                "factor_type": feature,
                "factor_value": factor_value,
                "raw_value": value,
                "is_modifiable": modifiable,
                "contribution_score": abs(importance) * 100,
                "category": "exam" if modifiable else "demographic",
                "recommendation": recommendation,  # Include recommendation from API
                "is_increasing_risk": False,  # Mark as decreasing risk (protective)
                "importance": importance  # Keep original importance value
            })
        
        # Sort by contribution score (descending)
        top_risk_factors.sort(key=lambda x: x["contribution_score"], reverse=True)
        
        # Get population comparison
        population_comparison = disease_data.get("population_comparison")
        
        diseases.append({
            "disease_name": disease_name,
            "disease_type": disease_key,
            "risk_score": risk_score,
            "confidence_score": confidence,
            "status": status,
            "top_risk_factors": top_risk_factors,
            "population_comparison": population_comparison
        })
    
    return {"diseases": diseases}


def _format_feature_name(feature_code):
    """Convert feature code to readable name."""
    feature_name_map = {
        "RIDAGEYR": "Age",
        "RIAGENDR": "Gender",
        "BMXBMI": "BMI",
        "BMXWAIST": "Waist Circumference",
        "BPXSY1": "Systolic Blood Pressure",
        "BPXDI1": "Diastolic Blood Pressure",
        "LBXGH": "HbA1c",
        "LBXGLU": "Fasting Glucose",
        "LBDGLUSI": "Fasting Glucose (SI)",
        "LBDLDLSI": "LDL Cholesterol (SI)",
        "LBDLDL": "LDL Cholesterol",
        "LBXTC": "Total Cholesterol",
        "LBDHDD": "HDL Cholesterol",
        "LBXSTR": "Triglycerides",
        "LBXSUA": "Uric Acid",
        "LBXSATSI": "ALT",
        "LUXCAPM": "Lung Capacity",
        "SMQ020": "Smoking Status",
        "SMQ040": "Smoking Frequency",
        "ALQ121": "Alcohol Consumption",
        "PAD680": "Physical Activity",
        "INDFMPIR": "Income to Poverty Ratio",
        "DIQ010": "Diabetes History",
        "BPQ020": "Hypertension History",
        "MCQ160B": "Heart Disease History",
        "MCQ220": "Kidney Disease History"
    }
    return feature_name_map.get(feature_code, feature_code)


def _format_feature_value(feature_code, value):
    """Format feature value for display."""
    if value is None:
        return ""
    
    # Gender
    if feature_code == "RIAGENDR":
        return "Male" if value == 1 else "Female"
    
    # Boolean-like values (1=Yes, 2=No)
    if feature_code in ["SMQ020", "DIQ010", "BPQ020", "MCQ160B", "MCQ220"]:
        return "Yes" if value == 1 else "No"
    
    # Return value as string
    if isinstance(value, float):
        return f"{value:.1f}"
    return str(value)


def _draw_forms():
    create_basic_info_section()
    create_lifestyle_factors_section()        
    create_medical_history_section()
    create_lab_values_section()