import streamlit as st
import json

# Styling
st.markdown("""
<style>
.card {
    padding: 15px;
    border-radius: 10px;
    background-color: #f5f5f5;
    margin-bottom: 10px;
}
.big-status {
    font-size: 28px;
    font-weight: bold;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# Access control
if st.session_state.get("role") != "Patient":
    st.warning("Access denied")
    st.stop()

st.title("Patient Health Summary")
st.caption("Your latest health status")

# Get logged-in patient
name = st.session_state.get("user")

if not name:
    st.warning("User not found. Please login again.")
    st.stop()

# Load data
try:
    with open("data.json", "r") as f:
        data = json.load(f)
except:
    data = []

# Filter data for THIS patient only
filtered = [d for d in data if d["name"] == name]

st.markdown("<div class='card'>", unsafe_allow_html=True)

if not filtered:
    st.warning("No health data available for you yet.")
else:
    latest = filtered[-1]

    # Patient name
    st.markdown(f"<h2 style='text-align:center;'>Patient: {name}</h2>", unsafe_allow_html=True)

    st.markdown("---")

    # Vitals in 2 columns
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"**BP:** {latest.get('sys', '-')}/{latest.get('dia', '-')}")
        st.markdown(f"**Sugar:** {latest['sugar']}")

    with col2:
        st.markdown(f"**Temp:** {latest['temp']}")
        st.markdown(f"**Mood:** {latest.get('mood', 'N/A')}")

    st.caption(f"Last updated: {latest.get('time', 'N/A')}")

    st.markdown("---")

    # Status (BIG + clear)
    if latest["status"] == "Critical":
        st.markdown("<div class='big-status' style='color:red;'>CRITICAL</div>", unsafe_allow_html=True)
        st.error("Immediate medical attention required!")
    elif latest["status"] == "Monitor":
        st.markdown("<div class='big-status' style='color:orange;'>MONITOR</div>", unsafe_allow_html=True)
        st.warning("Health needs monitoring")
    else:
        st.markdown("<div class='big-status' style='color:green;'>NORMAL</div>", unsafe_allow_html=True)
        st.success("You are in good condition")

    st.markdown("---")

st.markdown("</div>", unsafe_allow_html=True)