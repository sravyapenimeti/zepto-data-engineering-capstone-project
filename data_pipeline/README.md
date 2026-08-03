# Module 1 – Data Pipeline

## Project Overview

This project implements an end-to-end data engineering pipeline.

### Steps Performed

- Scraped book data from Books to Scrape
- Cleaned and transformed the data
- Converted GBP prices to INR
- Created a normalized SQLite database
- Executed SQL queries
- Loaded SQL results into pandas
- Compared SQL JOIN with pandas merge

## Data Source

https://books.toscrape.com/

## Technologies Used

- Python
- Requests
- BeautifulSoup
- Pandas
- SQLite

## Fixed Currency Conversion

1 GBP = 105.50 INR

## Database Schema

### categories

- category_id (Primary Key)
- category_name

### books

- book_id (Primary Key)
- title
- price_gbp
- price_inr
- rating
- in_stock
- category_id (Foreign Key)

## How to Run

1. Install dependencies:
   ```
   pip install requests beautifulsoup4 pandas
   ```

2. Open `data_pipeline.ipynb`.

3. Run all notebook cells from top to bottom.

## Outputs

- books.db
- data/raw_books.csv
- data/cleaned_books.csv
- outputs/query_1.csv
- outputs/query_2.csv
- outputs/query_3.csv
- outputs/query_4.csv
- outputs/query_5.csv
- outputs/query_6_join.csv
- outputs/join_comparison.csv
- outputs/sql_queries.txt

## Cleaning Decisions

- Converted price to float.
- Converted star ratings from text to integers.
- Converted availability to Boolean.
- Used median imputation for numeric parsing failures.
- Dropped rows with missing title or category.