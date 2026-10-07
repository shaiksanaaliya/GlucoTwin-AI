import streamlit as st
import pandas as pd
import joblib
from datetime import datetime

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="GlucoTwin AI",
    page_icon="🩺",
    layout="wide"
)

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>

.main {
    background-color: #f7f9fc;
}

.hero {
    padding: 25px;
    border-radius: 18px;
    background: linear-gradient(135deg, #0f766e, #14b8a6);
    color: white;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 42px;
    margin-bottom: 5px;
}

.hero p {
    font-size: 18px;
}

.card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #e5e7eb;
    margin-bottom: 15px;
}

.risk-high {
    padding: 20px;
    border-radius: 15px;
    background-color: #fee2e2;
    border: 2px solid #ef4444;
    color: #991b1b;
}

.risk-medium {
    padding: 20px;
    border-radius: 15px;
    background-color: #fef3c7;
    border: 2px solid #f59e0b;
    color: #92400e;
}

.risk-low {
    padding: 20px;
    border-radius: 15px;
    background-color: #dcfce7;
    border: 2px solid #22c55e;
    color: #166534;
}

.footer {
    text-align: center;
    color: #6b7280;
    padding: 25px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# LOAD MODEL
# --------------------------------------------------

MODEL_PATH = "glucotwin_random_forest.pkl"

try:
    model = joblib.load(MODEL_PATH)
    model_loaded = True
except Exception:
    model = None
    model_loaded = False

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown("""
<div class="hero">

<h1>🩺 GlucoTwin AI</h1>

<p>
A Personalized Digital Twin for Early Prediction of Blood Glucose Spikes
</p>

<p>
Combining historical health information with wearable data
to estimate future glucose-spike risk.
</p>

</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.header("👤 Patient Profile")

age = st.sidebar.number_input(
    "Age",
    min_value=18,
    max_value=100,
    value=50
)

gender = st.sidebar.selectbox(
    "Gender",
    ["Female", "Male"]
)

bmi = st.sidebar.number_input(
    "BMI",
    min_value=10.0,
    max_value=60.0,
    value=27.0,
    step=0.1
)

hba1c = st.sidebar.number_input(
    "HbA1c",
    min_value=3.0,
    max_value=15.0,
    value=6.5,
    step=0.1
)

systolic_bp = st.sidebar.number_input(
    "Systolic Blood Pressure",
    min_value=80,
    max_value=220,
    value=135
)

diabetes_history = st.sidebar.selectbox(
    "Diabetes History",
    [0, 1],
    format_func=lambda x: "Yes" if x == 1 else "No"
)

family_history = st.sidebar.selectbox(
    "Family History",
    [0, 1],
    format_func=lambda x: "Yes" if x == 1 else "No"
)

# --------------------------------------------------
# WEARABLE DATA
# --------------------------------------------------

st.subheader("⌚ Current Wearable Data")

col1, col2, col3, col4 = st.columns(4)

with col1:
    glucose = st.number_input(
        "Current Glucose (mg/dL)",
        min_value=40.0,
        max_value=400.0,
        value=149.7,
        step=0.1
    )

with col2:
    heart_rate = st.number_input(
        "Heart Rate (BPM)",
        min_value=30.0,
        max_value=200.0,
        value=72.0,
        step=1.0
    )

with col3:
    steps = st.number_input(
        "Steps",
        min_value=0,
        max_value=30000,
        value=850,
        step=50
    )

with col4:
    sleep_hours = st.number_input(
        "Sleep Hours",
        min_value=0.0,
        max_value=24.0,
        value=5.8,
        step=0.1
    )

# --------------------------------------------------
# TREND INPUTS
# --------------------------------------------------

st.subheader("📈 Recent Health Trends")

col1, col2, col3 = st.columns(3)

with col1:
    glucose_change_1h = st.number_input(
        "Glucose Change — 1 Hour",
        value=20.0,
        step=0.1
    )

with col2:
    glucose_change_2h = st.number_input(
        "Glucose Change — 2 Hours",
        value=35.0,
        step=0.1
    )

with col3:
    glucose_rolling_3h = st.number_input(
        "3-Hour Average Glucose",
        value=130.0,
        step=0.1
    )

col1, col2, col3 = st.columns(3)

with col1:
    glucose_rolling_std_3h = st.number_input(
        "3-Hour Glucose Variability",
        value=15.0,
        step=0.1
    )

with col2:
    heart_rate_change_1h = st.number_input(
        "Heart Rate Change — 1 Hour",
        value=3.0,
        step=0.1
    )

with col3:
    steps_rolling_3h = st.number_input(
        "Steps — 3 Hour Rolling Total",
        value=1500.0,
        step=50.0
    )

# --------------------------------------------------
# TIME FEATURES
# --------------------------------------------------

current_time = datetime.now()

hour = current_time.hour
day_of_week = current_time.weekday()

# --------------------------------------------------
# SNAPSHOT
# --------------------------------------------------

st.subheader("📊 Current Health Snapshot")

m1, m2, m3, m4 = st.columns(4)

m1.metric(
    "Glucose",
    f"{glucose:.1f} mg/dL"
)

m2.metric(
    "Heart Rate",
    f"{heart_rate:.0f} BPM"
)

m3.metric(
    "Steps",
    f"{steps:,}"
)

m4.metric(
    "Sleep",
    f"{sleep_hours:.1f} hrs"
)

# --------------------------------------------------
# ILLUSTRATIVE TREND
# --------------------------------------------------

st.subheader("📈 Glucose Trend")

trend_values = [
    glucose_rolling_3h - (glucose_change_2h * 0.4),
    glucose_rolling_3h - (glucose_change_1h * 0.3),
    glucose - glucose_change_1h,
    glucose
]

trend_df = pd.DataFrame(
    {
        "Glucose": trend_values
    },
    index=[
        "Earlier",
        "3 Hours Ago",
        "1 Hour Ago",
        "Current"
    ]
)

st.line_chart(trend_df)

# --------------------------------------------------
# PREDICTION
# --------------------------------------------------

st.subheader("🤖 Glucose Spike Prediction")

if model_loaded:

    input_data = pd.DataFrame(
        {
            "glucose": [glucose],
            "heart_rate": [heart_rate],
            "steps": [steps],
            "sleep_hours": [sleep_hours],
            "age": [age],
            "gender": [gender],
            "bmi": [bmi],
            "hba1c": [hba1c],
            "systolic_bp": [systolic_bp],
            "diabetes_history": [diabetes_history],
            "family_history": [family_history],
            "hour": [hour],
            "day_of_week": [day_of_week],
            "glucose_change_1h": [glucose_change_1h],
            "glucose_change_2h": [glucose_change_2h],
            "glucose_rolling_3h": [glucose_rolling_3h],
            "glucose_rolling_std_3h": [glucose_rolling_std_3h],
            "heart_rate_change_1h": [heart_rate_change_1h],
            "steps_rolling_3h": [steps_rolling_3h]
        }
    )

    try:

        prediction = model.predict(input_data)[0]

        probability = model.predict_proba(input_data)[0][1]

        if probability >= 0.70:
            risk = "HIGH"
            risk_class = "risk-high"

        elif probability >= 0.40:
            risk = "MEDIUM"
            risk_class = "risk-medium"

        else:
            risk = "LOW"
            risk_class = "risk-low"

        col1, col2 = st.columns(2)

        with col1:

            st.markdown(
                f"""
                <div class="{risk_class}">

                <h2>Risk Level: {risk}</h2>

                <p>
                Estimated glucose-spike probability:
                <strong>{probability * 100:.1f}%</strong>
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:

            st.metric(
                "Prediction",
                "Potential Spike"
                if prediction == 1
                else "No Spike"
            )

        # --------------------------------------------------
        # KEY SIGNALS
        # --------------------------------------------------

        st.subheader("🔎 Key Signals")

        signals = []

        if glucose_change_2h > 25:
            signals.append(
                "Glucose has increased considerably over the recent 2-hour period."
            )

        if glucose_change_1h > 10:
            signals.append(
                "Recent 1-hour glucose movement is upward."
            )

        if sleep_hours < 6:
            signals.append(
                "Sleep duration is below 6 hours."
            )

        if hba1c >= 6.5:
            signals.append(
                "HbA1c is at or above 6.5% in this prototype input."
            )

        if steps_rolling_3h < 1000:
            signals.append(
                "Recent physical activity is relatively low."
            )

        if not signals:
            signals.append(
                "No major prototype warning signals were detected from the entered values."
            )

        for signal in signals:
            st.write("•", signal)

    except Exception as e:

        st.error(
            "Prediction could not be generated. "
            f"Model/input compatibility issue: {e}"
        )

else:

    st.error(
        "Model file not found. Please make sure "
        "`glucotwin_random_forest.pkl` is in the same folder as app.py."
    )

# --------------------------------------------------
# HOW IT WORKS
# --------------------------------------------------

st.subheader("🧠 How GlucoTwin AI Works")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("""
    ### 1️⃣ EHR
    Historical patient information such as age, BMI, HbA1c and medical history.
    """)

with c2:
    st.markdown("""
    ### 2️⃣ Wearables
    Current glucose, heart rate, steps and sleep information.
    """)

with c3:
    st.markdown("""
    ### 3️⃣ AI Model
    A Random Forest model analyzes patient and time-series features.
    """)

with c4:
    st.markdown("""
    ### 4️⃣ Prediction
    The system estimates the probability of a future glucose spike.
    """)

# --------------------------------------------------
# DISCLAIMER
# --------------------------------------------------

st.warning(
    "⚠️ This is a synthetic-data research prototype. "
    "It is not clinically validated and must not be used "
    "for diagnosis, treatment, medication or emergency decisions."
)

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("""
<div class="footer">

<strong>GlucoTwin AI</strong><br>

Digital Twin Proof-of-Concept for Predictive Health Monitoring<br>

Built for healthcare innovation and educational research.

</div>
""", unsafe_allow_html=True)
