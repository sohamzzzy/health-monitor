import streamlit as st
import json
import datetime
import pandas as pd

# =========================
# ACCESS CONTROL
# =========================
if st.session_state.get("role") != "Admin":
    st.warning("Access denied")
    st.stop()

# =========================
# STYLING
# =========================
st.markdown("""
<style>
body { background-color: #f8fafc; }

.card {
    padding: 16px;
    border-radius: 12px;
    background: white;
    box-shadow: 0 6px 16px rgba(0,0,0,0.06);
    margin-bottom: 12px;
    border: 1px solid #e5e7eb;
}

.card-title {
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 6px;
}

.card-meta {
    font-size: 13px;
    color: #6b7280;
    margin-bottom: 10px;
}

.card-divider {
    margin: 10px 0;
}

.status-critical { color: #dc2626; font-weight: bold; }
.status-monitor { color: #f59e0b; font-weight: bold; }
.status-normal { color: #16a34a; font-weight: bold; }

.section { margin-top: 25px; }
</style>
""", unsafe_allow_html=True)

st.title("Admin Dashboard")

# =========================
# LOAD DATA
# =========================
with open("users.json") as f:
    users = json.load(f)

try:
    with open("data.json") as f:
        data = json.load(f)
except:
    data = []

# =========================
# METRICS
# =========================
col1, col2, col3 = st.columns(3)
col1.metric("Patients", len(users["patients"]))
col2.metric("Caregivers", len(users["caregivers"]))
col3.metric("Records", len(data))

# =========================
# USER MANAGEMENT
# =========================
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("User Management")

user_type = st.selectbox("Type", ["Caregiver", "Patient"])
u = st.text_input("Username")
p = st.text_input("Password", type="password")

if st.button("Add User"):
    all_users = users["caregivers"] + users["patients"]

    if any(x["username"] == u for x in all_users):
        st.error("Username exists")
    else:
        new = {"username": u, "password": p}
        users["caregivers" if user_type == "Caregiver" else "patients"].append(new)

        with open("users.json", "w") as f:
            json.dump(users, f)

        st.success("User added")

# =========================
# PREP DATA
# =========================
latest = {}
for d in data:
    latest[d["name"]] = d

# =========================
# 🚨 NEEDS ATTENTION (FIXED GRID)
# =========================
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("🚨 Needs Attention")

attention_items = []

for d in latest.values():
    try:
        t = datetime.datetime.fromisoformat(d["time"])
        diff = (datetime.datetime.now() - t).seconds

        if d["status"] == "Critical" or diff > 3600:
            attention_items.append((d, diff))
    except:
        pass

if not attention_items:
    st.success("All patients are stable")

for i in range(0, len(attention_items), 2):
    cols = st.columns(2)

    for j in range(2):
        if i + j >= len(attention_items):
            break

        d, diff = attention_items[i + j]

        with cols[j]:
            st.markdown("<div class='card'>", unsafe_allow_html=True)

            st.markdown(f"<div class='card-title'>👤 {d['name']}</div>", unsafe_allow_html=True)

            if d["status"] == "Critical":
                st.error("Critical condition")

            if diff > 3600:
                st.warning("Missed check-in")

            st.markdown("</div>", unsafe_allow_html=True)

# =========================
# PATIENT RECORDS
# =========================
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("Patient Records")

search = st.text_input("Search Patient")
filter_option = st.selectbox("Filter", ["All", "Critical Only"])

items = list(latest.values())

# SEARCH
if search:
    items = [d for d in items if search.lower() in d["name"].lower()]

# FILTER
if filter_option == "Critical Only":
    items = [d for d in items if d["status"] == "Critical"]

if not items:
    st.warning("No matching records")

# =========================
# GRID (ALIGNED)
# =========================
for i in range(0, len(items), 2):
    cols = st.columns(2)

    for j in range(2):
        if i + j >= len(items):
            break

        d = items[i + j]

        with cols[j]:
            st.markdown("<div class='card'>", unsafe_allow_html=True)

            # HEADER
            st.markdown(f"<div class='card-title'>👤 {d['name']}</div>", unsafe_allow_html=True)

            # TIME
            try:
                t = datetime.datetime.fromisoformat(d["time"])
                mins = int((datetime.datetime.now() - t).seconds / 60)
                st.markdown(f"<div class='card-meta'>Updated {mins} mins ago</div>", unsafe_allow_html=True)
            except:
                pass

            # VITALS
            st.markdown(f"**BP:** {d.get('sys','-')}/{d.get('dia','-')}")
            st.markdown(f"**Sugar:** {d['sugar']} | **Temp:** {d['temp']}")
            st.markdown(f"**Mood:** {d.get('mood','-')}")

            st.markdown("<div class='card-divider'></div>", unsafe_allow_html=True)

            # CHART
            hist = [x for x in data if x["name"] == d["name"]]
            hist = sorted(hist, key=lambda x: x.get("time", ""))

            bp = [x.get("sys") for x in hist if x.get("sys") is not None]

            if len(bp) >= 2:
                st.line_chart(pd.DataFrame({"BP": bp}))

            # STATUS
            if d["status"] == "Critical":
                st.markdown("<div class='status-critical'>🚨 CRITICAL</div>", unsafe_allow_html=True)
            elif d["status"] == "Monitor":
                st.markdown("<div class='status-monitor'>⚠ MONITOR</div>", unsafe_allow_html=True)
            else:
                st.markdown("<div class='status-normal'>✅ NORMAL</div>", unsafe_allow_html=True)

            st.markdown("</div>", unsafe_allow_html=True)