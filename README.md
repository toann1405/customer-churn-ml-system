# 📊 Customer Churn Prediction & Analytics System

[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![SQL](https://img.shields.io/badge/SQL-SQLite-orange.svg)](https://www.sqlite.org/)
[![Status](https://img.shields.io/badge/Status-In--Progress-yellow.svg)]()

---

## 📝 Project Overview

This project builds an **end-to-end churn prediction system** for a telecommunications dataset.

The goal is to help businesses **spot at-risk customers**, **understand churn drivers**, and **prioritize retention actions**.

Dataset: **Telco Customer Churn (IBM)**

- ~7,000 customers
- ~30 features
- Target variable: `Churn`

---

## 🧱 Project Roadmap (Current Progress)

This repo is organized as a phased workflow.

### ✅ Phase 1: Data Engineering & Infrastructure (Implemented)

- **Ingest raw CSV** into **SQLite** (`data/database/telco_customer_churn.db`)
- **Clean + standardize** via SQL (SQL script: `sql_scripts/transform_data.sql`)
- Output: **`cleaned_churn` table** ready for analysis

### ✅ Phase 2: Exploratory Data Analysis (Done)

- EDA captured in `notebooks/01_EDA.ipynb`
- Covers distribution analysis, churn drivers, and feature behavior

### ⏳ Phase 3: ML Engineering & Pipeline (Upcoming)

- Build preprocessing + modeling pipeline (scikit-learn / XGBoost)
- Add hyperparameter tuning, cross-validation, and robust evaluation metrics

### ⏳ Phase 4: Deployment & Delivery (Upcoming)

- Build a Streamlit app for real-time churn scoring
- Add explainability with SHAP
- Finalize documentation and deliverables

---

## 🗂 Project Structure (Current)

```
customer-churn-ml-system/
│
├── app/                    # Streamlit UI (in development)
├── data/
│   ├── raw/                # Raw CSV source data
│   └── database/           # SQLite database (output of pipeline)
│
├── docs/                   # Notes, analyses, and docs
├── models/                 # Trained model artifacts (future)
├── notebooks/              # EDA & experiments (Jupyter notebooks)
├── sql_scripts/            # SQL cleaning + transformation scripts
├── src/                    # Python orchestration scripts
│
├── requirements.txt
└── README.md
```

---

## 🛠 How to Run the Data Pipeline (Phase 1)

### 1) Setup environment

```bash
conda create -n churn_project python=3.10 -y
conda activate churn_project
pip install -r requirements.txt
```

### 2) Run ingestion + SQL cleaning

```bash
python src/database_manager.py \
  --csv data/raw/telco_customer_churn.csv \
  --db data/database/telco_customer_churn.db \
  --sql sql_scripts/transform_data.sql
```

✅ This will create (or update) the SQLite database and produce:

- `raw_customer_churn` table (raw CSV data)
- `cleaned_churn` table (cleaned / engineered output)

---

## 🔎 How to Explore (Phase 2)

Open and run the EDA notebook:

```bash
jupyter lab notebooks/01_EDA.ipynb
```

Key notebook output:

- Visual churn patterns by feature (contract, tenure, services, billing)
- Feature correlations + churn drivers
- Segmentation analysis and recommendations

---

## 🧪 What's Next (Phase 3 & 4)

- Build a **scikit-learn pipeline** (imputation, encoding, scaling, model training)
- Experiment with **XGBoost / RandomForest**
- Add **model evaluation metrics** (precision/recall/F1, ROC-AUC, PR-AUC)
- Deploy with **Streamlit + SHAP** for interpretability

---

## 📌 Notes / Tips

- The SQL transform script is intentionally in **English** for clarity and reuse.
- The notebook is intentionally **self-contained**; it reads directly from the cleaned SQLite table.

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
