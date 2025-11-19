import streamlit as st
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import display_results

st.set_page_config(page_title="Prediction Results", layout="wide")

st.title("Prediction Results")


def _show_no_results_message():
    """Display message when no prediction results are available."""
    st.info("No prediction results available yet.")
    st.markdown("---")
    st.markdown("### Please complete a prediction first")
    st.write("To view prediction results:")
    st.write("1. Go to the main page")
    st.write("2. Fill in the health information form")
    st.write("3. Click the 'Submit' button to run the prediction")
    st.write("4. You will be automatically redirected to this page with your results")
    st.markdown("---")
    
    if st.button("Go to Main Page", type="primary", use_container_width=True):
        st.switch_page("streamlit_app.py")
    
    st.stop()


def _validate_results_available():
    """Validate that prediction results are available in session state."""
    # Check if prediction was done
    if 'prediction_done' not in st.session_state or not st.session_state.prediction_done:
        return False
    
    # Check if risk scores are available
    if 'risk_scores' not in st.session_state or st.session_state.risk_scores is None:
        return False
    
    # Check if risk scores is not empty
    if not st.session_state.risk_scores:
        return False
    
    return True


# Validate results before displaying
if not _validate_results_available():
    _show_no_results_message()

# Display results
display_results()

