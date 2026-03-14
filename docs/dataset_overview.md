# Telco Customer Churn Dataset Overview

## 1. Project Overview

**Dataset:** Telco Customer Churn (IBM Sample Dataset)

This dataset contains customer information from a telecommunications company and is commonly used for churn prediction tasks.

Project goals:

* Predict whether a customer will churn.
* Identify the main factors that influence churn behavior.
* Segment customers based on value and service usage.

Dataset size:

* **7043 observations**
* **33 variables**

---

# 2. Data Categorization

The dataset variables can be grouped into several logical categories.

| Category            | Description                         | Example Features                           |
| ------------------- | ----------------------------------- | ------------------------------------------ |
| Demographics        | Basic customer information          | Gender, SeniorCitizen, Partner, Dependents |
| Services            | Services subscribed by the customer | PhoneService, InternetService, TechSupport |
| Account Information | Billing and contract details        | TenureMonths, Contract, PaymentMethod      |
| Target & Scores     | Churn related indicators            | ChurnValue, ChurnScore, CLTV               |

---

# 3. High Impact Features

Some variables play a significant role in churn prediction and require special handling.

---

## Target Variable

**Churn Value**

| Value | Meaning          |
| ----- | ---------------- |
| 1     | Customer churned |
| 0     | Customer stayed  |

This is the **main target variable** used for machine learning models.

---

## Numerical Features

### Tenure Months

Total number of months the customer has stayed with the company.

Customers with longer tenure typically have **lower churn probability**.

### Monthly Charge

Monthly payment amount for all subscribed services.

This variable helps analyze **customer price sensitivity**.

### Total Charges

This column requires special handling.

Issue:

Some rows contain blank values when customers have **Tenure = 0**.

Processing strategy:

* Convert to **FLOAT**
* Handle missing values via imputation (fill with 0)

---

## Categorical Features

### Contract

Contract type:

* Month-to-Month
* One Year
* Two Year

This feature typically has the **strongest correlation with churn**.

Customers on **month-to-month contracts** usually have higher churn risk.

---

### Internet Service

Types:

* DSL
* Fiber Optic
* Cable
* None

Special attention should be paid to **Fiber Optic customers**, which often show unusually high churn rates.

---

# 4. Data Processing Strategy

## Data Cleaning

Data preprocessing will include:

* Fix incorrect data types
* Handle missing values
* Normalize categorical variables

Examples:

* Convert `TotalCharges` to numeric
* Replace Yes/No with binary values (1/0)

---

## Feature Selection

The following variables will be removed during modeling:

* CustomerID
* Count
* Country
* State

Reason:

* Unique identifiers
* Low predictive value
* High cardinality

---

# 5. Customer Segmentation Strategy (Planned)

In addition to churn prediction, the project may include **customer segmentation** using clustering methods.

Segmentation will be based on three dimensions:

### Customer Loyalty

Measured by:

* Tenure Months

### Economic Value

Measured by:

* Monthly Charges
* CLTV

### Service Engagement

Measured by:

* Number of additional services subscribed

Potential algorithm:

* K-Means Clustering

---

# 6. Metadata Notes

### Geographic Data

The dataset includes geographic variables such as:

* Latitude
* Longitude
* Zip Code

These features could support **regional churn analysis** if spatial analysis is explored later.

---

### Data Privacy

The dataset is fully **anonymized**.

Customer identifiers are synthetic and do not correspond to real individuals.
