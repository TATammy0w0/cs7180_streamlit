import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(page_title="Dataset Statistics", layout="wide")

# Update last visited page to track page navigation
if 'last_visited_page' not in st.session_state:
    st.session_state.last_visited_page = 'dataset_statistics'
else:
    st.session_state.last_visited_page = 'dataset_statistics'

st.title("NHANES Dataset Statistics")
st.markdown("---")

# Dataset path (now in frontend folder)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = PROJECT_ROOT / "data" / "nhanes_2021_2023_master.csv"

@st.cache_data
def load_dataset():
    """Load the dataset with caching."""
    try:
        df = pd.read_csv(DATASET_PATH, low_memory=False)
        return df
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return None

# Load dataset
with st.spinner("Loading dataset..."):
    df = load_dataset()

if df is None:
    st.error("Failed to load dataset. Please check the file path.")
    st.stop()

# Overall Statistics
st.header("Overall Statistics")

col1, col2, col3, col4 = st.columns(4)

total_count = len(df)
col1.metric("Total Participants", f"{total_count:,}")

# Gender distribution
if 'RIAGENDR' in df.columns:
    gender_counts = df['RIAGENDR'].value_counts()
    male_count = gender_counts.get(1, 0)
    female_count = gender_counts.get(2, 0)
    male_pct = (male_count/total_count*100) if total_count > 0 else 0
    female_pct = (female_count/total_count*100) if total_count > 0 else 0
    col2.metric("Male", f"{male_count:,}", f"{male_pct:.1f}% of total")
    col3.metric("Female", f"{female_count:,}", f"{female_pct:.1f}% of total")
else:
    col2.metric("Male", "N/A")
    col3.metric("Female", "N/A")

# Age statistics
if 'RIDAGEYR' in df.columns:
    avg_age = df['RIDAGEYR'].mean()
    col4.metric("Average Age", f"{avg_age:.1f} years")
else:
    col4.metric("Average Age", "N/A")

st.markdown("---")

# Gender Distribution Chart
st.header("Gender Distribution")

if 'RIAGENDR' in df.columns:
    gender_data = df['RIAGENDR'].value_counts().sort_index()
    gender_labels = {1: "Male", 2: "Female"}
    gender_counts_dict = {gender_labels.get(k, k): v for k, v in gender_data.items()}
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Pie chart
        fig_pie = px.pie(
            values=list(gender_counts_dict.values()),
            names=list(gender_counts_dict.keys()),
            title="Gender Distribution (Pie Chart)",
            color_discrete_map={"Male": "#3b82f6", "Female": "#ec4899"}
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Bar chart
        fig_bar = px.bar(
            x=list(gender_counts_dict.keys()),
            y=list(gender_counts_dict.values()),
            title="Gender Distribution (Bar Chart)",
            labels={'x': 'Gender', 'y': 'Count'},
            color=list(gender_counts_dict.keys()),
            color_discrete_map={"Male": "#3b82f6", "Female": "#ec4899"}
        )
        fig_bar.update_layout(showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)
else:
    st.warning("Gender data (RIAGENDR) not available in dataset.")

st.markdown("---")

# Age Distribution
st.header("Age Distribution")

if 'RIDAGEYR' in df.columns:
    age_df = df[df['RIDAGEYR'].notna()].copy()
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Age histogram
        fig_hist = px.histogram(
            age_df,
            x='RIDAGEYR',
            nbins=50,
            title="Age Distribution (Histogram)",
            labels={'RIDAGEYR': 'Age (years)', 'count': 'Number of Participants'},
            color_discrete_sequence=['#3b82f6']
        )
        fig_hist.update_layout(bargap=0.1)
        st.plotly_chart(fig_hist, use_container_width=True)
    
    with col2:
        # Age groups
        age_df['Age Group'] = pd.cut(
            age_df['RIDAGEYR'],
            bins=[0, 20, 30, 40, 50, 60, 70, 80, 200],
            labels=['0-20', '20-30', '30-40', '40-50', '50-60', '60-70', '70-80', '80+']
        )
        age_group_counts = age_df['Age Group'].value_counts().sort_index()
        
        fig_age_group = px.bar(
            x=age_group_counts.index.astype(str),
            y=age_group_counts.values,
            title="Age Group Distribution",
            labels={'x': 'Age Group', 'y': 'Count'},
            color=age_group_counts.values,
            color_continuous_scale='Blues'
        )
        fig_age_group.update_layout(showlegend=False)
        st.plotly_chart(fig_age_group, use_container_width=True)
    
    # Age statistics table
    st.subheader("Age Statistics")
    age_stats = {
        'Statistic': ['Mean', 'Median', 'Min', 'Max', 'Std Dev'],
        'Value': [
            f"{age_df['RIDAGEYR'].mean():.1f} years",
            f"{age_df['RIDAGEYR'].median():.1f} years",
            f"{age_df['RIDAGEYR'].min():.0f} years",
            f"{age_df['RIDAGEYR'].max():.0f} years",
            f"{age_df['RIDAGEYR'].std():.1f} years"
        ]
    }
    st.dataframe(pd.DataFrame(age_stats), use_container_width=True, hide_index=True)
else:
    st.warning("Age data (RIDAGEYR) not available in dataset.")

st.markdown("---")

# Disease Prevalence
st.header("Disease Prevalence")

# Disease labels mapping
disease_labels = {
    'diabetes': {'col': 'DIQ010', 'name': 'Diabetes'},
    'hypertension': {'col': 'BPQ020', 'name': 'Hypertension'},
    'cvd': {'col': 'MCQ160B', 'name': 'Cardiovascular Disease'},
    'ckd': {'col': 'MCQ220', 'name': 'Chronic Kidney Disease'}
}

disease_stats = []

for disease_key, disease_info in disease_labels.items():
    col_name = disease_info['col']
    disease_name = disease_info['name']
    
    if col_name in df.columns:
        # Filter valid responses (1=Yes, 2=No)
        valid_data = df[df[col_name].isin([1, 2])]
        if len(valid_data) > 0:
            total = len(valid_data)
            disease_count = len(valid_data[valid_data[col_name] == 1])
            prevalence = (disease_count / total) * 100
            
            disease_stats.append({
                'Disease': disease_name,
                'Total Respondents': total,
                'Cases': disease_count,
                'Prevalence (%)': f"{prevalence:.2f}%",
                'Prevalence (raw)': prevalence
            })

if disease_stats:
    disease_df = pd.DataFrame(disease_stats)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Disease prevalence bar chart
        fig_disease = px.bar(
            disease_df,
            x='Disease',
            y='Prevalence (raw)',
            title="Disease Prevalence (%)",
            labels={'Prevalence (raw)': 'Prevalence (%)', 'Disease': 'Disease'},
            color='Prevalence (raw)',
            color_continuous_scale='Reds'
        )
        fig_disease.update_layout(showlegend=False, yaxis_title="Prevalence (%)")
        st.plotly_chart(fig_disease, use_container_width=True)
    
    with col2:
        # Disease cases count
        fig_cases = px.bar(
            disease_df,
            x='Disease',
            y='Cases',
            title="Number of Disease Cases",
            labels={'Cases': 'Number of Cases', 'Disease': 'Disease'},
            color='Cases',
            color_continuous_scale='Oranges'
        )
        fig_cases.update_layout(showlegend=False)
        st.plotly_chart(fig_cases, use_container_width=True)
    
    # Disease statistics table
    st.subheader("Disease Statistics Table")
    display_df = disease_df[['Disease', 'Total Respondents', 'Cases', 'Prevalence (%)']].copy()
    st.dataframe(display_df, use_container_width=True, hide_index=True)
else:
    st.warning("No disease data available in dataset.")

st.markdown("---")

# Disease by Gender
st.header("Disease Prevalence by Gender")

if 'RIAGENDR' in df.columns:
    disease_by_gender = []
    
    for disease_key, disease_info in disease_labels.items():
        col_name = disease_info['col']
        disease_name = disease_info['name']
        
        if col_name in df.columns:
            for gender_code, gender_name in [(1, 'Male'), (2, 'Female')]:
                gender_data = df[(df['RIAGENDR'] == gender_code) & (df[col_name].isin([1, 2]))]
                if len(gender_data) > 0:
                    total = len(gender_data)
                    cases = len(gender_data[gender_data[col_name] == 1])
                    prevalence = (cases / total) * 100
                    
                    disease_by_gender.append({
                        'Disease': disease_name,
                        'Gender': gender_name,
                        'Prevalence (%)': prevalence,
                        'Cases': cases,
                        'Total': total
                    })
    
    if disease_by_gender:
        gender_disease_df = pd.DataFrame(disease_by_gender)
        
        # Grouped bar chart
        fig_grouped = px.bar(
            gender_disease_df,
            x='Disease',
            y='Prevalence (%)',
            color='Gender',
            title="Disease Prevalence by Gender",
            barmode='group',
            color_discrete_map={'Male': '#3b82f6', 'Female': '#ec4899'},
            labels={'Prevalence (%)': 'Prevalence (%)', 'Disease': 'Disease'}
        )
        st.plotly_chart(fig_grouped, use_container_width=True)
        
        # Table
        st.subheader("Disease Prevalence by Gender (Table)")
        pivot_df = gender_disease_df.pivot(index='Disease', columns='Gender', values='Prevalence (%)')
        pivot_df = pivot_df.round(2)
        pivot_df.columns.name = None
        pivot_df.index.name = None
        st.dataframe(pivot_df, use_container_width=True)
else:
    st.warning("Gender data not available for disease analysis.")

st.markdown("---")

# Disease by Age Group
st.header("Disease Prevalence by Age Group")

if 'RIDAGEYR' in df.columns:
    age_disease_data = []
    
    # Create age groups
    df_age = df[df['RIDAGEYR'].notna()].copy()
    df_age['Age Group'] = pd.cut(
        df_age['RIDAGEYR'],
        bins=[0, 20, 30, 40, 50, 60, 70, 80, 200],
        labels=['0-20', '20-30', '30-40', '40-50', '50-60', '60-70', '70-80', '80+']
    )
    
    for disease_key, disease_info in disease_labels.items():
        col_name = disease_info['col']
        disease_name = disease_info['name']
        
        if col_name in df_age.columns:
            for age_group in df_age['Age Group'].cat.categories:
                age_data = df_age[
                    (df_age['Age Group'] == age_group) & 
                    (df_age[col_name].isin([1, 2]))
                ]
                if len(age_data) > 0:
                    total = len(age_data)
                    cases = len(age_data[age_data[col_name] == 1])
                    prevalence = (cases / total) * 100
                    
                    age_disease_data.append({
                        'Disease': disease_name,
                        'Age Group': str(age_group),
                        'Prevalence (%)': prevalence,
                        'Cases': cases,
                        'Total': total
                    })
    
    if age_disease_data:
        age_disease_df = pd.DataFrame(age_disease_data)
        
        # Line chart for each disease
        diseases_list = age_disease_df['Disease'].unique()
        
        if len(diseases_list) > 0:
            fig_line = go.Figure()
            
            colors = px.colors.qualitative.Set3
            for i, disease in enumerate(diseases_list):
                disease_data = age_disease_df[age_disease_df['Disease'] == disease].sort_values('Age Group')
                fig_line.add_trace(go.Scatter(
                    x=disease_data['Age Group'],
                    y=disease_data['Prevalence (%)'],
                    mode='lines+markers',
                    name=disease,
                    line=dict(width=3),
                    marker=dict(size=8)
                ))
            
            fig_line.update_layout(
                title="Disease Prevalence by Age Group",
                xaxis_title="Age Group",
                yaxis_title="Prevalence (%)",
                hovermode='x unified',
                height=500
            )
            st.plotly_chart(fig_line, use_container_width=True)
            
            # Heatmap
            st.subheader("Disease Prevalence Heatmap by Age Group")
            pivot_age = age_disease_df.pivot(index='Disease', columns='Age Group', values='Prevalence (%)')
            pivot_age = pivot_age.round(2)
            pivot_age.columns.name = None
            pivot_age.index.name = None
            
            fig_heatmap = px.imshow(
                pivot_age,
                labels=dict(x="Age Group", y="Disease", color="Prevalence (%)"),
                title="Disease Prevalence Heatmap",
                color_continuous_scale='Reds',
                aspect="auto"
            )
            st.plotly_chart(fig_heatmap, use_container_width=True)
            
            # Table
            st.subheader("Disease Prevalence by Age Group (Table)")
            st.dataframe(pivot_age, use_container_width=True)
else:
    st.warning("Age data not available for disease analysis.")

st.markdown("---")

# Additional Health Metrics
st.header("Additional Health Metrics")

health_metrics = {
    'BMI': 'BMXBMI',
    'Waist Circumference': 'BMXWAIST',
    'Systolic BP': 'BPXSY1',
    'Diastolic BP': 'BPXDI1',
    'HbA1c': 'LBXGH',
    'Total Cholesterol': 'LBXTC',
    'HDL Cholesterol': 'LBDHDD',
    'LDL Cholesterol': 'LBDLDL',
    'Triglycerides': 'LBXSTR'
}

available_metrics = {}
for metric_name, col_name in health_metrics.items():
    if col_name in df.columns:
        metric_data = df[df[col_name].notna()][col_name]
        if len(metric_data) > 0:
            available_metrics[metric_name] = {
                'column': col_name,
                'mean': metric_data.mean(),
                'median': metric_data.median(),
                'std': metric_data.std(),
                'min': metric_data.min(),
                'max': metric_data.max(),
                'count': len(metric_data)
            }

if available_metrics:
    # Summary table
    metrics_summary = []
    for metric_name, stats in available_metrics.items():
        metrics_summary.append({
            'Metric': metric_name,
            'Mean': f"{stats['mean']:.2f}",
            'Median': f"{stats['median']:.2f}",
            'Std Dev': f"{stats['std']:.2f}",
            'Min': f"{stats['min']:.2f}",
            'Max': f"{stats['max']:.2f}",
            'Sample Size': stats['count']
        })
    
    st.subheader("Health Metrics Summary")
    st.dataframe(pd.DataFrame(metrics_summary), use_container_width=True, hide_index=True)
    
    # Distribution charts for top metrics
    st.subheader("Distribution of Key Health Metrics")
    
    top_metrics = ['BMI', 'Systolic BP', 'HbA1c', 'Total Cholesterol']
    available_top = [m for m in top_metrics if m in available_metrics]
    
    if available_top:
        cols = st.columns(min(len(available_top), 2))
        for idx, metric_name in enumerate(available_top[:4]):
            col_idx = idx % 2
            with cols[col_idx]:
                col_name = available_metrics[metric_name]['column']
                metric_data = df[df[col_name].notna()][col_name]
                
                fig_dist = px.histogram(
                    metric_data,
                    nbins=30,
                    title=f"{metric_name} Distribution",
                    labels={'value': metric_name, 'count': 'Frequency'},
                    color_discrete_sequence=['#3b82f6']
                )
                fig_dist.update_layout(bargap=0.1, showlegend=False)
                st.plotly_chart(fig_dist, use_container_width=True)
else:
    st.warning("No additional health metrics available in dataset.")

st.markdown("---")

# Dataset Information
st.header("Dataset Information")

info_col1, info_col2 = st.columns(2)

with info_col1:
    st.subheader("Dataset Details")
    st.write(f"**Total Records:** {len(df):,}")
    st.write(f"**Total Columns:** {len(df.columns)}")
    st.write(f"**Memory Usage:** {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")

with info_col2:
    st.subheader("Data Quality")
    total_cells = len(df) * len(df.columns)
    missing_cells = df.isnull().sum().sum()
    completeness = ((total_cells - missing_cells) / total_cells) * 100
    
    st.write(f"**Total Cells:** {total_cells:,}")
    st.write(f"**Missing Cells:** {missing_cells:,}")
    st.write(f"**Data Completeness:** {completeness:.2f}%")
    
    # Top columns with missing data
    missing_data = df.isnull().sum().sort_values(ascending=False).head(10)
    if len(missing_data[missing_data > 0]) > 0:
        st.write("\n**Top 10 Columns with Missing Data:**")
        missing_df = pd.DataFrame({
            'Column': missing_data.index,
            'Missing Count': missing_data.values,
            'Missing %': (missing_data.values / len(df) * 100).round(2)
        })
        st.dataframe(missing_df, use_container_width=True, hide_index=True)

st.markdown("---")
st.markdown("### Note")
st.info("This page displays statistics from the NHANES 2021-2023 dataset. All disease prevalence calculations are based on self-reported data where available (1=Yes, 2=No).")

