import streamlit as st
import json
import datetime

st.title("Caregiver Interface")
st.caption("Enter daily patient health data")
name = st.selectbox("Patient Name", ["John", "Mary", "David"])

bp = int(st.text_input("Blood Pressure", "0"))
sugar = st.number_input("Sugar Level", min_value=0)
temp = st.number_input("Temperature", min_value=0.0)

def get_status(bp, sugar, temp):
    if bp > 140 or sugar > 180 or temp > 100:
        return "Critical"
    elif bp > 120 or sugar > 140:
        return "Monitor"
    else:
        return "Normal"

if st.button("Submit"):
    status = get_status(bp, sugar, temp)

    
    entry = {
        "name": name,
        "bp": bp,
        "sugar": sugar,
        "temp": temp,
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