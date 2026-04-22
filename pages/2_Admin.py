import streamlit as st
import json
import datetime
import pandas as pd

# =========================
# 🔐 ACCESS CONTROL
# =========================
if st.session_state.get("role") != "Admin":
    st.warning("Access denied")
    st.stop()

# =========================
# 🎨 PREMIUM STYLING
# =========================
st.markdown("""
<style>
body {
    background-color: #f8fafc;
}

.card {
    padding: 18px;
    border-radius: 14px;
    background: white;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    margin-bottom: 15px;
}

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

.section {
    margin-top: 25px;
}
</style>
""", unsafe_allow_html=True)

st.title("Admin Dashboard")

# =========================
# 📊 METRICS
# =========================
with open("users.json", "r") as f:
    users = json.load(f)

try:
    with open("data.json", "r") as f:
        data = json.load(f)
except:
    data = []

col1, col2, col3 = st.columns(3)
col1.metric("Patients", len(users["patients"]))
col2.metric("Caregivers", len(users["caregivers"]))
col3.metric("Records", len(data))

# =========================
# 👥 USER MANAGEMENT
# =========================
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("User Management")

user_type = st.selectbox("Add User Type", ["Caregiver", "Patient"])
new_username = st.text_input("New Username")
new_password = st.text_input("New Password", type="password")

if st.button("Add User"):
    with open("users.json", "r") as f:
        users = json.load(f)

    all_users = users["caregivers"] + users["patients"]

    if any(u["username"] == new_username for u in all_users):
        st.error("Username already exists")
    else:
        new_user = {"username": new_username, "password": new_password}

        if user_type == "Caregiver":
            users["caregivers"].append(new_user)
        else:
            users["patients"].append(new_user)

        with open("users.json", "w") as f:
            json.dump(users, f)

        st.success(f"{user_type} added successfully!")

st.markdown("</div>", unsafe_allow_html=True)

# =========================
# 🔥 PREPARE DATA
# =========================
latest_per_patient = {}
for d in data:
    latest_per_patient[d["name"]] = d

# =========================
# 🚨 NEEDS ATTENTION
# =========================
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("🚨 Needs Attention Today")

now = datetime.datetime.now()
attention_flag = False

for d in latest_per_patient.values():
    try:
        last_time = datetime.datetime.fromisoformat(d["time"])
        diff = (now - last_time).seconds

        if d["status"] == "Critical" or diff > 3600:
            attention_flag = True

            st.markdown("<div class='card' style='border-left:5px solid #dc2626;'>", unsafe_allow_html=True)

            st.subheader(f"👤 {d['name']}")

            if d["status"] == "Critical":
                st.error("Critical condition!")

            if diff > 3600:
                st.warning("Missed check-in!")

            st.markdown("</div>", unsafe_allow_html=True)

    except:
        pass

if not attention_flag:
    st.success("All patients are stable")

st.markdown("</div>", unsafe_allow_html=True)

# =========================
# 📋 PATIENT RECORDS
# =========================
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("Patient Records")

filter_option = st.selectbox("Filter", ["All", "Critical Only"])

# 🔍 SEARCH
search = st.text_input("Search Patient")

items = list(latest_per_patient.values())

if search:
    items = [d for d in items if search.lower() in d["name"].lower()]

if not items:
    st.warning("No matching data found")
else:
    # ✅ FIXED GRID
    for i in range(0, len(items), 2):
        cols = st.columns(2)

        for j in range(2):
            if i + j >= len(items):
                break

            d = items[i + j]

            if filter_option == "Critical Only" and d["status"] != "Critical":
                continue

            with cols[j]:
                st.markdown("<div class='card'>", unsafe_allow_html=True)

                st.subheader(f"👤 {d['name']}")

                st.markdown(f"**BP:** {d.get('sys', '-')}/{d.get('dia', '-')}")
                st.markdown(f"**Sugar:** {d['sugar']} | Temp: {d['temp']}")
                st.markdown(f"**Mood:** {d.get('mood', 'N/A')}")

                # ⏱ TIME
                try:
                    last_time = datetime.datetime.fromisoformat(d["time"])
                    mins = int((datetime.datetime.now() - last_time).seconds / 60)
                    st.caption(f"Updated {mins} mins ago")
                except:
                    st.caption("Updated: N/A")

                # 📈 MINI CHART
                history = [x for x in data if x["name"] == d["name"]]

                if len(history) >= 2:
                    df = pd.DataFrame({
                        "BP": [x.get("sys", 0) for x in history]
                    })
                    st.line_chart(df)

                st.markdown("---")

                # 🚦 STATUS
                if d["status"] == "Critical":
                    st.markdown("<div class='status-critical'>🚨 CRITICAL</div>", unsafe_allow_html=True)
                elif d["status"] == "Monitor":
                    st.markdown("<div class='status-monitor'>⚠ MONITOR</div>", unsafe_allow_html=True)
                else:
                    st.markdown("<div class='status-normal'>✅ NORMAL</div>", unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)