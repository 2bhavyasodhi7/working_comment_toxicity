# -*- coding: utf-8 -*-
"""main2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1e_Zs3sgwZeWRhZF9r12x2B_bgEkSaIIB
"""

import streamlit as st
import numpy as np
import requests
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import TextVectorization

# Model download link (update this with your own Hugging Face or raw URL)
MODEL_URL = "https://huggingface.co/2bhavyasodhi7/comment_toxicity/resolve/main/toxicity.h5"
MODEL_PATH = "toxicity.h5"

# Function to download and load model
@st.cache_resource
def download_model():
    if not os.path.exists(MODEL_PATH):
        with st.spinner("Downloading model... Please wait ⏳"):
            response = requests.get(MODEL_URL, stream=True)
            with open(MODEL_PATH, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
    return load_model(MODEL_PATH)

# Load the model
model = download_model()

# Get the TextVectorization layer (assumed to be first)
vectorizer_layer = None
for layer in model.layers:
    if isinstance(layer, TextVectorization):
        vectorizer_layer = layer
        break

# Prediction function
def predict_toxicity(text):
    if vectorizer_layer is None:
        return ["Model missing vectorizer layer."]

    vectorized = vectorizer_layer(np.array([text]))
    prediction = model.predict(vectorized)[0]
    labels = ["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]
    toxic_tags = [labels[i] for i, val in enumerate(prediction) if val > 0.5]
    return toxic_tags if toxic_tags else ["Clean / Non-toxic"]

# Streamlit App UI
st.title("💬 Toxic Comment Detector")
st.markdown("Enter a comment and check if it's **toxic** or **clean**.")

user_input = st.text_area("📝 Enter your comment here:")

if st.button("Analyze"):
    if user_input.strip():
        result = predict_toxicity(user_input)
        st.success("Prediction complete!")
        st.write("🚨 **Detected Tags:**", ", ".join(result))
    else:
        st.warning("Please enter a comment to analyze.")

# About
st.markdown("""
---
### ℹ️ About This App
This app uses a pre-trained deep learning model to detect toxic comments.

**Labels:** toxic, severe toxic, obscene, threat, insult, identity hate
Model trained on Jigsaw Toxic Comment Dataset.
""")