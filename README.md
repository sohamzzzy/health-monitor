# 🩺 Health Monitoring System

A smart, role-based health monitoring system designed for elderly care environments.  
It enables caregivers to record patient vitals, while automatically detecting critical conditions and missed check-ins.

---

## 🚀 Features

- 👤 **Multi-User System**
  - Admin, Caregiver, and Patient roles
  - Admin can dynamically add users

- 📊 **Admin Dashboard**
  - Real-time overview of patients, caregivers, and records
  - “Needs Attention” section for critical cases

- ❤️ **Health Tracking**
  - Blood Pressure (Systolic/Diastolic)
  - Sugar Levels, Temperature
  - Mood & Notes

- 🚨 **Smart Alerts**
  - Automatically flags:
    - Critical health conditions
    - Missed check-ins

- 📈 **Trend Visualization**
  - Mini charts to track BP trends over time

- 🔍 **Search & Filter**
  - Quickly find patients
  - Filter critical cases

- 🔐 **User-Based Access**
  - Patients can only view their own data

---

## 🧠 System Logic

The system simulates intelligent behavior using rule-based detection:

- Critical: High BP / Sugar / Temperature
- Monitor: Slightly elevated values
- Missed Check-in: No update within a time threshold

---

## 🛠️ Tech Stack

- **Frontend + Backend:** Streamlit
- **Data Storage:** JSON (lightweight, no DB)
- **Deployment:** Render

---

## 📦 Project Structure

├── app.py

├── pages/

│ ├── 1_Caregiver.py

│ ├── 2_Admin.py

│ └── 3_Patient.py

├── users.json

├── data.json

├── requirements.txt

└── runtime.txt


---

## ⚙️ Setup (Local)

```bash
git clone (https://github.com/sohamzzzy/health-monitor.git)

cd health-monitor

pip install -r requirements.txt

streamlit run app.py

---

## 🌐 Deployment

Deployed on Render:  
https://health-monitor-wsnl.onrender.com

---

## ⚠️ Note

- Data is stored in JSON files  
- On free hosting (Render), data may reset after redeploy  

---

## 🎯 Future Improvements

- Database integration (MongoDB / Firebase)
- Secure authentication (hashed passwords)
- Mobile-friendly UI
- Advanced analytics / AI predictions

---

## 👨‍💻 Author

Built by Soham 🚀
