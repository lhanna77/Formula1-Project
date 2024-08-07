#!/bin/bash

echo Load started - $(date)!

# Run plan
source plan.sh

# Get latest Results from API
py -3.10 get_latest_data_from_api_inc.py

# Populate silver results.csv
jupyter nbconvert --execute --to notebook --inplace 9.ingest_results_file_api_mulit_inc.ipynb

# Populate GCP BigQuery silver tables
py -3.10 bq_silver_gold_loads_api.py

echo Load finished - $(date)!