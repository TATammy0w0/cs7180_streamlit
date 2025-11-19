import streamlit as st
import requests
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from input.input_form import _convert_api_to_frontend_format
from utils.display import convert_api_response_to_display_format, display_results

st.set_page_config(page_title="API Test", layout="wide")

# Update last visited page to track page navigation
if 'last_visited_page' not in st.session_state:
    st.session_state.last_visited_page = 'test_api'
else:
    st.session_state.last_visited_page = 'test_api'

st.title("🧪 API Test Page")
st.markdown("This page tests the backend API with fixed test data.")

# Fixed test data - Complete dataset to show all 4 diseases (CKD, Diabetes, Hypertension, CVD)
TEST_DATA = {
    "input_data": {
        # Required fields
        "RIDAGEYR": 60,  # Age
        "RIAGENDR": 1,  # 1=Male, 2=Female
        "BMXHT": 175.0,  # Height (cm)
        "BMXWT": 90.0,  # Weight (kg)
        "BMXWAIST": 100.0,  # Waist circumference (cm)
        "ALQ121": 50,  # Alcohol consumption (days/year)
        
        # Health metrics
        "BMXBMI": 29.4,  # BMI (overweight)
        "BPXSY1": 145.0,  # Systolic BP 1
        "BPXDI1": 92.0,  # Diastolic BP 1
        "BPXSY2": 143.0,  # Systolic BP 2 (for hypertension full)
        "BPXDI2": 90.0,  # Diastolic BP 2
        "BPXSY3": 144.0,  # Systolic BP 3 (for hypertension full)
        "BPXDI3": 91.0,  # Diastolic BP 3
        "BPXSY4": 142.0,  # Systolic BP 4
        "BPXDI4": 89.0,  # Diastolic BP 4
        "BPXOSY1": 145.0,  # Systolic BP (for diabetes full, CVD full)
        
        # Lab values - for diabetes full, hypertension full, CVD full
        "LBXGH": 6.8,  # HbA1c (pre-diabetic)
        "LBXGLU": 120.0,  # Fasting glucose (pre-diabetic)
        "LBDGLUSI": 6.7,  # Fasting glucose SI (for hypertension full)
        "LBXTC": 250.0,  # Total cholesterol (for diabetes full, CVD full)
        "LBDHDD": 42.0,  # HDL cholesterol (for diabetes full)
        "LBDLDLSI": 170.0,  # LDL cholesterol SI (for diabetes full)
        "LBDLDL": 180.0,  # LDL cholesterol (for CVD full)
        "LBXSTR": 220.0,  # Triglycerides (for diabetes full)
        "LBXSUA": 7.5,  # Uric acid
        "LBXSATSI": 50.0,  # ALT
        "LUXCAPM": 3200,  # Lung capacity (for diabetes full)
        
        # Lifestyle - required for all diseases
        "SMQ020": 1,  # Ever smoked (1=Yes, 2=No)
        "SMQ040": 1,  # Current smoker (1=Yes, 2=No)
        "PAD680": 150,  # Physical activity (min/week)
        
        # Medical history - for hypertension and CVD
        "MCQ160A": 2,  # Arthritis (2=No)
        "MCQ160P": 2,  # COPD (2=No) - for CVD
        "MCQ160D": 2,  # Angina (2=No) - for CVD
        "MCQ500": 2,  # Cancer (2=No) - for hypertension
        "OSQ230": 2,  # Metal objects (2=No) - for CVD
        
        # Other
        "INDFMPIR": 2.0,  # Income to poverty ratio
        "RIDRETH3": 3  # Race/ethnicity
        
        # Note: DIQ010 and BPQ020 are NOT included
        # If included, they would skip diabetes and hypertension prediction
    }
}

# API URL
API_BASE_URL = os.getenv("API_BASE_URL", "https://disease-warning-1.onrender.com")
PREDICT_ALL_URL = f"{API_BASE_URL}/prediction/all"

st.markdown("---")
st.subheader("Test Configuration")
st.write(f"**API URL:** `{PREDICT_ALL_URL}`")
st.write(f"**Test Data:** {len(TEST_DATA['input_data'])} fields")

# Display test data in a readable format
st.markdown("---")
st.subheader("📋 Test Patient Data")
st.markdown("**Complete dataset to test all 4 diseases (CKD, Diabetes, Hypertension, CVD)**")

# Organize data by category
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Demographics")
    st.write(f"- **Age:** {TEST_DATA['input_data']['RIDAGEYR']} years")
    st.write(f"- **Gender:** {'Male' if TEST_DATA['input_data']['RIAGENDR'] == 1 else 'Female'}")
    st.write(f"- **Height:** {TEST_DATA['input_data']['BMXHT']} cm")
    st.write(f"- **Weight:** {TEST_DATA['input_data']['BMXWT']} kg")
    st.write(f"- **BMI:** {TEST_DATA['input_data']['BMXBMI']:.1f} (Overweight)")
    st.write(f"- **Waist:** {TEST_DATA['input_data']['BMXWAIST']} cm")
    
    st.markdown("#### Blood Pressure")
    st.write(f"- **Systolic BP:** {TEST_DATA['input_data']['BPXSY1']}/{TEST_DATA['input_data']['BPXDI1']} mmHg")
    st.write(f"- **BP Readings 2-3:** Available for Hypertension Full model")
    st.write("  ⚠️ Stage 1 Hypertension")
    
    st.markdown("#### Blood Glucose")
    st.write(f"- **HbA1c:** {TEST_DATA['input_data']['LBXGH']}%")
    st.write(f"- **Fasting Glucose:** {TEST_DATA['input_data']['LBXGLU']} mg/dL")
    st.write("  ⚠️ Pre-diabetic range")

with col2:
    st.markdown("#### Cholesterol")
    st.write(f"- **Total:** {TEST_DATA['input_data']['LBXTC']} mg/dL")
    st.write(f"- **LDL:** {TEST_DATA['input_data']['LBDLDL']} mg/dL")
    st.write(f"- **HDL:** {TEST_DATA['input_data']['LBDHDD']} mg/dL")
    st.write(f"- **Triglycerides:** {TEST_DATA['input_data']['LBXSTR']} mg/dL")
    st.write("  ⚠️ High cholesterol")
    
    st.markdown("#### Lifestyle")
    st.write(f"- **Smoking:** {'Current smoker' if TEST_DATA['input_data']['SMQ040'] == 1 else 'Non-smoker'}")
    st.write(f"- **Alcohol:** {TEST_DATA['input_data']['ALQ121']} days/year")
    st.write(f"- **Physical Activity:** {TEST_DATA['input_data']['PAD680']} min/week")
    
    st.markdown("#### Medical History")
    st.write(f"- **Arthritis:** {'Yes' if TEST_DATA['input_data']['MCQ160A'] == 1 else 'No'}")
    st.write(f"- **COPD:** {'Yes' if TEST_DATA['input_data']['MCQ160P'] == 1 else 'No'}")
    st.write(f"- **Angina:** {'Yes' if TEST_DATA['input_data']['MCQ160D'] == 1 else 'No'}")
    st.write(f"- **Cancer:** {'Yes' if TEST_DATA['input_data']['MCQ500'] == 1 else 'No'}")
    st.write(f"- **Diabetes History:** Not provided (allows diabetes prediction)")
    st.write(f"- **Hypertension History:** Not provided (allows hypertension prediction)")

# Show full data in expander
with st.expander("🔍 View Complete Raw Data", expanded=False):
    st.json(TEST_DATA)

if st.button("🚀 Send POST Request & View Results", type="primary", use_container_width=True):
    with st.spinner("Sending POST request to backend..."):
        try:
            # Send POST request
            response = requests.post(PREDICT_ALL_URL, json=TEST_DATA, timeout=30)
            
            if response.status_code == 200:
                st.success("✅ API request successful!")
                
                # Get API response
                api_response = response.json()
                
                # Show raw API response (collapsible)
                with st.expander("📋 View Raw API Response", expanded=False):
                    st.json(api_response)
                
                # Convert API response to frontend format
                with st.spinner("Converting API response..."):
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
                    # Mark that results were generated on Test_API page, not main page
                    st.session_state.results_page = 'test_api'
                    st.session_state.show_results_on_main_page = False
                
                # Show conversion summary
                st.info(f"""
                **Conversion Summary:**
                - Diseases found: {len(display_data['risk_scores'])}
                - Diseases with risk factors: {sum(1 for d, factors in display_data['risk_factors_by_disease'].items() if len(factors) > 0)}
                - Total risk factors: {sum(len(factors) for factors in display_data['risk_factors_by_disease'].values())}
                """)
                
                # Show risk scores
                st.subheader("📊 Risk Scores")
                for disease, data in display_data["risk_scores"].items():
                    factors_count = len(display_data["risk_factors_by_disease"].get(disease, []))
                    st.write(f"- **{disease}**: {data['score']}% ({data['status']}) - {factors_count} risk factors")
                
                # Show success message
                st.success("✅ Data processed!")
                st.rerun()
                
            else:
                st.error(f"❌ API request failed with status code: {response.status_code}")
                try:
                    error_data = response.json()
                    st.json(error_data)
                except requests.exceptions.JSONDecodeError:
                    st.text(response.text)
                    
        except requests.exceptions.ConnectionError as e:
            st.error(f"❌ Connection failed: {e}")
            st.info("💡 Make sure the backend service is running at the configured URL.")
            st.code(f"# To start backend:\nbash start_backend.sh", language="bash")
            
        except requests.exceptions.Timeout:
            st.error("❌ Request timed out. Please try again.")
            
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
            import traceback
            with st.expander("🔍 View Error Details"):
                st.code(traceback.format_exc())

# Display results if prediction is done
if st.session_state.get('prediction_done', False):
    st.markdown("---")
    display_results()

st.markdown("---")
st.markdown("### 📝 Notes")
st.info("""
- This page uses fixed test data to test the backend API
- Click the button above to send a POST request and view results
- Results will be displayed below after successful prediction
- Make sure the backend service is running before testing
""")

