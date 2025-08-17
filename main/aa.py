import streamlit as st
import requests
from PIL import Image

API_URL = "https://fraud-detect-35nr.onrender.com"


st.set_page_config(page_title="Fraud Detection", layout="centered")


page = st.sidebar.selectbox("Select Page", ["Home", "Prediction"])

if page == "Home":
    st.title("Fraud Detection App")
    st.markdown("""
        Welcome to the Fraud Detection App.  
        Use the **Prediction** page to enter insurance claim details and check if a claim is **Fraudulent** or **Not Fraudulent**.
    """)

    st.image("image/Enterprise_Security.jpg", use_container_width=True)

elif page == "Prediction":
    st.title(" Predict Insurance Fraud")
    st.markdown("Enter the claim details below:")

    with st.form(key='claim_form'):
        AddressChange_Claim = st.radio(
            "Address Change During Claim",
            options=[0, 1],
            format_func=lambda x: "No" if x == 0 else "Yes"
        )
        
        BasePolicy = st.selectbox(
            "Base Policy Type",
            options=[0, 1, 2],
            format_func=lambda x: ["Type A", "Type B", "Type C"][x]
        )
        
        VehiclePrice = st.slider("Vehicle Price", 0.0, 100000.0, 20000.0, 500.0)
        Deductible = st.slider("Deductible", 0.0, 5000.0, 500.0, 100.0)
        Fault = st.radio("Was the policyholder at Fault?", [0, 1], format_func=lambda x: "No" if x==0 else "Yes")
        PolicyNumber = st.number_input("Policy Number", min_value=1.0, value=1001.0, step=1.0)
        PastNumberOfClaims = st.number_input("Past Number of Claims", 0.0, value=0.0, step=1.0)

        submit_button = st.form_submit_button(label="Predict Fraud")

    if submit_button:
        payload = {
            "AddressChange_Claim": AddressChange_Claim,
            "BasePolicy": BasePolicy,
            "VehiclePrice": VehiclePrice,
            "Deductible": Deductible,
            "Fault": Fault,
            "PolicyNumber": PolicyNumber,
            "PastNumberOfClaims": PastNumberOfClaims
        }

        try:
            response = requests.post(f"{API_URL}/predict", json=payload)
            if response.status_code == 200:
                prediction = response.json()["prediction"]
                if prediction == "Fraud":
                    st.error(f"Prediction: {prediction}")
                    
                    fraud_image = Image.open("image/imaa.jpg") 
                    st.image(fraud_image, caption=" Fraud Alert!", use_column_width=True)
                else:
                    st.success(f"Prediction: {prediction}")

                    fraud_image = Image.open("image/nofraud.jpg") 
                    st.image(fraud_image, caption=" No Fraud Detected",width=200)
            else:
                st.warning("Error from API: " + response.text)
        except Exception as e:
            st.error(f"Failed to connect to API: {e}")
