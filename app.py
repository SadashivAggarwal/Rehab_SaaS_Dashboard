import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Rehab Outcomes SaaS Dashboard", layout="wide")

st.title("🏥 Rehab Outcomes SaaS Dashboard")
st.markdown("Simulated SaaS dashboard for physical therapy outcomes management.")

# Sidebar - user login (simulate multi-user)
user_type = st.sidebar.selectbox("User Type", ["Therapist", "Admin"])

# File uploader or sample data
st.sidebar.header("Upload Patient Data")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_csv("data/sample_patient_data.csv")

st.write("## Patient Data", df)

# Key metrics
st.subheader("Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Avg. Visits", f"{df['Visits'].mean():.1f}")
col2.metric("Avg. FIM Gain", f"{(df['Discharge_FIM']-df['Admission_FIM']).mean():.1f}")
col3.metric("Avg. Pain Reduction", f"{(df['Admission_Pain']-df['Discharge_Pain']).mean():.1f}")

# Charts
st.subheader("Patient Outcomes: FIM Score Change")
fig1 = px.histogram(df, x=(df["Discharge_FIM"] - df["Admission_FIM"]), nbins=10, labels={'x':'FIM Gain'}, title="Distribution of FIM Score Gain")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Visits vs FIM Gain by Diagnosis")
df['FIM_Gain'] = df["Discharge_FIM"] - df["Admission_FIM"]
fig2 = px.scatter(df, x="Visits", y="FIM_Gain", color="Diagnosis", hover_data=["Therapist"])
st.plotly_chart(fig2, use_container_width=True)

# Downloadable report
st.subheader("Download Data")
st.download_button("Download CSV", df.to_csv(index=False), "rehab_outcomes_report.csv")

st.info("This demo app simulates a SaaS-style dashboard for PT clinics. All data shown is synthetic.")

# Extra: Only Admin can see full raw data
if user_type == "Admin":
    st.markdown("### Full Raw Data (Admin Only)")
    st.dataframe(df)
