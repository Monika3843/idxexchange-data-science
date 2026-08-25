# California Single-Family Home Price Predictor

An automated valuation model (AVM) that predicts the sale price of California 
single-family residential properties, built during a 9-week data science 
internship project.

---

## 1. Dataset Source

- **Source:** CRMLS (California Regional MLS) sold-property data, downloaded 
  via FTP from `/raw/California`.
- **Coverage:** January 2022 - June 2026 (~818,000 raw listings across all 
  property types).
- **Scope:** Restricted to `PropertyType = Residential` and 
  `PropertySubType = SingleFamilyResidence`, per the project's defined scope 
  (~412,000 rows after filtering).
- **Target variable:** `ClosePrice`.
- **Feature reference:** Column definitions were reviewed against the Trestle 
  Property MetaData documentation provided at project start.

---

## 2. Preprocessing

- **Duplicates:** Removed duplicate listings, matched on `ListingKey`.
- **Missing values:** Rows missing critical fields (ClosePrice, Bedrooms, 
  LivingArea, Latitude/Longitude) were dropped, since these can't be 
  reasonably estimated. Less-critical missing values (LotSizeAcres, 
  YearBuilt, BathroomsTotalInteger) were imputed with median values, with a 
  corresponding `_missing` flag column added for each so the model can 
  distinguish real values from imputed ones.
- **Outliers:** Extreme ClosePrice outliers (e.g. a $1 sale, a $989M sale) 
  were capped at an IQR-based upper bound rather than dropped, preserving 
  data while limiting distortion.
- **Feature engineering (initial):** `PropertyAge` (calculated relative to 
  each property's actual sale date, not today's date, to avoid inflating the 
  age of older sales) and a `DaysOnMarket` anomaly flag for negative values.
- **Leakage prevention:** `ListPrice` and `OriginalListPrice` were 
  deliberately excluded from all model features. These are highly correlated 
  with ClosePrice and unavailable for off-market properties, so including 
  them would have caused target leakage and limited the model's real-world 
  use case.
- **Train/test split:** The most recent available month (June 2026) is held 
  out as the test set; the preceding N months are used for training. Window 
  length (N) was treated as a tunable parameter and tested across 3, 6, 9, 
  12, 18, and 24-month options — a **3-month window** performed best.

---

## 3. Feature Engineering (Advanced)

- **BedBathRatio:** bedrooms divided by bathrooms.
- **SchoolDistrict:** each property's coordinates were spatially joined 
  against CA Unified School District boundaries (2025-26 dataset from 
  data.ca.gov) to determine which district contains it. The result was added 
  as a categorical feature (one-hot encoded, 322 categories). ~75% of 
  properties matched to a Unified district; the remainder were labeled 
  `No_Unified_District` (served by separate elementary/high-school district 
  systems instead).

---

## 4. Models Tested

| Model               | Test R² | MAPE  | MdAPE |
|----------------------|---------|-------|-------|
| Linear Regression     | 0.649   | 34.5% | 22.2% |
| Decision Tree          | 0.774   | 22.4% | 14.9% |
| Random Forest          | 0.876   | 15.1% | 9.5%  |
| **XGBoost (best)**     | **0.892** | 15.4% | 10.2% |

All models were evaluated on the same 3-month training window and June 2026 
test month, using the full engineered feature set, for a fair comparison.

**Note:** while XGBoost achieved the best R², Random Forest had marginally 
better MAPE/MdAPE — XGBoost explains more overall price variance (likely 
performing better on harder, higher-end properties), while Random Forest is 
marginally more consistent for a "typical" home. Both are strong, defensible 
choices.

### Price Band Performance (XGBoost)

| Price Band     | MAPE  | MdAPE |
|----------------|-------|-------|
| Under $500k    | 25.6% | 13.7% |
| $500k - $1M    | 13.3% | 8.8%  |
| $1M - $2M      | 14.2% | 10.8% |
| Over $2M       | 13.8% | 11.2% |

The model performs meaningfully worse on sub-$500k properties — roughly 
double the error of every other band. Likely causes: lower price variance 
amplifies percentage error, fewer training examples in this segment, and 
low-end pricing being influenced by factors (condition, distressed sales) not 
captured in this dataset.

---

## 5. Best Result

**XGBoost**, trained on a 3-month rolling window with engineered features 
(BedBathRatio + SchoolDistrict), is the final production model:
- **Test R²: 0.892**
- **Test MAPE: 15.4%**
- **Test MdAPE: 10.2%**

Predictions for properties under $500k should be treated as lower-confidence 
given the higher error rate observed in that price band.

---

## 6. Repository Structure
IDX Exchange_DS/
├── notebooks/
│ ├── 01_exploration.ipynb
│ ├── 02_preprocessing.ipynb
│ ├── 03_baseline_model.ipynb
│ ├── 04_model_comparison.ipynb
│ ├── 05_feature_engineering.ipynb
│ ├── 06_advanced_models.ipynb
│ └── 07_evaluation.ipynb
├── outputs/
│ ├── cleaned_full.csv
│ ├── metrics_summary.csv
│ └── xgb_model_package.pkl
├── scripts/
│ └── [CA School District GeoJSON]
├── app.py
└── README.md


---

## 7. How to Re-run the Analysis

1. Install dependencies:
```bash
   pip install pandas numpy scikit-learn xgboost geopandas streamlit joblib
```
2. Download at least 6 months of CRMLS sold data (CSV) into `data/california/`.
3. Download the CA School District Areas GeoJSON from 
   [data.ca.gov](https://data.ca.gov/dataset/california-school-district-areas-2025-26) 
   into `scripts/`.
4. Run the notebooks in order (01 through 07) — each one builds on outputs 
   from the previous, ending with a trained XGBoost model and 
   `metrics_summary.csv` saved to `outputs/`.

---

## 8. How to Launch the Prediction App

1. Ensure `outputs/xgb_model_package.pkl` exists (generated at the end of 
   `06_advanced_models.ipynb`).
2. From the project root, run:
```bash
   python -m streamlit run app.py
```
3. A browser tab opens automatically. Enter Living Area, Bedrooms, 
   Bathrooms, and Lot Size to receive an estimated sale price.

   **Note:** the app only exposes 4 input fields per its intended scope. All 
   other features (location, school district, property age, etc.) are filled 
   with dataset-wide median values behind the scenes, so predictions are most 
   accurate for a "typical" property and should be treated as a general 
   estimate rather than a precise valuation.

---

## Summary

Starting from a Linear Regression baseline (R² = 0.649), performance improved 
steadily through Decision Tree, Random Forest, and finally XGBoost 
(R² = 0.892) — the final production model. Engineered features (bed/bath 
ratio, school district) provided the largest benefit to the simplest model 
(Linear Regression, +0.171 R²), with more modest gains for tree-based models, 
which could already infer geographic patterns directly from coordinates.