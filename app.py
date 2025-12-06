import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Cardio Disease Predictor",
    page_icon="❤️",
    layout="wide"
)

# Simplified CSS with lighter animations
st.markdown("""
    <style>
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        color: #667eea;
        text-align: center;
        margin-bottom: 0.5rem;
        animation: fadeIn 0.8s ease-out;
    }
    
    .sub-header {
        font-size: 1.1rem;
        color: #6c757d;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .info-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
    }
    
    .section-container {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        border-left: 4px solid #667eea;
    }
    
    .section-header {
        font-size: 1.3rem;
        font-weight: 600;
        color: #667eea;
        margin-bottom: 1rem;
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 1.2rem;
        font-weight: 600;
        padding: 0.8rem;
        border-radius: 30px;
        border: none;
        margin-top: 2rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        transition: transform 0.2s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
    }
    
    .result-box-success {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-top: 2rem;
        box-shadow: 0 4px 20px rgba(17, 153, 142, 0.3);
    }
    
    .result-box-danger {
        background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-top: 2rem;
        box-shadow: 0 4px 20px rgba(235, 51, 73, 0.3);
    }
    
    .result-title {
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .footer {
        text-align: center;
        color: #6c757d;
        padding: 1.5rem;
        margin-top: 2rem;
        font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)

# Load model
@st.cache_resource
def load_model():
    return pickle.load(open("model.pkl", "rb"))

model = load_model()

# Header
st.markdown('<p class="main-header">❤️ Cardio Disease Prediction</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-Powered Health Assessment</p>', unsafe_allow_html=True)

# Info card
st.markdown("""
    <div class="info-card">
        <h3 style="margin: 0 0 0.5rem 0;">🏥 Health Assessment Tool</h3>
        <p style="margin: 0; opacity: 0.95;">
            Enter your health parameters for an instant cardiovascular risk assessment
        </p>
    </div>
""", unsafe_allow_html=True)

# Create two columns
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="section-container"><div class="section-header">👤 Personal Information</div>', unsafe_allow_html=True)
    age = st.number_input("Age (years)", min_value=18, max_value=70, value=50)
    weight = st.number_input("Weight (kg)", min_value=20, max_value=200, value=70)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown('<div class="section-container"><div class="section-header">🩺 Blood Pressure</div>', unsafe_allow_html=True)
    ap_hi = st.number_input("Systolic BP (ap_hi)", min_value=80, max_value=200, value=120)
    ap_lo = st.number_input("Diastolic BP (ap_lo)", min_value=40, max_value=150, value=80)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown('<div class="section-container"><div class="section-header">🧪 Laboratory Results</div>', unsafe_allow_html=True)
    cholesterol = st.selectbox("Cholesterol", [1, 2, 3], format_func=lambda x: {1: "1 - Normal", 2: "2 - Above Normal", 3: "3 - High"}[x])
    gluc = st.selectbox("Glucose", [1, 2, 3], format_func=lambda x: {1: "1 - Normal", 2: "2 - Above Normal", 3: "3 - High"}[x])
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown('<div class="section-container"><div class="section-header">🏃 Lifestyle Factors</div>', unsafe_allow_html=True)
    smoke = st.selectbox("Smoking", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
    alco = st.selectbox("Alcohol", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
    active = st.selectbox("Physical Activity", [0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
    st.markdown("</div>", unsafe_allow_html=True)

# Derive age_category from age
if 25 <= age <= 30:
    age_category = 'Young'
elif 31 <= age <= 50:
    age_category = 'Middle_age'
elif 51 <= age <= 70:
    age_category = 'Senior'
else:
    age_category = 'Middle_age'

# Create input DataFrame
input_df = pd.DataFrame({
    'Unnamed: 0': [0],
    'age': [age],
    'weight': [weight],
    'ap_hi': [ap_hi],
    'ap_lo': [ap_lo],
    'cholesterol': [cholesterol],
    'gluc': [gluc],
    'smoke': [smoke],
    'alco': [alco],
    'active': [active],
    'age_category': [age_category]
})

# Apply one-hot encoding
input_df = pd.get_dummies(input_df, columns=['age_category'])

# Ensure all expected columns exist
expected_cols = ['Unnamed: 0', 'age', 'weight', 'ap_hi', 'ap_lo', 'cholesterol', 'gluc', 
                 'smoke', 'alco', 'active', 'age_category_Middle_age', 
                 'age_category_Senior', 'age_category_Young']

for col in expected_cols:
    if col not in input_df.columns:
        input_df[col] = 0

input_df = input_df[expected_cols]
input_data = input_df.values

# Predict button
if st.button("🔍 Analyze Health"):
    prediction = model.predict(input_data)
    
    if prediction[0] == 1:
        st.markdown("""
            <div class="result-box-danger">
                <div class="result-title">⚠️ High Risk</div>
                <p>Your assessment indicates elevated cardiovascular risk. Please consult a healthcare professional.</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class="result-box-success">
                <div class="result-title">✅ Low Risk</div>
                <p>Your assessment shows lower cardiovascular risk. Keep up the healthy lifestyle!</p>
            </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class="footer">
        <strong>⚕️ Disclaimer:</strong> This tool provides preliminary screening only. Always consult healthcare professionals.
    </div>
""", unsafe_allow_html=True)