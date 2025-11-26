import streamlit as st
import plotly.graph_objects as go
import html
import json

# Constants for styling
RISK_COLORS = {
    "LOW": {"color": "#16a34a", "variant": "default", 
            "bg_gradient": "linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%)"},
    "MODERATE": {"color": "#ca8a04", "variant": "secondary",
                 "bg_gradient": "linear-gradient(135deg, #fefce8 0%, #fef3c7 100%)"},
    "HIGH": {"color": "#dc2626", "variant": "destructive",
             "bg_gradient": "linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%)"}
}

MODIFIABLE_STYLES = {
    "border_color": "#3b82f6",
    "bg_gradient": "linear-gradient(90deg, #eff6ff 0%, #dbeafe 100%)",
    "badge_bg": "#2563eb",
    "circle_bg": "#3b82f6"
}

NON_MODIFIABLE_STYLES = {
    "border_color": "#e5e7eb",
    "bg_gradient": "linear-gradient(90deg, #f9fafb 0%, #f3f4f6 100%)",
    "badge_bg": "#6b7280",
    "circle_bg": "#6b7280"
}


def _get_risk_style(status):
    """Get styling information based on risk status."""
    if "LOW" in status:
        return RISK_COLORS["LOW"]
    elif "MODERATE" in status:
        return RISK_COLORS["MODERATE"]
    else:
        return RISK_COLORS["HIGH"]


def _format_ordinal(n):
    """Format a number as an ordinal (1st, 2nd, 3rd, 4th, etc.)."""
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


def _format_percentage(value):
    """Format a number as a percentage with at most 2 decimal places, rounded."""
    if value is None:
        return "0%"
    rounded = round(value, 2)
    # If it's a whole number, don't show decimal places
    if rounded == int(rounded):
        return f"{int(rounded)}%"
    # Otherwise, show up to 2 decimal places, removing trailing zeros
    return f"{rounded:.2f}".rstrip('0').rstrip('.') + "%"


def _generate_factor_html(factor_data, index, recommendation):
    """Generate HTML for a risk factor card."""
    factor = factor_data["factor"]
    is_modifiable = factor_data["modifiable"]
    styles = MODIFIABLE_STYLES if is_modifiable else NON_MODIFIABLE_STYLES
    modifiable_text = "MODIFIABLE" if is_modifiable else "Non-modifiable"
    
    # Build the complete HTML structure
    rec_escaped = html.escape(recommendation) if recommendation else ""
    
    # Build HTML as a single string to avoid formatting issues
    html_parts = []
    html_parts.append(f"<div style='margin-bottom: 24px; border: 2px solid {styles['border_color']}; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>")
    html_parts.append(f"<div style='padding: 20px; background: {styles['bg_gradient']}; border-bottom: 2px solid {styles['border_color']};'>")
    html_parts.append("<div style='display: flex; align-items: center; justify-content: space-between;'>")
    html_parts.append("<div style='display: flex; align-items: center; gap: 16px;'>")
    html_parts.append(f"<div style='width: 40px; height: 40px; border-radius: 50%; background: {styles['circle_bg']}; color: white; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 18px;'>{index}</div>")
    html_parts.append(f"<span style='font-size: 18px; font-weight: 600; color: #1f2937;'>{html.escape(factor)}</span>")
    html_parts.append("</div>")
    html_parts.append(f"<span style='padding: 6px 14px; background: {styles['badge_bg']}; color: white; border-radius: 20px; font-size: 12px; font-weight: 600;'>{modifiable_text}</span>")
    html_parts.append("</div>")
    html_parts.append("</div>")
    
    if recommendation:
        # Different styles for modifiable vs non-modifiable recommendations
        if is_modifiable:
            # Modifiable: Use deeper blue to emphasize actionable recommendations
            rec_bg = "#eff6ff"
            rec_border = "#2563eb"
            rec_label_color = "#1e40af"
        else:
            # Non-modifiable: Use subtle gray for informational recommendations
            rec_bg = "#f9fafb"
            rec_border = "#9ca3af"
            rec_label_color = "#6b7280"
        
        html_parts.append(f"<div style='padding: 20px 24px 20px 76px; background: {rec_bg}; border-left: 4px solid {rec_border}; border-radius: 0 0 12px 12px;'>")
        html_parts.append("<div style='display: flex; align-items: start; gap: 16px;'>")
        html_parts.append(f"<div style='width: 6px; height: 6px; border-radius: 50%; background: {rec_border}; margin-top: 10px; flex-shrink: 0;'></div>")
        html_parts.append("<div style='flex: 1;'>")
        html_parts.append(f"<div style='font-size: 13px; color: {rec_label_color}; margin-bottom: 8px; font-weight: 700; letter-spacing: 0.3px; text-transform: uppercase;'>Recommendation</div>")
        html_parts.append(f"<div style='font-size: 16px; color: #1e293b; line-height: 1.8; font-weight: 400;'>{rec_escaped}</div>")
        html_parts.append("</div>")
        html_parts.append("</div>")
        html_parts.append("</div>")
    
    html_parts.append("</div>")
    
    return "".join(html_parts)


def _generate_comparison_card_html(disease, user_score, avg_score):
    """Generate HTML for detailed comparison card."""
    diff = user_score - avg_score
    diff_abs = abs(diff)
    if diff > 0:
        diff_color = "#dc2626"
        diff_bg = "rgba(220, 38, 38, 0.15)"
    else:
        diff_color = "#16a34a"
        diff_bg = "rgba(22, 163, 74, 0.15)"
    diff_icon = "▲" if diff > 0 else "▼"
    
    return f"""
    <div style='padding: 24px; margin-bottom: 20px; background: linear-gradient(135deg, #ffffff 0%, #f9fafb 100%); border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); border: 2px solid #e5e7eb;'>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <div style='flex: 1;'>
                <h3 style='margin: 0 0 16px 0; color: #1f2937; font-size: 20px; font-weight: 700;'>{disease}</h3>
                <div style='display: flex; gap: 32px; margin-top: 16px;'>
                    <div style='padding: 16px; background: #eff6ff; border-radius: 12px; border: 2px solid #3b82f6; min-width: 120px;'>
                        <div style='font-size: 13px; color: #64748b; margin-bottom: 8px; font-weight: 600;'>Your Risk</div>
                        <div style='font-size: 32px; font-weight: bold; color: #3b82f6;'>{_format_percentage(user_score)}</div>
                    </div>
                    <div style='padding: 16px; background: #f1f5f9; border-radius: 12px; border: 2px solid #94a3b8; min-width: 120px;'>
                        <div style='font-size: 13px; color: #64748b; margin-bottom: 8px; font-weight: 600;'>Population Avg</div>
                        <div style='font-size: 32px; font-weight: bold; color: #94a3b8;'>{_format_percentage(avg_score)}</div>
                    </div>
                </div>
            </div>
            <div style='text-align: center; padding: 24px 28px; background: {diff_bg}; border-radius: 16px; border: 3px solid {diff_color}; margin-left: 24px; min-width: 140px;'>
                <div style='font-size: 13px; color: #64748b; margin-bottom: 8px; font-weight: 600;'>Difference</div>
                <div style='font-size: 36px; font-weight: bold; color: {diff_color};'>{diff_icon} {_format_percentage(diff_abs)}</div>
            </div>
        </div>
    </div>
    """


def _display_risk_scores(risk_scores, risk_factors_by_disease):
    """Display risk scores for each disease using Plotly interactive cards."""
    st.markdown("### Risk Scores for Each Disease")
    st.caption("Click on a disease card below to view detailed risk factors and recommendations")
    st.markdown("")
    
    # Display all diseases, regardless of whether they have risk factors
    risk_items = [
        (disease, data) for disease, data in risk_scores.items()
    ]
    
    if not risk_items:
        st.info("No prediction results available.")
        st.markdown("")
        return
    
    selected_disease = st.session_state.get("selected_disease")
    
    # Dynamically create columns based on number of diseases (max 5 per row)
    num_diseases = len(risk_items)
    cols_per_row = min(num_diseases, 5)
    
    # Display diseases in rows using Plotly cards
    for row_start in range(0, num_diseases, cols_per_row):
        row_end = min(row_start + cols_per_row, num_diseases)
        row_items = risk_items[row_start:row_end]
        risk_cols = st.columns(len(row_items))
        
        for col_idx, (disease, data) in enumerate(row_items):
            score = data["score"]
            status = data["status"]
            is_selected = (disease == selected_disease)
            style = _get_risk_style(status)
            status_short = status.replace(" RISK", "")
            idx = row_start + col_idx
            bg_color = style["color"]
            
            with risk_cols[col_idx]:
                # Determine card styling
                card_border_color = "#1e40af" if is_selected else bg_color
                card_border_width = "4px" if is_selected else "2px"
                card_shadow = "0 10px 30px rgba(30, 64, 175, 0.3)" if is_selected else "0 6px 20px rgba(0,0,0,0.2)"
                
                # Create beautiful HTML card
                card_html = f"""
                <div style='padding: 24px; margin-bottom: 12px; background: {style["bg_gradient"]}; 
                             border-radius: 16px; box-shadow: {card_shadow}; 
                             border: {card_border_width} solid {card_border_color}; 
                             text-align: center; height: 300px; width: 100%; 
                             display: flex; flex-direction: column; justify-content: space-between; 
                             box-sizing: border-box; transition: all 0.3s ease;'>
                    <div style='flex: 1; display: grid; grid-template-rows: 32px 140px auto; row-gap: 12px;'>
                        <div style='font-size: 18px; font-weight: 700; color: #1f2937; margin: 0; height: 40px; 
                                    display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; line-height: 1.2;'>{disease}</div>
                        <div style='display: flex; align-items: center; justify-content: center; height: 100%; 
                                    font-size: 72px; font-weight: 900; color: {bg_color}; margin: 0; 
                                    line-height: 72px; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; 
                                    letter-spacing: -3px;'>{_format_percentage(score)}</div>
                        <div style='margin: 0; height: 8px; width: 100%; background-color: rgba(0,0,0,0.1); 
                                     border-radius: 4px; overflow: hidden;'>
                            <div style='width: {score}%; height: 100%; background: {bg_color}; border-radius: 4px; transition: width 0.3s ease;'></div>
                        </div>
                    </div>
                    <div style='margin-top: auto; padding-top: 12px;'>
                        <span style='display: inline-block; padding: 8px 16px; background-color: {bg_color}; 
                                     color: white; border-radius: 20px; font-size: 12px; font-weight: 700;'>{status_short}</span>
                    </div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
                
                # Add click button below the card
                if st.button(
                    "View Details" if not is_selected else "✓ Selected",
                    key=f"disease_btn_{idx}",
                    use_container_width=True,
                    type="primary" if is_selected else "secondary"
                ):
                    st.session_state.selected_disease = disease
                    st.rerun()
        
        st.markdown("")
    
    st.markdown("")


def _display_selected_disease_factors(selected_disease, risk_factors_by_disease, factor_recommendations_map):
    """Display risk factors and recommendations for the selected disease (all factors)."""
    if not selected_disease:
        return
    
    if selected_disease not in risk_factors_by_disease:
        return
    
    factors = risk_factors_by_disease[selected_disease]  # Display all factors
    
    if not factors:
        return
    
    # Separate factors into increasing risk and decreasing risk
    increasing_risk_factors = [
        f for f in factors if f.get("is_increasing_risk", True)
    ]
    decreasing_risk_factors = [
        f for f in factors if not f.get("is_increasing_risk", True)
    ]
    
    st.markdown("---")
    st.markdown(f"### Risk Factors for {selected_disease}")
    st.markdown("")
    
    # Display increasing risk factors (with recommendations - these need improvement)
    if increasing_risk_factors:
        st.markdown("#### Factors Increasing Risk")
        st.caption(f"{len(increasing_risk_factors)} factor(s) that increase your risk")
        st.markdown("")
        
        for idx, factor_data in enumerate(increasing_risk_factors, 1):
            factor_type = factor_data.get("factor_type", "")
            
            # Get recommendation for increasing risk factors (these need improvement)
            recommendation = None
            # First try to get from factor_data (from API)
            if factor_data.get("recommendation"):
                recommendation = factor_data.get("recommendation")
            # Then try factor_recommendations_map
            elif factor_type in factor_recommendations_map:
                recommendation = factor_recommendations_map[factor_type]
            # Default message if no recommendation found
            elif factor_type:
                recommendation = "Consult with your healthcare provider for personalized recommendations based on your specific health profile."
            
            # Display factor with recommendation (index starts from 1 for increasing risk)
            factor_html = _generate_factor_html(factor_data, idx, recommendation)
            st.markdown(factor_html, unsafe_allow_html=True)
        
        st.markdown("")
    
    # Display decreasing risk factors (no recommendations - these are protective factors)
    if decreasing_risk_factors:
        st.markdown("#### Factors Decreasing Risk")
        st.caption(f"{len(decreasing_risk_factors)} factor(s) that decrease your risk")
        st.markdown("")
        
        for idx, factor_data in enumerate(decreasing_risk_factors, 1):
            # No recommendation for decreasing risk factors (these are already good)
            # Index starts from 1 for decreasing risk (separate numbering)
            factor_html = _generate_factor_html(factor_data, idx, None)
            st.markdown(factor_html, unsafe_allow_html=True)
        
        st.markdown("")
    
    st.markdown("")


def _display_comparison(selected_disease, risk_scores, comparison_data_by_disease):
    """Display comparison to similar individuals for the selected disease."""
    if not selected_disease:
        return
    
    if selected_disease not in comparison_data_by_disease:
        st.warning(f"No comparison data available for **{selected_disease}**.")
        st.markdown("")
        return
    
    comp_data = comparison_data_by_disease[selected_disease]
    
    st.markdown("---")
    st.markdown(f"### Population Comparison: {selected_disease}")
    st.caption(f"Your risk compared to others in your age group (**{comp_data.get('age_range', 'N/A')}**) and population statistics")
    st.markdown("")
    
    user_score = risk_scores[selected_disease]["score"]
    pop_mean = comp_data.get("population_mean", 0)
    pop_std_dev = comp_data.get("population_std_dev", 0)
    percentile = comp_data.get("percentile", 0)
    sample_size = comp_data.get("sample_size", 0)
    
    # Display comparison chart (bar chart) - only for selected disease
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Your Risk',
        x=[selected_disease],
        y=[user_score],
        marker_color='#3b82f6',
        text=[_format_percentage(user_score)],
        textposition='outside',
        textfont=dict(size=16, color='#1e40af', weight='bold'),
        hovertemplate='<b>%{x}</b><br>Your Risk: %{y}%<extra></extra>',
        width=0.3,
    ))
    
    fig.add_trace(go.Bar(
        name='Population Average',
        x=[selected_disease],
        y=[pop_mean],
        marker_color='#94a3b8',
        text=[_format_percentage(pop_mean)],
        textposition='outside',
        textfont=dict(size=16, color='#475569', weight='bold'),
        hovertemplate='<b>%{x}</b><br>Population Avg: %{y}%<extra></extra>',
        width=0.3,
    ))
    
    fig.update_layout(
        title=dict(text=f"Risk Comparison: {selected_disease}", 
                  font=dict(size=18, color='#1f2937')),
        xaxis=dict(title="", showticklabels=False),
        yaxis=dict(title=dict(text="Risk Score (%)", font=dict(size=14, color='#374151')), range=[0, max(user_score, pop_mean) * 1.2]),
        barmode='group',
        height=400,
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font=dict(size=12),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, 
                   font=dict(size=13)),
        margin=dict(l=20, r=20, t=60, b=40),
        hovermode='x unified',
    )
    
    st.plotly_chart(fig, use_container_width=True, key="comparison_chart")
    
    st.markdown("")
    
    # Display comparison card
    st.markdown(f"**Detailed Comparison: {selected_disease}**")
    st.markdown("")
    
    comparison_html = _generate_comparison_card_html(selected_disease, user_score, pop_mean)
    st.markdown(comparison_html, unsafe_allow_html=True)
    
    # Additional statistics with unified background
    st.markdown("")
    stats_html = f"""
    <div style='padding: 24px; margin-top: 20px; background: linear-gradient(135deg, #ffffff 0%, #f9fafb 100%); border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); border: 2px solid #e5e7eb;'>
        <h3 style='margin: 0 0 20px 0; color: #1f2937; font-size: 18px; font-weight: 700;'>Additional Statistics</h3>
        <div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px;'>
            <div style='padding: 16px; background: #eff6ff; border-radius: 12px; border: 2px solid #3b82f6;'>
                <div style='font-size: 13px; color: #64748b; margin-bottom: 8px; font-weight: 600;'>Your Percentile</div>
                <div style='font-size: 28px; font-weight: bold; color: #3b82f6;'>{_format_percentage(percentile)}</div>
                <div style='font-size: 11px; color: #94a3b8; margin-top: 4px;'>Higher than {_format_percentage(percentile)} of similar individuals</div>
            </div>
            <div style='padding: 16px; background: #f1f5f9; border-radius: 12px; border: 2px solid #94a3b8;'>
                <div style='font-size: 13px; color: #64748b; margin-bottom: 8px; font-weight: 600;'>Population Mean</div>
                <div style='font-size: 28px; font-weight: bold; color: #94a3b8;'>{_format_percentage(pop_mean)}</div>
                <div style='font-size: 11px; color: #94a3b8; margin-top: 4px;'>Average risk score</div>
            </div>
            <div style='padding: 16px; background: #f9fafb; border-radius: 12px; border: 2px solid #d1d5db;'>
                <div style='font-size: 13px; color: #64748b; margin-bottom: 8px; font-weight: 600;'>Sample Size</div>
                <div style='font-size: 28px; font-weight: bold; color: #6b7280;'>{sample_size:,}</div>
                <div style='font-size: 11px; color: #94a3b8; margin-top: 4px;'>Similar individuals in comparison</div>
            </div>
        </div>
    </div>
    """
    st.markdown(stats_html, unsafe_allow_html=True)


def convert_api_response_to_display_format(api_response, recommendations_config=None):
    """
    Convert API response (snake_case format) to display format for frontend.
    
    Args:
        api_response: Dictionary containing the API response with snake_case fields
                     Expected format:
                     {
                         "user_id": str,
                         "assessment_date": str,
                         "diseases": [
                             {
                                 "disease_type": str,
                                 "disease_name": str,
                                 "risk_score": int,
                                 "confidence_score": float,
                                 "status": str,
                                 "top_risk_factors": [...],
                                 "population_comparison": {...}
                             }
                         ]
                     }
        recommendations_config: Optional dictionary with recommendations config.
                                If None, will try to load from recommendations_config.json
    
    Returns:
        Dictionary with keys: risk_scores, risk_factors, comparison_data, recommendations
    """
    risk_scores = {}
    all_risk_factors = []
    comparison_data = {
        "age_group": "",
        "gender": "",
        "population_avg": {}
    }
    recommendations = []
    
    # Load recommendations config if not provided
    if recommendations_config is None:
        try:
            with open("recommendations_config.json", 'r') as f:
                recommendations_config = json.load(f)
        except FileNotFoundError:
            recommendations_config = {}
    
    # Disease name mapping for recommendations config
    disease_name_mapping = {
        "hypertension": "Hypertension",
        "diabetes": "Diabetes",
        "cvd": "CVD",
        "Cardiovascular Disease": "CVD",
        "Type 2 Diabetes": "Diabetes"
    }
    
    # Dictionary to store risk factors by disease (top 5 per disease)
    risk_factors_by_disease = {}
    # Dictionary to store comparison data by disease
    comparison_data_by_disease = {}
    
    # Process each disease
    for disease in api_response.get("diseases", []):
        disease_name = disease.get("disease_name", "")
        disease_type = disease.get("disease_type", "")
        risk_score = disease.get("risk_score", 0)
        status = disease.get("status", "LOW RISK")
        
        # Add to risk_scores
        risk_scores[disease_name] = {
            "score": risk_score,
            "status": status
        }
        
        # Collect all risk factors for this disease
        disease_factors = []
        top_factors = disease.get("top_risk_factors", [])  # Get all factors
        
        for factor in top_factors:
            factor_name = factor.get("factor_name", "")
            factor_value = factor.get("factor_value", "")
            is_modifiable = factor.get("is_modifiable", False)
            factor_type = factor.get("factor_type", "")
            is_increasing_risk = factor.get("is_increasing_risk", True)  # Default to True for backward compatibility
            recommendation = factor.get("recommendation", "")
            
            # Format factor display string with separator
            factor_display = f"{factor_name}"
            if factor_value:
                factor_display += f": {factor_value}"
            
            # Store factor for this disease
            disease_factors.append({
                "factor": factor_display,
                "modifiable": is_modifiable,
                "factor_type": factor_type,
                "is_increasing_risk": is_increasing_risk,
                "recommendation": recommendation
            })
        
        # Store factors for this disease
        risk_factors_by_disease[disease_name] = disease_factors
        
        # Process population comparison for this disease
        pop_comp = disease.get("population_comparison", {})
        if pop_comp:
            # Store comparison data for this specific disease
            comparison_data_by_disease[disease_name] = {
                "age_range": pop_comp.get("age_range", ""),
                "gender": pop_comp.get("gender", ""),
                "user_risk": pop_comp.get("user_risk", risk_score),
                "population_mean": pop_comp.get("population_mean", 0),
                "population_std_dev": pop_comp.get("population_std_dev", 0),
                "percentile": pop_comp.get("percentile", 0),
                "sample_size": pop_comp.get("sample_size", 0)
            }
            
            # Also update general comparison_data for backward compatibility
            if not comparison_data["age_group"]:
                comparison_data["age_group"] = pop_comp.get("age_range", "")
                comparison_data["gender"] = pop_comp.get("gender", "")
            
            comparison_data["population_avg"][disease_name] = pop_comp.get("population_mean", 0)
        
    # Build factor recommendations map from API response
    factor_recommendations_map = {}
    
    # First, try to extract recommendations from API response
    for disease in api_response.get("diseases", []):
        top_factors = disease.get("top_risk_factors", [])
        for factor in top_factors:
            factor_type = factor.get("factor_type", "")
            # Check if recommendation is in the factor data (from API)
            if "recommendation" in factor:
                factor_recommendations_map[factor_type] = factor["recommendation"]
    
    # Also load from file as fallback
    try:
        with open("factor_recommendations.json", 'r') as f:
            file_recommendations = json.load(f)
            # Merge with API recommendations (API takes precedence)
            for key, value in file_recommendations.items():
                if key not in factor_recommendations_map:
                    factor_recommendations_map[key] = value
    except FileNotFoundError:
        pass  # Use empty dict if file not found
    
    return {
        "risk_scores": risk_scores,
        "risk_factors_by_disease": risk_factors_by_disease,
        "comparison_data": comparison_data,
        "comparison_data_by_disease": comparison_data_by_disease,
        "factor_recommendations_map": factor_recommendations_map
    }


def display_results():
    """Display prediction results - shared function for both main page and results page."""
    
    if 'prediction_done' not in st.session_state or not st.session_state.prediction_done:
        return False
    
    if 'risk_scores' not in st.session_state or st.session_state.risk_scores is None:
        return False
    
    if 'risk_factors_by_disease' not in st.session_state:
        return False
    
    if 'factor_recommendations_map' not in st.session_state:
        return False
    
    # Initialize selected_disease if not exists
    if 'selected_disease' not in st.session_state:
        st.session_state.selected_disease = None
    
    # Display all diseases, regardless of whether they have risk factors
    # Risk factors section will be hidden automatically if empty (handled in _display_selected_disease_factors)
    _display_risk_scores(st.session_state.risk_scores, st.session_state.risk_factors_by_disease)
    
    # Display selected disease details (risk factors and comparison)
    selected_disease = st.session_state.get("selected_disease")
    
    if selected_disease:
        # Display risk factors (will be hidden if empty, handled in _display_selected_disease_factors)
        if selected_disease in st.session_state.risk_factors_by_disease:
            _display_selected_disease_factors(
                selected_disease,
                st.session_state.risk_factors_by_disease,
                st.session_state.factor_recommendations_map
            )
        
        # Display comparison for selected disease (always show if available)
        if selected_disease in st.session_state.risk_scores:
            _display_comparison(
                selected_disease,
                st.session_state.risk_scores,
                st.session_state.comparison_data_by_disease
            )
    
    return True

