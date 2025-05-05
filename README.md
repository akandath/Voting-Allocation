To run the code in this folder, make sure to run `pip install -r requirements.txt`.

This code runs through the entire process of recreating our Optimziation work. 
Run the following in this order:

1. `demo_cleaning.ipynb` - Generates `total_demographics.csv`
2. `disability_cleaning.ipynb` - Generates `total_disability.csv`
3. `precinct_cleaning.ipynb` - Generates `relevant_precincts.geojson`
4. `location_merging.ipynb` - Generates `merged_location_data.csv`
5. `predict_turnout.ipynb` - Generates `2026_predictions.csv`
6. `prepare_data_for_opti.ipynb` - Generates `2026_full_data.csv`
7. `gurobi_opt_final.ipynb` - The Optimization Work
8. `optiguide_analysis.ipynb` - Optiguide Analysis
9. `optiguide_script.py` - Python script that `optiguide_analysis.ipynb` refers to
