import streamlit as st
import pickle
import pandas as pd
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="Cardiovascular Disease Predictor",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for animations and better UI
st.markdown("""
    <style>
    /* Main background gradient - Dark Theme */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        animation: backgroundShift 15s ease infinite;
    }
    
    @keyframes backgroundShift {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    /* Card-like containers - Dark Mode */
    .main .block-container {
        background: rgba(30, 30, 46, 0.95);
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(147, 51, 234, 0.2);
    }
    
    /* Title animation - Dark Theme */
    h1 {
        background: linear-gradient(120deg, #a855f7, #ec4899, #8b5cf6, #06b6d4);
        background-size: 300% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient 4s ease infinite, float 3s ease-in-out infinite;
        font-weight: 800 !important;
        text-align: center;
        padding: 1rem 0;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    /* Subheader styling - Dark Theme */
    h2, h3 {
        color: #e0e0e0;
        font-weight: 700;
        text-shadow: 0 0 20px rgba(168, 85, 247, 0.5);
        background: linear-gradient(135deg, #a855f7 0%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline-block;
    }
    
    /* Subheader container for full width */
    .stMarkdown h2, .stMarkdown h3 {
        background: linear-gradient(135deg, #f0abfc 0%, #fbbf24 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: block;
    }
    
    /* Input field styling - Dark Theme */
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > div {
        border-radius: 10px;
        border: 2px solid rgba(147, 51, 234, 0.3);
        background: rgba(30, 30, 46, 0.8);
        color: #e0e0e0;
        transition: all 0.3s ease;
    }
    
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > div:focus {
        border-color: #a855f7;
        box-shadow: 0 0 0 3px rgba(168, 85, 247, 0.2), 0 0 20px rgba(168, 85, 247, 0.4);
        transform: scale(1.02);
    }
    
    /* Label styling */
    label {
        color: #c0c0c0 !important;
        font-weight: 500;
    }
    
    /* Button styling with pulse animation - Dark Theme */
    .stButton > button {
        background: linear-gradient(135deg, #a855f7 0%, #ec4899 50%, #f59e0b 100%);
        background-size: 200% 200%;
        color: white;
        border: none;
        border-radius: 15px;
        padding: 0.75rem 2rem;
        font-size: 1.2rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.4s ease;
        animation: gradientShift 3s ease infinite, buttonPulse 1.5s ease-in-out infinite;
        position: relative;
        overflow: hidden;
        box-shadow: 0 6px 30px rgba(168, 85, 247, 0.6), 0 0 0 0 rgba(236, 72, 153, 0.5);
    }
    
    .stButton > button::before {
        content: '✨';
        position: absolute;
        top: 50%;
        left: -30px;
        transform: translateY(-50%);
        font-size: 1.5rem;
        animation: sparkleMove 2s linear infinite;
    }
    
    .stButton > button::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        transition: left 0.5s;
    }
    
    .stButton > button:hover::after {
        left: 100%;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes buttonPulse {
        0%, 100% { 
            transform: scale(1); 
            box-shadow: 0 6px 30px rgba(168, 85, 247, 0.6), 0 0 0 0 rgba(236, 72, 153, 0.5);
        }
        50% { 
            transform: scale(1.05); 
            box-shadow: 0 8px 40px rgba(236, 72, 153, 0.8), 0 0 0 10px rgba(168, 85, 247, 0);
        }
    }
    
    @keyframes sparkleMove {
        0% { left: -30px; opacity: 0; }
        50% { opacity: 1; }
        100% { left: calc(100% + 30px); opacity: 0; }
    }
    
    @keyframes glow {
        0%, 100% { filter: brightness(1); }
        50% { filter: brightness(1.3); }
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.08);
        box-shadow: 0 12px 50px rgba(168, 85, 247, 0.8), 0 0 30px rgba(236, 72, 153, 0.6);
        animation: none;
        filter: brightness(1.2);
    }
    
    .stButton > button:active {
        transform: translateY(-1px) scale(1.03);
        box-shadow: 0 4px 20px rgba(168, 85, 247, 0.7);
    }
    
    /* Metric cards - Dark Theme */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #a855f7;
        animation: scaleIn 0.5s ease-out;
        text-shadow: 0 0 20px rgba(168, 85, 247, 0.5);
    }
    
    @keyframes scaleIn {
        from { transform: scale(0.5); opacity: 0; }
        to { transform: scale(1); opacity: 1; }
    }
    
    /* Info boxes with gradient borders - Dark Theme */
    .stAlert {
        border-radius: 15px;
        animation: fadeIn 0.5s ease-in;
        background: rgba(30, 30, 46, 0.8);
        border: 1px solid rgba(168, 85, 247, 0.3);
        color: #e0e0e0;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Success message - Dark Theme */
    .success-box {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        animation: slideIn 0.5s ease-out, shimmer 3s ease-in-out infinite;
        box-shadow: 0 8px 32px rgba(16, 185, 129, 0.4);
    }
    
    @keyframes slideIn {
        from { transform: translateX(-100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    @keyframes shimmer {
        0%, 100% { box-shadow: 0 8px 32px rgba(16, 185, 129, 0.4); }
        50% { box-shadow: 0 8px 40px rgba(16, 185, 129, 0.7); }
    }
    
    /* Warning message - Dark Theme */
    .warning-box {
        background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        animation: slideIn 0.5s ease-out, pulse-warning 2s ease-in-out infinite;
        box-shadow: 0 8px 32px rgba(239, 68, 68, 0.4);
    }
    
    @keyframes pulse-warning {
        0%, 100% { box-shadow: 0 8px 32px rgba(239, 68, 68, 0.4); }
        50% { box-shadow: 0 8px 40px rgba(239, 68, 68, 0.7); }
    }
    
    /* Divider styling - Dark Theme */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #a855f7, #ec4899, #a855f7, transparent);
        margin: 2rem 0;
        animation: dividerGlow 3s ease-in-out infinite;
    }
    
    @keyframes dividerGlow {
        0%, 100% { opacity: 0.5; }
        50% { opacity: 1; }
    }
    
    /* Card hover effect for columns */
    .element-container {
        transition: transform 0.3s ease;
    }
    
    .element-container:hover {
        transform: translateY(-2px);
    }
    
    /* Recommendation list styling - Dark Theme */
    .recommendation-item {
        background: linear-gradient(135deg, rgba(168, 85, 247, 0.1) 0%, rgba(236, 72, 153, 0.1) 100%);
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
        border-left: 4px solid #a855f7;
        animation: fadeInUp 0.5s ease-out, itemPulse 3s ease-in-out infinite;
        color: #e0e0e0;
        box-shadow: 0 4px 15px rgba(168, 85, 247, 0.2);
    }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes itemPulse {
        0%, 100% { border-left-color: #a855f7; }
        50% { border-left-color: #ec4899; }
    }
    
    /* BMI badge styling - Dark Theme */
    .bmi-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        margin-top: 0.5rem;
        animation: bounceIn 0.6s ease-out, badgeFloat 3s ease-in-out infinite;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    
    @keyframes bounceIn {
        0% { transform: scale(0.3); opacity: 0; }
        50% { transform: scale(1.05); }
        70% { transform: scale(0.9); }
        100% { transform: scale(1); opacity: 1; }
    }
    
    @keyframes badgeFloat {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
    }
    
    /* Footer styling - Dark Theme */
    .footer {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
        color: #e0e0e0;
        padding: 1.5rem;
        border-radius: 15px;
        margin-top: 2rem;
        border: 1px solid rgba(168, 85, 247, 0.3);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    }
    
    /* Particle effect overlay */
    @keyframes float-particles {
        0%, 100% { transform: translateY(0px) translateX(0px); opacity: 0.5; }
        50% { transform: translateY(-20px) translateX(10px); opacity: 0.8; }
    }
    
    /* Text glow effect */
    .glow-text {
        animation: textGlow 2s ease-in-out infinite;
    }
    
    @keyframes textGlow {
        0%, 100% { text-shadow: 0 0 10px rgba(168, 85, 247, 0.5); }
        50% { text-shadow: 0 0 20px rgba(236, 72, 153, 0.8), 0 0 30px rgba(168, 85, 247, 0.6); }
    }
    </style>
""", unsafe_allow_html=True)

# Load the trained model
@st.cache_resource
def load_model():
    with open('model.pkl', 'rb') as file:
        model = pickle.load(file)
    return model

try:
    model = load_model()
except FileNotFoundError:
    st.error("❌ Error: model.pkl file not found. Please ensure model.pkl is in the same directory as app.py")
    st.stop()

# Page title and description
st.title("❤️ Cardiovascular Disease Risk Predictor")
st.markdown("""
    <div style='text-align: center; padding: 1.5rem; background: linear-gradient(135deg, rgba(168, 85, 247, 0.1) 0%, rgba(236, 72, 153, 0.1) 100%); border-radius: 15px; margin-bottom: 2rem; border: 1px solid rgba(168, 85, 247, 0.3); animation: fadeIn 1s ease-in;'>
        <p style='font-size: 1.1rem; color: #e0e0e0; margin: 0;'>
            🏥 This app predicts the risk of cardiovascular disease based on various health parameters.<br>
            📋 Please provide your health information below to get a prediction.
        </p>
    </div>
""", unsafe_allow_html=True)

# Create two columns for input
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔢 Basic Information")
    
    age = st.number_input(
        "Age (years)",
        min_value=18,
        max_value=100,
        value=30,
        help="Age should be between 18 and 100"
    )
    
    height = st.number_input(
        "Height (cm)",
        min_value=100,
        max_value=250,
        value=170,
        help="Height in centimeters"
    )
    
    weight = st.number_input(
        "Weight (kg)",
        min_value=30,
        max_value=200,
        value=70,
        help="Weight in kilograms"
    )
    
    gender = st.selectbox(
        "Gender",
        options=[1, 2],
        format_func=lambda x: "Male" if x == 1 else "Female",
        help="1 for Male, 2 for Female"
    )

with col2:
    st.subheader("🩺 Blood Pressure & Cholesterol")
    
    systolic_bp = st.number_input(
        "Systolic Blood Pressure (mmHg)",
        min_value=60,
        max_value=250,
        value=120,
        help="Higher number in BP reading"
    )
    
    diastolic_bp = st.number_input(
        "Diastolic Blood Pressure (mmHg)",
        min_value=40,
        max_value=150,
        value=80,
        help="Lower number in BP reading"
    )
    
    cholesterol = st.selectbox(
        "Cholesterol Level",
        options=[0, 1, 2, 3],
        format_func=lambda x: ["Normal", "Above Normal", "High", "Very High"][x],
        help="0=Normal, 1=Above Normal, 2=High, 3=Very High"
    )
    
    glucose = st.selectbox(
        "Glucose Level",
        options=[0, 1, 2, 3],
        format_func=lambda x: ["Normal", "Above Normal", "High", "Very High"][x],
        help="0=Normal, 1=Above Normal, 2=High, 3=Very High"
    )

# Lifestyle factors
st.subheader("🏃 Lifestyle Factors")
col3, col4, col5 = st.columns(3)

with col3:
    smoking = st.selectbox(
        "Smoking Status",
        options=[0, 1],
        format_func=lambda x: "Non-Smoker" if x == 0 else "Smoker",
        help="0=Non-Smoker, 1=Smoker"
    )

with col4:
    alcohol = st.selectbox(
        "Alcohol Consumption",
        options=[0, 1],
        format_func=lambda x: "No" if x == 0 else "Yes",
        help="0=No, 1=Yes"
    )

with col5:
    physical_activity = st.selectbox(
        "Physical Activity",
        options=[0, 1],
        format_func=lambda x: "Inactive" if x == 0 else "Active",
        help="0=Inactive, 1=Active"
    )

# Calculate BMI
bmi = weight / ((height / 100) ** 2)

# Display BMI
st.divider()
st.subheader("📊 Health Metrics")
col_bmi, col_spacer = st.columns([1, 2])
with col_bmi:
    st.metric("Calculated BMI", f"{bmi:.2f}")
    
    # BMI Category
    if bmi < 18.5:
        bmi_category = "Underweight"
        bmi_color = "🔵"
        badge_style = "background: #3b82f6; color: white;"
    elif bmi < 25:
        bmi_category = "Normal Weight"
        bmi_color = "🟢"
        badge_style = "background: #10b981; color: white;"
    elif bmi < 30:
        bmi_category = "Overweight"
        bmi_color = "🟡"
        badge_style = "background: #f59e0b; color: white;"
    else:
        bmi_category = "Obese"
        bmi_color = "🔴"
        badge_style = "background: #ef4444; color: white;"
    
    st.markdown(f"""
        <div class='bmi-badge' style='{badge_style}'>
            {bmi_color} <strong>BMI Category:</strong> {bmi_category}
        </div>
    """, unsafe_allow_html=True)

# Prediction button
st.divider()
if st.button("🔮 Predict Risk", use_container_width=True, type="primary"):
    # Prepare features in the exact order the model was trained on
    features = pd.DataFrame([[
        0,  # Unnamed: 0 (index column)
        age, 
        height, 
        weight, 
        systolic_bp,  # ap_hi
        diastolic_bp,  # ap_lo
        cholesterol, 
        glucose,  # gluc
        smoking,  # smoke
        alcohol,  # alco
        physical_activity,  # active
        bmi
    ]], columns=['Unnamed: 0', 'age', 'height', 'weight', 'ap_hi', 'ap_lo', 'cholesterol', 'gluc', 'smoke', 'alco', 'active', 'bmi'])
    
    try:
        # Make prediction
        prediction = model.predict(features)[0]
        prediction_proba = model.predict_proba(features)[0]
        
        # Display results
        st.success("✅ Prediction Complete!")
        
        col_pred, col_conf = st.columns(2)
        
        with col_pred:
            if prediction == 0:
                st.markdown("""
                    <div class='success-box'>
                        <h2 style='color: white; margin: 0;'>🟢 Low Risk</h2>
                        <p style='font-size: 1.1rem; margin: 0.5rem 0 0 0;'>No cardiovascular disease detected.</p>
                    </div>
                """, unsafe_allow_html=True)
                risk_level = "Low"
                confidence = prediction_proba[0]
            else:
                st.markdown("""
                    <div class='warning-box'>
                        <h2 style='color: white; margin: 0;'>🔴 High Risk</h2>
                        <p style='font-size: 1.1rem; margin: 0.5rem 0 0 0;'>Cardiovascular disease risk detected.</p>
                    </div>
                """, unsafe_allow_html=True)
                risk_level = "High"
                confidence = prediction_proba[1]
        
        # Additional health advice
        st.divider()
        st.subheader("💡 Health Recommendations")
        
        recommendations = []
        
        if age > 50:
            recommendations.append("**Age Factor:** Regular check-ups are important at your age.")
        
        if bmi >= 25:
            recommendations.append("**Weight:** Consider maintaining a healthy BMI through diet and exercise.")
        
        if systolic_bp > 140 or diastolic_bp > 90:
            recommendations.append("**Blood Pressure:** Your BP is elevated. Consult a healthcare professional.")
        
        if cholesterol >= 2:
            recommendations.append("**Cholesterol:** High cholesterol levels. Discuss with your doctor about diet and medication.")
        
        if glucose >= 2:
            recommendations.append("**Glucose:** High glucose levels. Regular monitoring is recommended.")
        
        if smoking == 1:
            recommendations.append("**Smoking:** Consider quitting smoking to reduce cardiovascular risk.")
        
        if physical_activity == 0:
            recommendations.append("**Exercise:** Increase physical activity. Aim for 150 minutes of moderate activity per week.")
        
        if recommendations:
            for i, rec in enumerate(recommendations):
                st.markdown(f"""
                    <div class='recommendation-item' style='animation-delay: {i * 0.1}s;'>
                        • {rec}
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style='background: linear-gradient(135deg, #059669 0%, #10b981 100%); padding: 1.5rem; border-radius: 15px; color: white; text-align: center; animation: slideIn 0.5s ease-out, shimmer 3s ease-in-out infinite; box-shadow: 0 8px 32px rgba(16, 185, 129, 0.4);'>
                    <h3 style='color: white; margin: 0; text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);'>✅ Excellent Health!</h3>
                    <p style='margin: 0.5rem 0 0 0;'>Your health parameters look good! Keep maintaining your healthy lifestyle.</p>
                </div>
            """, unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"❌ Error in prediction: {str(e)}")
        st.info("Please ensure all inputs are valid and try again.")

# Footer
st.divider()
st.markdown("""
    <div class='footer'>
        <h3 style='color: white; margin-top: 0;'>⚠️ Important Disclaimer</h3>
        <p style='margin: 0.5rem 0;'><strong>Medical Advice:</strong> This prediction tool is for informational purposes only and should not be 
        used as a substitute for professional medical advice. Always consult with a qualified healthcare 
        professional for accurate diagnosis and treatment recommendations.</p>
        <p style='margin: 0.5rem 0 0 0;'><strong>🔒 Data Privacy:</strong> Your health information is processed locally and not stored or transmitted.</p>
    </div>
""", unsafe_allow_html=True)