import streamlit as st
import json
import datetime
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
if st.session_state.get("role") != "Caregiver":
    st.warning("Access denied")
    st.stop()
st.title("Caregiver Interface")
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.caption("Enter daily patient health data")
name = st.selectbox("Patient Name", ["John", "Mary", "David"])

st.subheader("Vitals")

col1, col2 = st.columns(2)

with col1:
    sys = st.number_input("Systolic BP")

with col2:
    dia = st.number_input("Diastolic BP")

sugar = st.number_input("Sugar Level")
temp = st.number_input("Temperature")
st.subheader("Additional Info")

mood = st.selectbox("Mood", ["Good", "Okay", "Bad"])
notes = st.text_area("Notes (optional)")
def get_status(sys, sugar, temp):
    if sys > 140 or sugar > 180 or temp > 100:
        return "Critical"
    elif sys > 120 or sugar > 140:
        return "Monitor"
    else:
        return "Normal"
st.markdown("</div>", unsafe_allow_html=True)
if st.button("Submit"):
    status = get_status(sys, sugar, temp)

    
    import datetime

    entry = {
        "name": name,
        "sys": sys,
        "dia": dia,
        "sugar": sugar,
        "temp": temp,
        "mood": mood,
        "notes": notes,
        "status": status,
        "time": str(datetime.datetime.now())
    }

    try:
        with open("data.json", "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append(entry)

    with open("data.json", "w") as f:
        json.dump(data, f)

    st.success(f"Saved! Status: {status}")