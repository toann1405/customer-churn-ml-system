# 📊 Customer Churn Prediction & Analytics System

[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![SQL](https://img.shields.io/badge/SQL-SQLite-orange.svg)](https://www.sqlite.org/)
[![Status](https://img.shields.io/badge/Status-In--Progress-yellow.svg)]()

---

## 📝 Project Overview

This project builds an **end-to-end machine learning system** to predict **customer churn** for a telecommunications company.

The goal is to help businesses **identify customers at risk of leaving** and enable **data-driven retention strategies**.

Dataset: **Telco Customer Churn**

- 7,043 customers
- 33 features
- Target variable: `Churn`

---

## 🎯 Business Goals

- Identify **key factors driving churn**
- Predict **customers likely to leave**
- Segment customers for **retention strategies**
- Build a **deployable ML pipeline**

---

## ⚙️ ML Pipeline Architecture

```

Raw Dataset
↓
Data Ingestion (Python)
↓
SQL Data Cleaning
↓
Feature Engineering
↓
Data Validation
↓
Processed Dataset
↓
EDA
↓
Machine Learning Model
↓
Deployment (Dashboard)

```

---

## 🗂 Project Structure

```

customer-churn-ml/
│
├── app/                # Streamlit dashboard (future)
├── data/
│   ├── raw/
│   └── processed/
│
├── database/           # SQLite database
├── docs/               # Documentation
├── models/             # Trained models
├── notebooks/          # EDA & experiments
├── sql/                # SQL cleaning & feature engineering
├── src/                # Python pipeline scripts
│
├── requirements.txt
└── README.md

```

---

## 🔧 Data Engineering Pipeline (Completed)

The current pipeline processes raw data into a **model-ready dataset**.

---

### 🛠 Setup Environment

```bash
# Create virtual environment
conda create -n churn_project python=3.10

# Activate environment
conda activate churn_project

# Install dependencies
pip install -r requirements.txt

```

### Run Data Pipeline

```
python src/run_pipeline.py
```

---

## 🚀 Project Progress

| Phase   | Description                | Status                                   |
| ------- | -------------------------- | ---------------------------------------- |
| Phase 1 | Project Setup              | ✅ Completed                             |
| Phase 2 | Data Engineering Pipeline  | ✅ Completed                             |
| Phase 3 | Exploratory Data Analysis  | ✅ Completed (EDA insights consolidated) |
| Phase 4 | Machine Learning Modeling  | ⏳ Upcoming                              |
| Phase 5 | Model Evaluation           | ⏳ Upcoming                              |
| Phase 6 | Deployment (Dashboard/API) | ⏳ Upcoming                              |

> **Note:** EDA is now complete, with redundant analyses removed and insights consolidated into a single, clean narrative.

---

## 🛠 Technologies

**Languages**

- Python
- SQL

**Libraries**

- pandas
- numpy
- scikit-learn
- matplotlib
- seaborn

**Tools**

- SQLite
- Jupyter Notebook
- Git
- VSCode

---

## 👤 Contact

**Nguyen Duc Toan** - _Computer Science Student @ Ho Chi Minh City University of Technology (HCMUT) - VNUHCM_

📧 **Email:** [nductoan1815@gmail.com](mailto:nductoan1815@gmail.com)  
💼 **LinkedIn:** [Updating](https://linkedin.com/in/your-profile-link)  
🐙 **GitHub:** [@toann1405](https://github.com/toann1405)

---

⭐ **Project Status:** In Development  
Latest milestone: **Exploratory Data Analysis Completed**
