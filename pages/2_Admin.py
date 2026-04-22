import streamlit as st
import json

st.title("Admin Dashboard")
st.caption("Monitor patient health and alerts")

# Load data
try:
    with open("data.json", "r") as f:
        data = json.load(f)
except:
    data = []

st.subheader("Patient Records")

# Filter option
filter_option = st.selectbox("Filter", ["All", "Critical Only"])

if not data:
    st.warning("No data available")
else:
    for d in data[::-1]:  # latest first

        if filter_option == "Critical Only" and d["status"] != "Critical":
            continue

        st.write(f"Patient: {d['name']}")
        st.write(f"BP: {d['bp']} | Sugar: {d['sugar']} | Temp: {d['temp']}")

        st.write(f"Time: {d.get('time', 'N/A')}")
        if d["status"] == "Critical":
            st.error(f"Status: {d['status']}")
        elif d["status"] == "Monitor":
            st.warning(f"Status: {d['status']}")
        else:
            st.success(f"Status: {d['status']}")

        st.markdown("---")