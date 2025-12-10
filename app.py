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
    This app predicts the risk of cardiovascular disease based on various health parameters.
    Please provide your health information below to get a prediction.
""")

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
    elif bmi < 25:
        bmi_category = "Normal Weight"
        bmi_color = "🟢"
    elif bmi < 30:
        bmi_category = "Overweight"
        bmi_color = "🟡"
    else:
        bmi_category = "Obese"
        bmi_color = "🔴"
    
    st.write(f"{bmi_color} **BMI Category:** {bmi_category}")

# Prediction button
st.divider()
if st.button("🔮 Predict Risk", use_container_width=True, type="primary"):
    # Prepare features in the exact order the model was trained on
    # Order: Unnamed: 0, age, gender, height, weight, ap_hi, ap_lo, cholesterol, gluc, smoke, alco, active, bmi
    feature_array = np.array([[
        0,  # Unnamed: 0 (index)
        age, 
        gender, 
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
    ]])
    
    try:
        # Make prediction
        prediction = model.predict(feature_array)[0]
        prediction_proba = model.predict_proba(feature_array)[0]
        
        # Display results
        #st.success("✅ Prediction Complete!")
        
        col_pred, col_conf = st.columns(2)
        
        # with col_pred:
        #     if prediction == 0:
        #         st.info("### 🟢 Low Risk\nNo cardiovascular disease detected.")
        #         risk_level = "Low"
        #         confidence = prediction_proba[0]
        #     else:
        #         st.warning("### 🔴 High Risk\nCardiovascular disease risk detected.")
        #         risk_level = "High"
        #         confidence = prediction_proba[1]
        
        # with col_conf:
        #     st.metric("Confidence Level", f"{confidence*100:.2f}%")
        
        # Additional health advice
        st.divider()
        st.subheader("💡 Health Recommendations")
        
        recommendations = []
        
        if age > 50:
            recommendations.append("• **Age Factor:** Regular check-ups are important at your age.")
        
        if bmi >= 25:
            recommendations.append("• **Weight:** Consider maintaining a healthy BMI through diet and exercise.")
        
        if systolic_bp > 140 or diastolic_bp > 90:
            recommendations.append("• **Blood Pressure:** Your BP is elevated. Consult a healthcare professional.")
        
        if cholesterol >= 2:
            recommendations.append("• **Cholesterol:** High cholesterol levels. Discuss with your doctor about diet and medication.")
        
        if glucose >= 2:
            recommendations.append("• **Glucose:** High glucose levels. Regular monitoring is recommended.")
        
        if smoking == 1:
            recommendations.append("• **Smoking:** Consider quitting smoking to reduce cardiovascular risk.")
        
        if physical_activity == 0:
            recommendations.append("• **Exercise:** Increase physical activity. Aim for 150 minutes of moderate activity per week.")
        
        if recommendations:
            for rec in recommendations:
                st.write(rec)
        else:
            st.success("✅ Your health parameters look good! Keep maintaining your healthy lifestyle.")
    
    except Exception as e:
        st.error(f"❌ Error in prediction: {str(e)}")
        st.info("Please ensure all inputs are valid and try again.")

# Footer
st.divider()
st.markdown("""
---
**⚠️ Disclaimer:** This prediction tool is for informational purposes only and should not be 
used as a substitute for professional medical advice. Always consult with a qualified healthcare 
professional for accurate diagnosis and treatment recommendations.

**Data Privacy:** Your health information is processed locally and not stored or transmitted.
""")
