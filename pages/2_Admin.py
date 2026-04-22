import streamlit as st
import json
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

if st.session_state.get("role") != "Admin":
    st.warning("Access denied")
    st.stop()

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

        st.markdown("<div class='card'>", unsafe_allow_html=True)

        st.subheader(f"Patient: {d['name']}")

        st.markdown(f"**BP:** {d.get('sys', '-')}/{d.get('dia', '-')}")
        st.markdown(f"**Sugar:** {d['sugar']} | **Temp:** {d['temp']}")
        st.markdown(f"**Mood:** {d.get('mood', 'N/A')}")
        st.markdown(f"**Notes:** {d.get('notes', '-')}")
        st.markdown(f"**Time:** {d.get('time', 'N/A')}")
        
        # Status
        if d["status"] == "Critical":
            st.markdown(
                "<h4 style='color:red;'>CRITICAL</h4>",
                unsafe_allow_html=True
            )
        elif d["status"] == "Monitor":
            st.markdown(
                "<h4 style='color:orange;'>MONITOR</h4>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                "<h4 style='color:green;'>NORMAL</h4>",
                unsafe_allow_html=True
            )
        st.markdown("---")
        st.markdown("</div>", unsafe_allow_html=True)