# California Property Close Price Prediction
**IDX Exchange — Data Science Internship**
**Intern:** Monika | **Data Source:** CRMLS (California Regional Multiple Listing Service)

---

## Project Overview

This project builds a machine learning model to predict the **close price (final sale price)** of residential properties in California using historical MLS data from CRMLS. The goal is to accurately estimate what a single-family home will sell for based on its characteristics — similar to how Zillow's Zestimate works, but built from the ground up.

---

## Objectives

- Explore and clean CRMLS sold property data
- Engineer meaningful features that influence home prices
- Train and compare multiple ML models (Linear Regression, Random Forest, XGBoost, etc.)
- Evaluate model performance using R², MAPE, and MdAPE
- (Optional) Deploy a simple prediction app using Streamlit

---

## Dataset

- **Source:** CRMLS via IDX Exchange FTP server (`/raw/California` — `CRMLSSold` files)
- **Filter:** `PropertyType = Residential` and `PropertySubType = SingleFamilyResidence`
- **Target Variable:** `ClosePrice` — the final agreed sale price of a property
- **Note:** Raw CSV files are not included in this repository per project guidelines

---

## Repository Structure

```
├── notebooks/
│   ├── 01_exploration.ipynb          # EDA and data distributions
│   ├── 02_preprocessing.ipynb        # Cleaning, encoding, train/test split
│   ├── 03_baseline_model.ipynb       # Linear Regression baseline
│   ├── 04_model_comparison.ipynb     # Decision Tree and Random Forest
│   ├── 05_advanced_models.ipynb      # XGBoost / LightGBM
│   └── 06_evaluation.ipynb           # Full metrics summary
├── scripts/
│   ├── preprocessing.py              # Data cleaning pipeline
│   ├── train.py                      # Model training
│   ├── evaluate.py                   # Model evaluation
│   └── predict.py                    # Prediction on new inputs
├── outputs/
│   └── metrics_summary.csv           # Model performance comparison
├── app.py                            # (Optional) Streamlit prediction app
└── README.md
```

---

## How to Run

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/california-price-prediction.git
cd california-price-prediction
```

### 2. Install dependencies
```bash
pip install pandas numpy scikit-learn xgboost lightgbm matplotlib seaborn jupyter streamlit
```

### 3. Add your data
- Download `CRMLSSold` CSV files from the IDX Exchange FTP server
- Place them in a local `/data` folder (not tracked by Git)

### 4. Run notebooks in order
Open Jupyter and run notebooks `01` through `06` sequentially.

### 5. (Optional) Launch the Streamlit app
```bash
streamlit run app.py
```
Enter property details (living area, beds, baths, lot size) to get a predicted close price.

---

## Models Tested

| Model | Description |
|---|---|
| Linear Regression | Baseline — simple and interpretable |
| Decision Tree | Captures non-linear relationships |
| Random Forest | Ensemble of trees — reduces overfitting |
| XGBoost / LightGBM | Gradient boosting — highest accuracy |

---

## Evaluation Metrics

- **R²** — how well the model explains price variance (primary metric)
- **MAPE** — Mean Absolute Percentage Error
- **MdAPE** — Median Absolute Percentage Error (robust to outliers)

---

## 12-Week Timeline

| Week | Focus |
|---|---|
| 1 | Setup, FTP access, dataset review |
| 2 | Exploratory Data Analysis |
| 3 | Data Preprocessing |
| 4 | Baseline Model (Linear Regression) |
| 5 | Additional Models (Decision Tree, Random Forest) |
| 6 | Feature Engineering (school districts, bed/bath ratio) |
| 7 | Advanced Models (XGBoost / LightGBM) |
| 8 | Evaluation Expansion |
| 9 | (Optional) Streamlit App |
| 10 | Documentation |
| 11 | Practice Presentation |
| 12 | Final Zoom Presentation & Repo Handoff |

---

## Acknowledgements

Data provided by IDX Exchange via CRMLS. Project completed as part of the IDX Exchange Data Science Internship Program.
