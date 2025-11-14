import streamlit as st
import requests
from constants import REQUIRED_FEATURE_SET, OPTIONAL_FEATURE_SET
from feature_map import FeatureMap
from form_components import create_basic_info_section, create_lab_values_section, create_lifestyle_factors_section, create_medical_history_section
from data_validation import format_post_data, validate_form_input, collect_form_values

API_BASE_URL = "https://disease-warning.onrender.com"

required_features_map = FeatureMap(REQUIRED_FEATURE_SET)
optional_features_map = FeatureMap(OPTIONAL_FEATURE_SET)

def three_diseases_input_form():
    with st.form("risk_form"):
        create_basic_info_section()
        create_lifestyle_factors_section()
        create_medical_history_section()
        create_lab_values_section()
        
        submitted = st.form_submit_button(
            "Submit", 
            type="primary",
            use_container_width=True
        )

        if submitted:
            missing_fields = validate_form_input(st)
            
            if missing_fields:
                st.error(f"Please fill in all required fields: {', '.join(missing_fields)}")
            
            collect_form_values(st, required_features_map, optional_features_map)
            data = format_post_data(required_features_map, optional_features_map)
            st.write(data)

            metrics_endpoint = f"{API_BASE_URL}/predict_all/"

            try:
                st.write(f"正在向 `{metrics_endpoint}` 发送 GET 请求...")
                response = requests.get(metrics_endpoint)
                st.write(f"**收到的状态码: {response.status_code}**")
                
                if response.status_code == 200:
                    st.success("获取 Metrics 成功！🎉")
                    st.subheader("收到的结果:")
                    st.json(response.json())
                else:
                    st.error("API 请求失败")
                    st.subheader("收到的错误详情:")
                    try:
                        st.json(response.json())
                    except requests.exceptions.JSONDecodeError:
                        st.text(response.text)

            except requests.exceptions.ConnectionError as e:
                st.error(f"连接失败: {e}")            

            if missing_fields:
                st.error(f"Please fill in all required fields: {', '.join(missing_fields)}")