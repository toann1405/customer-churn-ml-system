import streamlit as st
import pandas as pd
import numpy as np
import joblib
import shap
import matplotlib.pyplot as plt
import matplotlib
from sklearn.metrics import (
    confusion_matrix, roc_curve, auc,
    classification_report, precision_score, recall_score, f1_score
)
import seaborn as sns
import os

matplotlib.use("Agg")

# ─────────────────────────────────────────────
# Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Churn Prediction Dashboard",
    page_icon="📊",
    layout="wide",
)

MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
DATA_DIR   = os.path.join(os.path.dirname(__file__), "..", "data", "processed")

OPTIMAL_THRESHOLD = 0.40

# ─────────────────────────────────────────────
# Load artifacts (cached)
# ─────────────────────────────────────────────
@st.cache_resource
def load_pipeline():
    return joblib.load(os.path.join(MODELS_DIR, "churn_pipeline.pkl"))

@st.cache_resource
def load_metadata():
    return joblib.load(os.path.join(MODELS_DIR, "model_metadata.pkl"))

@st.cache_data
def load_test_data():
    path = os.path.join(DATA_DIR, "processed_test_data.csv")
    df = pd.read_csv(path)
    return df

@st.cache_resource
def load_shap_explainer(_pipeline, _X_bg):
    preprocessor = _pipeline.named_steps["preprocessor"]
    classifier   = _pipeline.named_steps["classifier"]

    # Get all feature names after transformation
    cat_encoder    = preprocessor.named_transformers_["cat"].named_steps["onehot"]
    cat_names      = list(cat_encoder.get_feature_names_out(CATEGORICAL_FEATURES))
    all_feat_names = NUMERIC_FEATURES + cat_names

    # Transform background → DataFrame (avoids feature_names_in_ mismatch in sklearn 1.7+)
    X_bg_arr   = np.array(preprocessor.transform(_X_bg))
    background = shap.sample(X_bg_arr, min(100, len(_X_bg)))

    return shap.LinearExplainer(classifier, background), all_feat_names

# ─────────────────────────────────────────────
# Feature metadata (must match notebook)
# ─────────────────────────────────────────────
NUMERIC_FEATURES     = ["tenure", "MonthlyCharges", "TotalCharges", "AvgCharges"]
CATEGORICAL_FEATURES = [
    "gender", "SeniorCitizen", "Partner", "Dependents",
    "PhoneService", "MultipleLines", "InternetService",
    "OnlineSecurity", "OnlineBackup", "DeviceProtection",
    "TechSupport", "StreamingTV", "StreamingMovies",
    "Contract", "PaperlessBilling", "PaymentMethod",
]

# ─────────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────────
st.sidebar.title("📊 Churn Prediction")
st.sidebar.caption("Telco Customer Churn · Logistic Regression")
threshold = st.sidebar.slider(
    "Decision Threshold",
    min_value=0.10, max_value=0.90,
    value=OPTIMAL_THRESHOLD, step=0.01,
    help="Lower → higher Recall (catch more churners). Higher → higher Precision (fewer false alarms)."
)
tab_predict, tab_dashboard, tab_about = st.tabs(
    ["🔮 Predict", "📈 Dashboard", "ℹ️ About"]
)

# ═════════════════════════════════════════════
# TAB 1 — PREDICT
# ═════════════════════════════════════════════
with tab_predict:
    st.header("Customer Churn Prediction System")
    st.caption("Enter customer information to get a real-time churn prediction with explanation.")

    pipeline = load_pipeline()
    meta     = load_metadata()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Contract & Billing")
        contract        = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
        payment_method  = st.selectbox("Payment Method", [
            "Electronic check", "Mailed check",
            "Bank transfer (automatic)", "Credit card (automatic)"
        ])
        paperless       = st.selectbox("Paperless Billing", ["Yes", "No"])
        monthly_charges = st.slider("Monthly Charges ($)", 10.0, 120.0, 65.0, 0.5)
        tenure          = st.slider("Tenure (months)", 1, 72, 12)

    with col2:
        st.subheader("Internet Services")
        internet_service   = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])
        online_security    = st.selectbox("Online Security",  ["Yes", "No", "No internet service"])
        online_backup      = st.selectbox("Online Backup",    ["Yes", "No", "No internet service"])
        device_protection  = st.selectbox("Device Protection",["Yes", "No", "No internet service"])
        tech_support       = st.selectbox("Tech Support",     ["Yes", "No", "No internet service"])
        streaming_tv       = st.selectbox("Streaming TV",     ["Yes", "No", "No internet service"])
        streaming_movies   = st.selectbox("Streaming Movies", ["Yes", "No", "No internet service"])

    with col3:
        st.subheader("Demographics & Phone")
        gender         = st.selectbox("Gender",         ["Male", "Female"])
        senior_citizen = st.selectbox("Senior Citizen", ["No", "Yes"])
        partner        = st.selectbox("Partner",        ["Yes", "No"])
        dependents     = st.selectbox("Dependents",     ["Yes", "No"])
        phone_service  = st.selectbox("Phone Service",  ["Yes", "No"])
        multiple_lines = st.selectbox("Multiple Lines", ["Yes", "No", "No phone service"])

    # ── Build input dataframe ──────────────────
    total_charges = monthly_charges * tenure
    avg_charges   = monthly_charges if tenure == 0 else total_charges / tenure

    input_data = pd.DataFrame([{
        "tenure":           tenure,
        "MonthlyCharges":   monthly_charges,
        "TotalCharges":     total_charges,
        "AvgCharges":       avg_charges,
        "gender":           gender,
        "SeniorCitizen":    "Yes" if senior_citizen == "Yes" else "No",
        "Partner":          partner,
        "Dependents":       dependents,
        "PhoneService":     phone_service,
        "MultipleLines":    multiple_lines,
        "InternetService":  internet_service,
        "OnlineSecurity":   online_security,
        "OnlineBackup":     online_backup,
        "DeviceProtection": device_protection,
        "TechSupport":      tech_support,
        "StreamingTV":      streaming_tv,
        "StreamingMovies":  streaming_movies,
        "Contract":         contract,
        "PaperlessBilling": paperless,
        "PaymentMethod":    payment_method,
    }])

    st.divider()
    if st.button("🔮 Predict Churn", use_container_width=True, type="primary"):
        proba = pipeline.predict_proba(input_data)[0][1]
        churn = proba >= threshold

        # ── Prediction result ──────────────────
        res_col1, res_col2, res_col3 = st.columns(3)
        with res_col1:
            st.metric("Churn Probability", f"{proba:.1%}")
        with res_col2:
            st.metric("Threshold Used", f"{threshold:.2f}")
        with res_col3:
            if churn:
                st.error("⚠️ HIGH RISK — Likely to Churn")
            else:
                st.success("✅ LOW RISK — Likely to Stay")

        # ── SHAP explanation ───────────────────
        st.subheader("Why this prediction? (SHAP Feature Impact)")
        st.info("🚧 SHAP explanation is temporarily disabled — will be fixed in the next update.")
        # TODO: Fix SHAP LinearExplainer compatibility with sklearn 1.7+ (feature_names_in_ issue)
        # try:
        #     test_df  = load_test_data()
        #     X_bg     = test_df.drop(columns=["Churn"])
        #     explainer, all_feat_names = load_shap_explainer(pipeline, X_bg)
        #
        #     preprocessor = pipeline.named_steps["preprocessor"]
        #     X_input_arr  = np.array(preprocessor.transform(input_data))
        #
        #     shap_vals_raw = explainer.shap_values(X_input_arr)
        #     expected_val  = explainer.expected_value
        #
        #     if isinstance(shap_vals_raw, list):
        #         sv = shap_vals_raw[1][0]
        #         ev = expected_val[1] if hasattr(expected_val, "__len__") else expected_val
        #     else:
        #         sv = shap_vals_raw[0]
        #         ev = float(expected_val)
        #
        #     shap.plots.waterfall(
        #         shap.Explanation(
        #             values       = sv,
        #             base_values  = ev,
        #             data         = X_input_arr[0],
        #             feature_names= all_feat_names,
        #         ),
        #         max_display=12,
        #         show=False,
        #     )
        #     st.pyplot(plt.gcf(), use_container_width=True)
        #     plt.close()
        # except Exception as e:
        #     st.warning(f"SHAP explanation unavailable: {e}")


# ═════════════════════════════════════════════
# TAB 2 — DASHBOARD
# ═════════════════════════════════════════════
with tab_dashboard:
    st.header("Model Performance Dashboard")

    try:
        pipeline = load_pipeline()
        meta     = load_metadata()
        test_df  = load_test_data()

        X_test_raw = test_df.drop(columns=["Churn"])
        y_test     = test_df["Churn"]

        y_proba = pipeline.predict_proba(X_test_raw)[:, 1]
        y_pred_opt     = (y_proba >= threshold).astype(int)
        y_pred_default = (y_proba >= 0.50).astype(int)

        # ── KPI cards ─────────────────────────
        st.subheader("Key Metrics at Selected Threshold")
        k1, k2, k3, k4, k5 = st.columns(5)
        k1.metric("Threshold",  f"{threshold:.2f}", delta=f"{threshold - 0.50:+.2f} vs default")
        k2.metric("Recall",     f"{recall_score(y_test, y_pred_opt):.3f}")
        k3.metric("Precision",  f"{precision_score(y_test, y_pred_opt):.3f}")
        k4.metric("F1-Score",   f"{f1_score(y_test, y_pred_opt):.3f}")
        k5.metric("ROC-AUC",    f"{meta['roc_auc']:.3f}")

        st.divider()

        col_a, col_b = st.columns(2)

        # ── Confusion Matrix ───────────────────
        with col_a:
            st.subheader(f"Confusion Matrix (threshold = {threshold:.2f})")
            cm  = confusion_matrix(y_test, y_pred_opt)
            fig_cm, ax_cm = plt.subplots(figsize=(5, 4))
            sns.heatmap(
                cm, annot=True, fmt="d", cmap="Blues", ax=ax_cm,
                xticklabels=["Stay", "Churn"],
                yticklabels=["Stay", "Churn"],
            )
            ax_cm.set_xlabel("Predicted"); ax_cm.set_ylabel("Actual")
            tn, fp, fn, tp = cm.ravel()
            ax_cm.set_title(f"TP={tp}  FP={fp}  FN={fn}  TN={tn}")
            st.pyplot(fig_cm, use_container_width=True)
            plt.close()

        # ── ROC Curve ─────────────────────────
        with col_b:
            st.subheader("ROC Curve")
            fpr, tpr, thresholds_roc = roc_curve(y_test, y_proba)
            auc_score = auc(fpr, tpr)

            fig_roc, ax_roc = plt.subplots(figsize=(5, 4))
            ax_roc.plot(fpr, tpr, color="#2196F3", lw=2,
                        label=f"Logistic Regression (AUC = {auc_score:.3f})")
            ax_roc.plot([0, 1], [0, 1], linestyle="--", color="gray")
            ax_roc.set_xlabel("False Positive Rate")
            ax_roc.set_ylabel("True Positive Rate")
            ax_roc.legend(loc="lower right")
            ax_roc.grid(True, alpha=0.3)
            st.pyplot(fig_roc, use_container_width=True)
            plt.close()

        st.divider()

        # ── Threshold comparison table ─────────
        st.subheader("Threshold Comparison")
        rows = []
        for thr in [0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60]:
            y_p = (y_proba >= thr).astype(int)
            rows.append({
                "Threshold": thr,
                "Recall":    round(float(recall_score(y_test, y_p)), 3),
                "Precision": round(float(precision_score(y_test, y_p)), 3),
                "F1":        round(float(f1_score(y_test, y_p)), 3),
                "FN (Missed)": int(((y_test == 1) & (y_p == 0)).sum()),
            })
        comparison_df = pd.DataFrame(rows)
        # Highlight optimal threshold row
        def highlight_optimal(row):
            color = "background-color: #1a3a5c; color: white" if row["Threshold"] == threshold else ""
            return [color] * len(row)
        st.dataframe(
            comparison_df.style.apply(highlight_optimal, axis=1),
            use_container_width=True, hide_index=True
        )

        # ── Classification report ──────────────
        with st.expander("📋 Full Classification Report"):
            report_default = classification_report(y_test, y_pred_default, output_dict=True)
            report_opt     = classification_report(y_test, y_pred_opt,     output_dict=True)
            rc1, rc2 = st.columns(2)
            with rc1:
                st.caption("Default threshold (0.50)")
                st.dataframe(pd.DataFrame(report_default).T.round(3))
            with rc2:
                st.caption(f"Optimized threshold ({threshold:.2f})")
                st.dataframe(pd.DataFrame(report_opt).T.round(3))

    except FileNotFoundError:
        st.warning("⚠️ Processed test data not found. Please run Section 15 of the notebook first to export model artifacts.")


# ═════════════════════════════════════════════
# TAB 3 — ABOUT
# ═════════════════════════════════════════════
with tab_about:
    st.header("About the Model")

    try:
        meta = load_metadata()
        st.subheader("Model Configuration")
        cfg_col1, cfg_col2 = st.columns(2)
        with cfg_col1:
            st.markdown(f"""
| Parameter | Value |
|:---|:---|
| **Algorithm** | Logistic Regression |
| **Class Weight** | `balanced` |
| **Optimal Threshold** | `{meta['optimal_threshold']}` |
| **Training Date** | {meta['training_date']} |
""")
        with cfg_col2:
            st.markdown(f"""
| Metric | Value |
|:---|:---|
| **ROC-AUC** | {meta['roc_auc']} |
| **Recall @ optimal threshold** | {meta['recall_at_threshold']} |
| **Features used** | {len(meta['feature_columns'])} |
""")
    except FileNotFoundError:
        st.info("Model metadata not found. Please export from notebook.")

    st.divider()
    st.subheader("Why Logistic Regression?")
    st.markdown("""
- **Highest Recall** among all tested models after applying `class_weight='balanced'`
- **Highest ROC-AUC (0.848)** — best discriminative power
- **Simplest to deploy** — lightest model file, fastest inference, no extra dependencies
- **Interpretable** — SHAP `LinearExplainer` gives fast, exact explanations

The relationships between features and churn in this dataset are **largely linear**,
making Logistic Regression an ideal choice over more complex tree-based models.
""")

    st.divider()
    st.subheader("Why Recall as Primary Metric?")
    st.markdown("""
| Error Type | Business Impact |
|:---|:---|
| **False Negative** (miss a churner) | 🔴 Customer leaves → lost Monthly Revenue forever |
| **False Positive** (flag a loyal customer) | 🟡 Unnecessary retention offer → small cost |

Minimizing **False Negatives** (maximizing Recall) is the business priority.
A lower threshold trades some Precision for higher Recall — acceptable for this use case.
""")

    st.divider()
    st.subheader("Features Used")
    col_n, col_c = st.columns(2)
    with col_n:
        st.caption("Numeric Features")
        for f in NUMERIC_FEATURES:
            st.markdown(f"- `{f}`")
    with col_c:
        st.caption("Categorical Features")
        for f in CATEGORICAL_FEATURES:
            st.markdown(f"- `{f}`")

    st.divider()
    st.caption("Built with Streamlit · scikit-learn · SHAP · Telco Customer Churn dataset (IBM)")
