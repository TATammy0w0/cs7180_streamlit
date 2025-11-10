import streamlit as st
import streamlit_shadcn_ui as ui
import plotly.graph_objects as go
import html

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


def _generate_risk_card_html(disease, score, status):
    """Generate HTML for a risk score card."""
    style = _get_risk_style(status)
    status_short = status.replace(" RISK", "")
    
    return f"""
    <div style='padding: 24px 24px 20px 24px; margin-bottom: 20px; background: {style["bg_gradient"]}; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.15); border: 2px solid {style["color"]}; text-align: center; height: 240px; width: 100%; display: flex; flex-direction: column; justify-content: space-between; box-sizing: border-box;'>
        <div style='flex: 1; display: flex; flex-direction: column; justify-content: center;'>
            <div style='font-size: 14px; font-weight: 600; color: #374151; margin-bottom: 16px; height: 20px; line-height: 20px; overflow: hidden;'>{disease}</div>
            <div style='font-size: 64px; font-weight: 800; color: {style["color"]}; margin: 20px 0; line-height: 64px; height: 64px; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; letter-spacing: -2px;'>{score}%</div>
            <div style='margin: 16px 0; height: 12px;'>
                <div style='width: 100%; height: 12px; background-color: rgba(0,0,0,0.1); border-radius: 6px; overflow: hidden;'>
                    <div style='width: {score}%; height: 100%; background-color: {style["color"]}; border-radius: 6px;'></div>
                </div>
            </div>
        </div>
        <div style='margin-top: auto; padding-top: 12px; display: flex; align-items: center; justify-content: center;'>
            <span style='display: inline-block; padding: 6px 12px; background-color: {style["color"]}; color: white; border-radius: 20px; font-size: 11px; font-weight: 600; white-space: nowrap; max-width: 100%; overflow: hidden; text-overflow: ellipsis;'>{status_short}</span>
        </div>
    </div>
    """


def _generate_factor_html(factor_data, index, recommendation):
    """Generate HTML for a risk factor card."""
    factor = factor_data["factor"]
    is_modifiable = factor_data["modifiable"]
    styles = MODIFIABLE_STYLES if is_modifiable else NON_MODIFIABLE_STYLES
    modifiable_text = "MODIFIABLE" if is_modifiable else "Non-modifiable"
    
    factor_header = f"""
    <div style='margin-bottom: 24px; border: 2px solid {styles["border_color"]}; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
        <div style='padding: 20px; background: {styles["bg_gradient"]}; border-bottom: 2px solid {styles["border_color"]};'>
            <div style='display: flex; align-items: center; justify-content: space-between;'>
                <div style='display: flex; align-items: center; gap: 16px;'>
                    <div style='width: 40px; height: 40px; border-radius: 50%; background: {styles["circle_bg"]}; color: white; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 18px;'>
                        {index}
                    </div>
                    <span style='font-size: 18px; font-weight: 600; color: #1f2937;'>{factor}</span>
                </div>
                <span style='padding: 6px 14px; background: {styles["badge_bg"]}; color: white; border-radius: 20px; font-size: 12px; font-weight: 600;'>
                    {modifiable_text}
                </span>
            </div>
        </div>
    """
    
    rec_html = ""
    if recommendation:
        rec_escaped = html.escape(recommendation)
        rec_html = f"""
        <div style='padding: 16px 20px 16px 76px; background: #f8fafc; border-left: 4px solid #3b82f6;'>
            <div style='display: flex; align-items: start; gap: 12px;'>
                <div style='width: 6px; height: 6px; border-radius: 50%; background: #3b82f6; margin-top: 8px; flex-shrink: 0;'></div>
                <div style='flex: 1;'>
                    <div style='font-size: 12px; color: #64748b; margin-bottom: 4px; font-weight: 600;'>RECOMMENDATION</div>
                    <div style='font-size: 15px; color: #1e293b; line-height: 1.6;'>{rec_escaped}</div>
                </div>
            </div>
        </div>
        """
    
    return factor_header + rec_html + "</div>"


def _generate_comparison_chart(diseases, user_scores, avg_scores):
    """Generate comparison chart between user and population averages."""
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Your Risk',
        x=diseases,
        y=user_scores,
        marker_color='#3b82f6',
        text=[f"{s}%" for s in user_scores],
        textposition='outside',
        textfont=dict(size=14, color='#1e40af', weight='bold'),
        hovertemplate='<b>%{x}</b><br>Your Risk: %{y}%<extra></extra>',
    ))
    
    fig.add_trace(go.Bar(
        name='Population Average',
        x=diseases,
        y=avg_scores,
        marker_color='#94a3b8',
        text=[f"{s}%" for s in avg_scores],
        textposition='outside',
        textfont=dict(size=14, color='#475569', weight='bold'),
        hovertemplate='<b>%{x}</b><br>Population Avg: %{y}%<extra></extra>',
    ))
    
    fig.update_layout(
        title=dict(text="Risk Comparison: You vs Population Average (Click a bar to see details)", 
                  font=dict(size=18, color='#1f2937')),
        xaxis=dict(title="Disease", titlefont=dict(size=14, color='#374151')),
        yaxis=dict(title="Risk Score (%)", titlefont=dict(size=14, color='#374151'), range=[0, 100]),
        barmode='group',
        height=450,
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        font=dict(size=12),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, 
                   font=dict(size=13)),
        margin=dict(l=20, r=20, t=60, b=40),
        hovermode='x unified',
    )
    
    return fig


def _generate_comparison_card_html(disease, user_score, avg_score):
    """Generate HTML for detailed comparison card."""
    diff = user_score - avg_score
    diff_abs = abs(diff)
    diff_color = "#dc2626" if diff > 0 else "#16a34a"
    diff_icon = "▲" if diff > 0 else "▼"
    
    return f"""
    <div style='padding: 24px; margin-bottom: 20px; background: linear-gradient(135deg, #ffffff 0%, #f9fafb 100%); border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); border: 2px solid #e5e7eb;'>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <div style='flex: 1;'>
                <h3 style='margin: 0 0 16px 0; color: #1f2937; font-size: 20px; font-weight: 700;'>{disease}</h3>
                <div style='display: flex; gap: 32px; margin-top: 16px;'>
                    <div style='padding: 16px; background: #eff6ff; border-radius: 12px; border: 2px solid #3b82f6; min-width: 120px;'>
                        <div style='font-size: 13px; color: #64748b; margin-bottom: 8px; font-weight: 600;'>Your Risk</div>
                        <div style='font-size: 32px; font-weight: bold; color: #3b82f6;'>{user_score}%</div>
                    </div>
                    <div style='padding: 16px; background: #f1f5f9; border-radius: 12px; border: 2px solid #94a3b8; min-width: 120px;'>
                        <div style='font-size: 13px; color: #64748b; margin-bottom: 8px; font-weight: 600;'>Population Avg</div>
                        <div style='font-size: 32px; font-weight: bold; color: #94a3b8;'>{avg_score}%</div>
                    </div>
                </div>
            </div>
            <div style='text-align: center; padding: 24px 28px; background: {diff_color}20; border-radius: 16px; border: 3px solid {diff_color}; margin-left: 24px; min-width: 140px;'>
                <div style='font-size: 13px; color: #64748b; margin-bottom: 8px; font-weight: 600;'>Difference</div>
                <div style='font-size: 36px; font-weight: bold; color: {diff_color};'>{diff_icon} {diff_abs}%</div>
            </div>
        </div>
    </div>
    """


def _handle_chart_selection(chart_event):
    """Handle chart click/selection to update selected disease."""
    if chart_event and 'selection' in chart_event:
        if 'points' in chart_event['selection'] and len(chart_event['selection']['points']) > 0:
            point = chart_event['selection']['points'][0]
            if 'x' in point:
                st.session_state.selected_disease = point['x']
            elif 'customdata' in point and len(point['customdata']) > 0:
                st.session_state.selected_disease = point['customdata'][0]


def _display_risk_scores(risk_scores):
    """Display risk scores for each disease."""
    st.markdown("### Risk Scores for Each Disease (0-100%)")
    st.markdown("")
    
    risk_cols = st.columns(4)
    risk_items = list(risk_scores.items())
    
    for idx, (disease, data) in enumerate(risk_items):
        score = data["score"]
        status = data["status"]
        risk_card_html = _generate_risk_card_html(disease, score, status)
        
        with risk_cols[idx]:
            st.markdown(risk_card_html, unsafe_allow_html=True)
    
    st.markdown("")


def _display_risk_factors(risk_factors, recommendations):
    """Display risk factors with recommendations."""
    st.markdown("### Top Risk Factors Identified")
    st.caption("Factors contributing to your health risk assessment with personalized recommendations")
    
    with ui.card(key="risk_factors_card"):
        recommendations_list = recommendations if recommendations else []
        
        for idx, factor_data in enumerate(risk_factors, 1):
            is_modifiable = factor_data["modifiable"]
            recommendation = None
            
            if is_modifiable:
                if recommendations_list:
                    recommendation = recommendations_list[0] if len(recommendations_list) > 0 else \
                        "Consult with your healthcare provider for personalized advice"
                else:
                    recommendation = "Consult with your healthcare provider for personalized advice"
            
            factor_html = _generate_factor_html(factor_data, idx, recommendation)
            st.markdown(factor_html, unsafe_allow_html=True)
    
    st.markdown("")


def _display_comparison(risk_scores, comparison_data):
    """Display comparison to similar individuals."""
    st.markdown("### Comparison to Similar Individuals")
    st.caption(f"Your risk compared to others in your age group ({comparison_data['age_group']}) and population statistics")
    
    pop_avg = comparison_data["population_avg"]
    diseases = list(risk_scores.keys())
    user_scores = [risk_scores[d]["score"] for d in diseases]
    avg_scores = [pop_avg.get(d, 0) for d in diseases]
    
    fig = _generate_comparison_chart(diseases, user_scores, avg_scores)
    chart_event = st.plotly_chart(fig, use_container_width=True, key="comparison_chart", on_select="rerun")
    
    _handle_chart_selection(chart_event)
    
    st.markdown("")
    st.caption("Click on a bar in the chart above to see detailed comparison below")
    st.markdown("")
    
    # Display detailed comparison if disease is selected
    if st.session_state.selected_disease and st.session_state.selected_disease in risk_scores:
        with ui.card(key="comparison_card"):
            st.markdown(f"**Detailed Comparison: {st.session_state.selected_disease}**")
            st.markdown("")
            
            disease = st.session_state.selected_disease
            user_score = risk_scores[disease]["score"]
            avg_score = pop_avg.get(disease, 0)
            
            comparison_html = _generate_comparison_card_html(disease, user_score, avg_score)
            st.markdown(comparison_html, unsafe_allow_html=True)


def display_results():
    """Display prediction results - shared function for both main page and results page."""
    
    if 'prediction_done' not in st.session_state or not st.session_state.prediction_done:
        return False
    
    if 'risk_scores' not in st.session_state or st.session_state.risk_scores is None:
        return False
    
    # Initialize selected_disease if not exists
    if 'selected_disease' not in st.session_state:
        st.session_state.selected_disease = None
    
    # Display all sections
    _display_risk_scores(st.session_state.risk_scores)
    _display_risk_factors(st.session_state.risk_factors, st.session_state.recommendations)
    _display_comparison(st.session_state.risk_scores, st.session_state.comparison_data)
    
    return True

