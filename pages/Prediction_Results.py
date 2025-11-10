import streamlit as st
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import display_results

st.set_page_config(page_title="Prediction Results", layout="wide")

st.title("Prediction Results")


def _show_no_results_message(message):
    """Display warning message and button to return to main page."""
    st.warning(message)
    if st.button("Go to Main Page"):
        st.switch_page("streamlit_app.py")
    st.stop()


def _validate_results_available():
    """Validate that prediction results are available in session state."""
    if 'prediction_done' not in st.session_state or not st.session_state.prediction_done:
        _show_no_results_message(
            "No prediction results available. Please go back to the main page and run a prediction."
        )
    
    if 'risk_scores' not in st.session_state or st.session_state.risk_scores is None:
        _show_no_results_message(
            "No risk scores available. Please go back to the main page and run a prediction."
        )


def _load_sample_data():
    """Load sample prediction data for demonstration."""
    st.session_state.prediction_done = True
    st.session_state.risk_scores = {
        "Diabetes": {"score": 23, "status": "MODERATE RISK"},
        "Hypertension": {"score": 67, "status": "HIGH RISK"},
        "CVD": {"score": 15, "status": "LOW RISK"},
        "Kidney Disease": {"score": 12, "status": "LOW RISK"}
    }
    st.session_state.risk_factors = [
        {"factor": "Age (62 years)", "modifiable": False},
        {"factor": "BMI 31.2 (Obese)", "modifiable": True},
        {"factor": "Low physical activity", "modifiable": True},
        {"factor": "Family history", "modifiable": False}
    ]
    st.session_state.recommendations = [
        "Lose 10-15 pounds (reduce BMI to <30)",
        "Exercise 30 minutes daily, 5 days/week",
        "Reduce sodium intake to <2,300mg/day",
        "Consider consulting your doctor about blood pressure"
    ]
    st.session_state.comparison_data = {
        "age_group": "60-65",
        "gender": "Similar",
        "population_avg": {
            "Diabetes": 18,
            "Hypertension": 45,
            "CVD": 12,
            "Kidney Disease": 8
        }
    }


# Temporarily load sample data to display the results page
# TODO: Remove this when real prediction data is available
if 'prediction_done' not in st.session_state or not st.session_state.prediction_done:
    _load_sample_data()

# Validate results before displaying
# Temporarily commented out to allow results page to display
# _validate_results_available()

# Display results
display_results()

