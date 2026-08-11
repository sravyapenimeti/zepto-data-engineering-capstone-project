# Zepto Data Engineering Capstone Project

## Overview

This repository contains the **Zepto Data Engineering Capstone Project**, a multi-module data engineering solution designed to demonstrate an end-to-end workflow from data ingestion and analysis to an AI-powered support assistant.

The project is organized into three major modules:

1. **Module 1 — Data Pipeline**
2. **Module 2 — Analytics**
3. **Module 3 — Support Assistant**

Together, these modules demonstrate data engineering, data analysis, database management, machine learning/analytics, retrieval-augmented generation (RAG), API development, and containerization.

---

# Project Objectives

The main objectives of this capstone project are to:

* Build an automated data ingestion pipeline.
* Clean and transform raw data.
* Store structured data in a relational database.
* Perform SQL and pandas-based analysis.
* Generate business-oriented analytics and insights.
* Build a retrieval-based customer support assistant.
* Use local embeddings and vector search.
* Orchestrate the support workflow using LangGraph.
* Expose the support assistant through a FastAPI endpoint.
* Containerize the application using Docker.
* Maintain the complete project using Git and GitHub.

---

# Project Architecture

```text
                         ZEpto Data Engineering Capstone
                                      |
             +------------------------+------------------------+
             |                        |                        |
             v                        v                        v
      +-------------+          +-------------+          +----------------+
      |   Module 1  |          |   Module 2  |          |    Module 3   |
      | Data Pipeline|          |  Analytics  |          |Support Assistant|
      +------+------+          +------+------+          +-------+--------+
             |                        |                        |
             v                        v                        v
        Web Scraping            Data Analysis             Policy Corpus
             |                        |                        |
             v                        v                        v
       Data Cleaning           Business Insights          Embeddings
             |                        |                        |
             v                        v                        v
     Currency Conversion       Visualizations              ChromaDB
             |                        |                        |
             v                        v                        v
       SQLite Database         Analytics Results          LangGraph
             |                        |                        |
             v                        v                        v
       SQL + Pandas             Reports/Outputs           FastAPI
                                                              |
                                                              v
                                                           Docker
```

---

# Repository Structure

```text
zepto-data-engineering-project/
│
├── data_pipeline/
│   ├── data_pipeline.ipynb
│   ├── database/
│   ├── outputs/
│   ├── README.md
│   └── ...
│
├── analytics/
│   ├── 01_eda.ipynb
│   ├── 02_modeling.ipynb
│   ├── outputs/
│   ├── README.md
│   └── ...
│
├── support_assistant/
│   ├── docs/
│   │   ├── doc_01.txt
│   │   ├── doc_02.txt
│   │   ├── doc_03.txt
│   │   ├── doc_04.txt
│   │   ├── doc_05.txt
│   │   ├── doc_06.txt
│   │   ├── doc_07.txt
│   │   └── doc_08.txt
│   │
│   ├── chroma_db/
│   ├── create_corpus.py
│   ├── rag_pipeline.py
│   ├── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── .env.example
│   ├── .gitignore
│   └── README.md
│
└── README.md
```

---

# Module 1 — Data Pipeline

## Objective

Module 1 implements an end-to-end raw-to-relational data pipeline.

The pipeline scrapes book catalogue data from:

```text
books.toscrape.com
```

The data is cleaned, transformed, enriched with the required fixed currency conversion rate, and loaded into a normalized SQLite database.

---

## Pipeline

```text
Books to Scrape
       |
       v
Web Scraping
       |
       v
BeautifulSoup + Requests
       |
       v
Raw Product Data
       |
       v
Data Cleaning
       |
       v
Type Conversion
       |
       v
GBP → INR Conversion
       |
       v
Normalized SQLite Database
       |
       +----------------+
       |                |
       v                v
      SQL             Pandas
     Queries          Analysis
```

---

## Technologies

* Python
* Requests
* BeautifulSoup
* pandas
* SQLite
* sqlite3
* Jupyter Notebook

---

## Data Cleaning

The pipeline performs the following transformations:

### Price

The original GBP price is cleaned into:

```text
price_gbp
```

and converted to:

```text
float
```

### Rating

Text ratings such as:

```text
One
Two
Three
Four
Five
```

are converted to:

```text
1
2
3
4
5
```

### Availability

Availability text is converted into:

```text
in_stock
```

as a boolean value.

### Currency Conversion

The required fixed project baseline is:

```text
1 GBP = 105.50 INR
```

Therefore:

```text
price_inr = price_gbp × 105.50
```

This is a project-defined fixed rate and does not require an external currency API.

---

## Database

The cleaned data is stored in a normalized SQLite database.

The schema contains related tables such as:

```text
categories
    |
    | category_id
    |
    v
books
```

The database demonstrates:

* Primary keys
* Foreign keys
* Normalized relational structure
* SQL querying

---

## SQL Analysis

The module demonstrates SQL operations including:

* SELECT
* WHERE
* ORDER BY
* LIMIT
* DISTINCT
* IN
* BETWEEN
* JOIN

The results are also read back into pandas DataFrames.

---

# Module 2 — Analytics

## Objective

Module 2 focuses on analyzing the processed dataset and generating useful business insights.

The module follows an exploratory-data-analysis and modeling workflow.

---

## Analytics Pipeline

```text
Processed Dataset
       |
       v
Data Loading
       |
       v
Data Cleaning
       |
       v
Exploratory Data Analysis
       |
       v
Statistical Analysis
       |
       v
Feature Preparation
       |
       v
Modeling
       |
       v
Model Evaluation
       |
       v
Business Insights
```

---

## Main Activities

The analytics module includes:

* Dataset inspection
* Missing-value analysis
* Duplicate detection
* Data-type validation
* Descriptive statistics
* Distribution analysis
* Correlation analysis
* Outlier analysis
* Feature engineering
* Model development
* Model evaluation
* Visualization
* Business interpretation

---

## EDA

The exploratory analysis examines:

* Numerical variables
* Categorical variables
* Distributions
* Relationships between variables
* Correlations
* Potential outliers
* Data quality issues

Typical visualizations include:

* Histograms
* Box plots
* Bar charts
* Correlation heatmaps
* Other relevant analytical plots

---

## Modeling

The modeling stage prepares the data for machine-learning analysis.

The workflow includes:

```text
Feature Selection
       ↓
Data Preparation
       ↓
Train/Test Split
       ↓
Model Training
       ↓
Prediction
       ↓
Evaluation
```

Appropriate evaluation metrics are calculated based on the selected modeling task.

---

# Module 3 — Support Assistant

## Objective

Module 3 implements a small retrieval-augmented customer support assistant using the supplied Zepto policy corpus.

The required graded baseline runs locally using:

```text
MOCK_LLM=1
```

No external LLM API key is required for the graded path.

---

## RAG Architecture

```text
8 Policy Documents
        |
        v
Document Ingestion
        |
        v
all-MiniLM-L6-v2
        |
        v
Vector Embeddings
        |
        v
ChromaDB
        |
        |
    User Query
        |
        v
FastAPI /ask
        |
        v
LangGraph
        |
        v
classify_intent
        |
     +--+--+
     |     |
     v     v
 Policy  General
     |     |
     v     v
retrieve  direct
and       answer
answer
     |
     v
Top-3 Retrieval
     |
     v
Structured Response
     |
     v
Pydantic Validation
     |
     v
JSON Response
```

---

## Policy Corpus

The module contains eight policy documents:

```text
doc_01.txt
doc_02.txt
doc_03.txt
doc_04.txt
doc_05.txt
doc_06.txt
doc_07.txt
doc_08.txt
```

These documents cover areas such as:

* Delivery
* Returns and refunds
* Membership
* Order tracking
* Order cancellation
* Damaged or missing items
* Gift cards
* Customer support

---

## Embeddings

The project uses the local model:

```text
all-MiniLM-L6-v2
```

Embeddings are generated locally and stored in:

```text
ChromaDB
```

The collection is:

```text
zepto_policies
```

---

## LangGraph

The support workflow contains three required nodes:

```text
classify_intent
retrieve_and_answer
direct_answer
```

### Policy question

```text
classify_intent
       |
       v
policy_question
       |
       v
retrieve_and_answer
```

### General question

```text
classify_intent
       |
       v
general_question
       |
       v
direct_answer
```

---

## Mock Mode

The required graded mode is:

```text
MOCK_LLM=1
```

In this mode:

* No LLM API is required.
* Intent classification uses the specified keyword heuristic.
* Embeddings are generated locally.
* ChromaDB performs real retrieval.
* Policy responses use the deterministic mock generation.
* General questions use the required canned response.
* Pydantic validates the final response.

---

## API

The support assistant exposes:

```text
POST /ask
```

Example request:

```json
{
  "query": "How much is the delivery fee?"
}
```

Example response:

```json
{
  "answer": "Based on the retrieved context: ...",
  "sources": [
    "doc_01"
  ],
  "confidence": 1.0
}
```

A general question such as:

```json
{
  "query": "What is the capital of India?"
}
```

returns the non-retrieval response.

---

# Technologies Used

## Data Engineering

* Python
* Requests
* BeautifulSoup
* pandas
* SQLite
* SQL

## Analytics

* Python
* pandas
* NumPy
* Matplotlib
* Scikit-learn
* Jupyter Notebook

## AI / RAG

* LangGraph
* ChromaDB
* Sentence Transformers
* `all-MiniLM-L6-v2`
* Pydantic

## API and Deployment

* FastAPI
* Uvicorn
* Docker

## Version Control

* Git
* GitHub

---

# Installation

Clone the repository:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Move into the project:

```bash
cd zepto-data-engineering-project
```

---

# Module 1 Setup

Move into Module 1:

```bash
cd data_pipeline
```

Install the required packages listed in its README or requirements file.

Run the Jupyter notebook:

```bash
jupyter notebook
```

or open the notebook directly in VS Code.

---

# Module 2 Setup

Move into:

```bash
cd analytics
```

Open the notebooks in VS Code or Jupyter.

Run the cells sequentially from the beginning to reproduce the analysis.

---

# Module 3 Setup

Move into:

```bash
cd support_assistant
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Build the Module 3 Vector Database

Run:

```bash
python create_corpus.py
```

This:

1. Loads the eight policy documents.
2. Generates local embeddings.
3. Creates the ChromaDB collection.
4. Stores the documents and embeddings.

---

# Run the Support Assistant

Run:

```bash
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

Use the Swagger interface to test:

```text
POST /ask
```

---

# Docker

Build the Module 3 Docker image:

```bash
docker build -t zepto-support-assistant .
```

Run:

```bash
docker run --rm -p 7860:7860 zepto-support-assistant
```

Open:

```text
http://localhost:7860/docs
```

---

# Git Workflow

The project is maintained using Git feature branches.

Example:

```bash
git checkout main
git pull origin main

git checkout -b feature/module-3-support-assistant
```

Make changes and commit:

```bash
git add .
git commit -m "Add Module 3 support assistant"
```

Push:

```bash
git push -u origin feature/module-3-support-assistant
```

Create a Pull Request:

```text
feature/module-3-support-assistant
                ↓
              main
```

After review, merge the Pull Request into `main`.

---

# Project Validation Checklist

## Module 1

* [ ] Data scraping runs successfully
* [ ] At least 60 records are generated
* [ ] At least 3 categories are represented
* [ ] Data cleaning is completed
* [ ] GBP prices are converted to INR using `105.50`
* [ ] SQLite database is created
* [ ] Primary/foreign-key relationship exists
* [ ] Required SQL queries are executed
* [ ] SQL results are saved
* [ ] pandas results are generated
* [ ] SQL JOIN is reproduced with `pd.merge`

## Module 2

* [ ] Dataset loads successfully
* [ ] Data cleaning is completed
* [ ] EDA is completed
* [ ] Visualizations are generated
* [ ] Features are prepared
* [ ] Modeling is completed
* [ ] Evaluation metrics are calculated
* [ ] Results are interpreted
* [ ] Notebooks execute successfully

## Module 3

* [ ] Eight policy documents are included
* [ ] `all-MiniLM-L6-v2` embeddings are generated
* [ ] ChromaDB is created
* [ ] Top-3 retrieval works
* [ ] LangGraph `StateGraph` works
* [ ] Three required nodes are present
* [ ] Conditional routing works
* [ ] `MOCK_LLM=1` works without an API key
* [ ] Pydantic output validation works
* [ ] FastAPI `/ask` works
* [ ] Example API calls are documented
* [ ] Docker builds successfully
* [ ] Docker container runs successfully
* [ ] Architecture is documented in README

---

# Expected End-to-End Flow

The complete capstone follows:

```text
                 RAW DATA
                    |
                    v
          +-------------------+
          |    Module 1       |
          |   Data Pipeline   |
          +---------+---------+
                    |
                    v
             Cleaned Data
                    |
                    v
          +-------------------+
          |    Module 2       |
          |     Analytics     |
          +---------+---------+
                    |
                    v
           Analytical Insights
                    |
                    |
                    v
          +-------------------+
          |    Module 3       |
          | Support Assistant |
          +---------+---------+
                    |
                    v
              Policy Corpus
                    |
                    v
                ChromaDB
                    |
                    v
                LangGraph
                    |
                    v
                FastAPI
                    |
                    v
                 Docker
```

---

# Key Project Outcomes

This capstone demonstrates an end-to-end data engineering workflow combining:

* Automated data collection
* Data cleaning
* Data transformation
* Relational database design
* SQL querying
* pandas analysis
* Exploratory data analysis
* Machine learning analytics
* Vector embeddings
* Semantic retrieval
* RAG architecture
* Workflow orchestration
* Structured AI responses
* REST API development
* Docker containerization
* Git/GitHub collaboration workflow

---

# Author

**Sravya Penimeti**

B.Tech Student

---

# Conclusion

The Zepto Data Engineering Capstone Project demonstrates how raw data can be transformed into structured information, analyzed for business insights, and combined with an AI-powered support workflow.

The three modules together provide an end-to-end implementation covering:

```text
Data Engineering
      +
Analytics
      +
AI / RAG
      +
API Development
      +
Containerization
      +
Version Control
```

This repository contains the complete implementation and documentation for the capstone project.
