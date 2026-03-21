# 📊 Customer Churn Prediction & Analytics System

[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![SQL](https://img.shields.io/badge/SQL-SQLite-orange.svg)](https://www.sqlite.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.55-FF4B4B.svg)](https://streamlit.io/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.7-F7931E.svg)](https://scikit-learn.org/)
[![SHAP](https://img.shields.io/badge/SHAP-0.49-brightgreen.svg)](https://shap.readthedocs.io/)
[![Status](https://img.shields.io/badge/Status-Completed-success.svg)]()

---

## 📝 Project Overview

An **end-to-end churn prediction system** for a telecommunications dataset, from raw data ingestion to a deployed interactive web application.

The system helps businesses **spot at-risk customers**, **understand churn drivers**, and **prioritize retention actions** — with full model explainability via SHAP.

**Dataset:** Telco Customer Churn (IBM) · ~7,000 customers · ~30 features · Target: `Churn`

---

## 🏆 Model Results

| Model | Recall (Churn) | Precision | ROC-AUC | Notes |
|:---|:---:|:---:|:---:|:---|
| **Logistic Regression** ✅ | **0.85** | 0.49 | **0.848** | `class_weight='balanced'`, threshold=0.40 |
| Random Forest | 0.49 | 0.60 | 0.837 | `class_weight='balanced'` |
| XGBoost | 0.69 | 0.54 | 0.833 | `scale_pos_weight` |

**Key decisions:**
- Primary metric: **Recall** (minimizing missed churners is business priority)
- Class imbalance handled via `class_weight='balanced'`
- Final threshold: **0.40** (optimized for Recall vs Precision trade-off)

---

## 🧱 Project Roadmap

### ✅ Phase 1: Data Engineering & Infrastructure

- Ingest raw CSV → **SQLite** (`data/database/telco_customer_churn.db`)
- Clean + standardize via SQL (`sql_scripts/transform_data.sql`)
- Output: `cleaned_churn` table ready for analysis

### ✅ Phase 2: Exploratory Data Analysis

- EDA in `notebooks/01_EDA.ipynb`
- Churn drivers: contract type, tenure, internet service, monthly charges
- Feature correlations, distribution analysis, segmentation

### ✅ Phase 3: ML Engineering & Pipeline

- Preprocessing pipeline: `StandardScaler` + `OneHotEncoder` (via `ColumnTransformer`)
- Feature engineering: `AvgCharges = TotalCharges / tenure`
- Models: Logistic Regression, Random Forest, XGBoost
- Class imbalance: `class_weight='balanced'` + threshold optimization
- See `notebooks/02_modeling.ipynb`

### ✅ Phase 4: Deployment & Delivery

- **Streamlit app** (`app/app.py`): real-time prediction + SHAP explanation + performance dashboard
- **SHAP integration** (`LinearExplainer`): explains why each customer is predicted to churn
- Final documentation: this README

---

## 🗂 Project Structure

```
customer-churn-ml-system/
│
├── app/
│   └── app.py                   # Streamlit web application
│
├── data/
│   ├── raw/                     # Raw CSV source data
│   ├── database/                # SQLite database
│   └── processed/               # Feature-engineered test set (CSV)
│
├── models/
│   ├── churn_pipeline.pkl       # Trained sklearn Pipeline (preprocessor + LR)
│   ├── model_metadata.pkl       # Threshold, metrics, feature list
│   └── shap_background.pkl      # SHAP background dataset
│
├── notebooks/
│   ├── 01_EDA.ipynb             # Exploratory Data Analysis
│   └── 02_modeling.ipynb        # ML pipeline, training & evaluation
│
├── sql_scripts/
│   └── transform_data.sql       # SQL cleaning + transformation
│
├── src/
│   └── database_manager.py      # Data ingestion orchestrator
│
├── requirements.txt
└── README.md
```

---

## 🚀 How to Run

### 1) Setup environment

```bash
conda create -n churn_project python=3.10 -y
conda activate churn_project
pip install -r requirements.txt
```

### 2) Phase 1 — Data Pipeline

```bash
python src/database_manager.py \
  --csv data/raw/telco_customer_churn.csv \
  --db data/database/telco_customer_churn.db \
  --sql sql_scripts/transform_data.sql
```

### 3) Phase 2 & 3 — EDA & Modeling

```bash
jupyter lab notebooks/01_EDA.ipynb
jupyter lab notebooks/02_modeling.ipynb
```

> Run all cells in `02_modeling.ipynb` through **Section 15 (Model Export)** to generate the model artifacts in `models/` and processed data in `data/processed/`.

### 4) Phase 4 — Launch Streamlit App

```bash
streamlit run app/app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

**App features:**
- 🔮 **Predict tab** — enter customer info → get churn probability + SHAP explanation
- 📈 **Dashboard tab** — interactive threshold slider, confusion matrix, ROC curve, metric comparison
- ℹ️ **About tab** — model explanation, feature list, business rationale

---

## 🛠 Technologies

| Category | Stack |
|:---|:---|
| **Language** | Python 3.10, SQL |
| **ML** | scikit-learn, XGBoost, imbalanced-learn |
| **Explainability** | SHAP |
| **Web App** | Streamlit |
| **Data** | pandas, numpy |
| **Visualization** | matplotlib, seaborn |
| **Storage** | SQLite, joblib |
| **Dev Tools** | Jupyter, Git, VSCode |

---

## 👤 Contact

**Nguyen Duc Toan** — _CS Student @ HCMUT - VNUHCM_

📧 [nductoan1815@gmail.com](mailto:nductoan1815@gmail.com)
💼 [LinkedIn](https://linkedin.com/in/your-profile-link)
🐙 [@toann1405](https://github.com/toann1405)

---

⭐ **Project Status:** Completed
