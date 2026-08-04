# Module 2 – Analytics and Machine Learning

## Project Overview

This module performs exploratory data analysis, preprocessing, machine learning, and regression using the Titanic dataset.

## Dataset

Titanic Dataset loaded once using:

```python
sns.load_dataset("titanic")
```

The dataset was saved locally as:

```
titanic.csv
```

## Steps Performed

- Data profiling
- Missing value analysis
- Data cleaning
- Exploratory Data Analysis
- Correlation analysis
- Outlier detection
- Feature scaling
- Logistic Regression
- Decision Tree
- Random Forest
- SMOTE
- GridSearchCV
- OOB Score
- Linear Regression
- Residual Analysis
- Pipeline serialization using Joblib

## Folder Structure

```
analytics/
│
├── 01_eda.ipynb
├── 02_modeling.ipynb
├── titanic.csv
├── best_pipeline.joblib
├── charts/
├── outputs/
└── README.md
```

## Technologies

- Python
- Pandas
- NumPy
- Seaborn
- Matplotlib
- Scikit-learn
- imbalanced-learn
- Joblib

## How to Run

1. Install required packages.
2. Run `01_eda.ipynb`.
3. Run `02_modeling.ipynb`.
3. Review generated charts and outputs.

## Outputs

- Cleaned dataset
- Scaled dataset
- Classification comparison
- Final model summary
- Saved ML pipeline
