import streamlit as st
import requests
import pickle
import time

# Load important features list
with open('../features.pkl', 'rb') as f:
    important_features = pickle.load(f)

# Custom CSS for better styling
st.markdown("""
    <style>
    .big-title {
        font-size: 3em;
        font-weight: bold;
        text-align: center;
        margin-bottom: 10px;
    }
    .description {
        font-size: 1.2em;
        text-align: center;
        color: #555555;
        margin-bottom: 30px;
    }
    .symptom-checkbox label {
        font-size: 1.1em !important;
    }
    .prediction-result {
        font-size: 1.8em;
        text-align: center;
        font-weight: bold;
        color: green;
    }
    .health-tip {
        font-size: 1.2em;
        color: #3366cc;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="big-title">🩺 Disease Prediction App 🤒</div>', unsafe_allow_html=True)
st.markdown('<div class="description">AI-powered disease prediction based on your symptoms.<br>Fast, simple, and educational!</div>', unsafe_allow_html=True)

st.divider()

# Symptom selection
st.subheader("🔍 Select Your Symptoms")
st.caption("Tick the symptoms you are currently experiencing:")

user_input = {}
emoji_map = ["🤧", "🤒", "😷", "🤢", "🤕", "🤮", "😵", "😴", "😰", "🥵"]

# Make checkboxes bigger
for idx, feature in enumerate(important_features):
    emoji = emoji_map[idx % len(emoji_map)]  # Rotate emojis
    user_input[feature] = st.checkbox(f"{emoji} {feature}", key=feature)

# Predict button
if st.button("🚀 Predict Disease", use_container_width=True):
    with st.spinner('Analyzing your symptoms... 🔎'):
        # Simulate loading
        for i in range(80):
            time.sleep(0.01)
            st.progress(i + 1)
    
    # API request
    api_url = "https://api-deploy-6wmx.onrender.com/predict"  # Your Render URL

    payload = {
        "input_data": user_input
    }

    try:
        response = requests.post(api_url, json=payload)
        if response.status_code == 200:
            prediction = response.json()['prediction']
            st.markdown(f'<div class="prediction-result">🩺 Predicted Disease: {prediction}</div>', unsafe_allow_html=True)
            
            # Health tip suggestions based on prediction
            st.markdown("<br>", unsafe_allow_html=True)
            st.subheader("💡 Health Tip:")
            st.markdown('<div class="health-tip">', unsafe_allow_html=True)

            if prediction.lower() == "flu":
                st.write("- Stay hydrated 🥤\n- Get lots of rest 🛌\n- See a doctor if symptoms worsen 👩‍⚕️")
            elif prediction.lower() == "migraine":
                st.write("- Rest in a quiet dark room 🕶️\n- Avoid trigger foods 🚫🍫\n- Use prescribed medications 💊")
            else:
                st.write("- Please consult a healthcare provider for a complete diagnosis. 👨‍⚕️👩‍⚕️")
            
            st.markdown('</div>', unsafe_allow_html=True)

        else:
            st.error(f"🚫 Error: {response.text}")
    except Exception as e:
        st.error(f"❗ Failed to connect to API: {e}")

# Footer
st.divider()
st.caption("Built with ❤️ using Streamlit | Not a substitute for professional medical advice.")
