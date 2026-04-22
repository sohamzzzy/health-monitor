import streamlit as st
import json

st.title("Patient Health Summary")
st.caption("Your latest health status")
# Load data
try:
    with open("data.json", "r") as f:
        data = json.load(f)
except:
    data = []

if not data:
    st.warning("No health data available")
else:
    latest = data[-1]

    st.subheader(f"Patient: {latest['name']}")

    st.write(f"Blood Pressure: {latest['bp']}")
    st.write(f"Sugar Level: {latest['sugar']}")
    st.write(f"Temperature: {latest['temp']}")

    st.markdown("---")

    if latest["status"] == "Critical":
        st.error("⚠ Immediate medical attention required!")
    elif latest["status"] == "Monitor":
        st.warning("⚠ Health needs monitoring")
    else:
        st.success("✔ You are in good condition")