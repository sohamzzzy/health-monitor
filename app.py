import streamlit as st
import json

# Page config FIRST (important)
st.set_page_config(page_title="Health Monitor", layout="wide")

# Styling
st.markdown("""
<style>
body {
    background-color: #f8fafc;
}

/* Card */
.card {
    padding: 18px;
    border-radius: 14px;
    background: white;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    margin-bottom: 15px;
}

/* Status styles */
.status-critical {
    color: #dc2626;
    font-weight: bold;
    font-size: 20px;
}

.status-monitor {
    color: #f59e0b;
    font-weight: bold;
    font-size: 20px;
}

.status-normal {
    color: #16a34a;
    font-weight: bold;
    font-size: 20px;
}

/* Section spacing */
.section {
    margin-top: 25px;
}
</style>
""", unsafe_allow_html=True)

st.title("Health Monitoring System Login")

# Load users
with open("users.json", "r") as f:
    users = json.load(f)

# Role selection
role = st.selectbox("Select Role", ["Admin", "Caregiver", "Patient"])

# Username + Password
username = st.text_input("Username")
password = st.text_input("Password", type="password")

# Login button
if st.button("Login"):

    login_success = False

    # Admin login
    if role == "Admin":
        if password == users["admin"]["password"]:
            st.session_state["role"] = "Admin"
            login_success = True

    # Caregiver login
    elif role == "Caregiver":
        for u in users["caregivers"]:
            if u["username"] == username and u["password"] == password:
                st.session_state["role"] = "Caregiver"
                st.session_state["user"] = username
                login_success = True
                break

    # Patient login
    elif role == "Patient":
        for u in users["patients"]:
            if u["username"] == username and u["password"] == password:
                st.session_state["role"] = "Patient"
                st.session_state["user"] = username
                login_success = True
                break

    if not login_success:
        st.error("Invalid credentials")

# After login
if "role" in st.session_state:
    st.success(f"Logged in as {st.session_state['role']}")
    st.sidebar.success("Use sidebar to navigate")