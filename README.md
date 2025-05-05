# Fund the Vote: Reducing Voter Wait Times with Predict-Then-Optimize

This project, developed at Carnegie Mellon University, aims to minimize voter wait times in Allegheny County through a **predict-then-optimize pipeline**. By forecasting voter turnout using historical and demographic data, and then applying an optimization model to allocate limited resources, we provide evidence-based recommendations to improve election operations—especially in marginalized precincts.

## 📌 Problem Statement

Our goal is to reduce wait times at polling stations while prioritizing voters in historically disenfranchised areas. We use:

- **Regression models** to forecast 2026 precinct-level voter turnout.
- **Clustering** to identify precincts with marginalized populations.
- **Optimization models** to allocate check-in stations and voting booths efficiently.
- **Optiguide** to perform what-if analyses on turnout variability, resource bottlenecks, and dynamic reallocation strategies.

## 🧠 Methodology

- **Data Sources**: US Census demographic data, Allegheny County election turnout data, and GIS shapefiles.
- **Prediction Pipeline**: Hierarchical model with linear regression for demographics, followed by logistic regression for voter turnout (R² ≈ 0.75).
- **Optimization Model**: Allocates check-in and voting booths across 144 precincts to minimize total queue time across the election day.
- **Optiguide Analysis**: Evaluates the robustness of our solution under dynamic conditions and turnout uncertainties.

## ⚙️ Results

- Average wait time per voter: **~6 minutes 40 seconds**
- Priority precinct wait time: **~2 minutes 30 seconds**
- All check-in stations were fully allocated
- **Check-in stations** identified as key bottleneck
- **Doubling check-in stations** reduced total queue time by **23.5%**
- **Dynamic reallocation** helped high-flux areas at slight cost to system-wide wait time

## ▶️ Execution Guide

To run the code in this folder, make sure to first install dependencies:

```bash
pip install -r requirements.txt
```

Then execute the notebooks/scripts in the following order:

1. `demo_cleaning.ipynb` – Generates `total_demographics.csv`
2. `disability_cleaning.ipynb` – Generates `total_disability.csv`
3. `precinct_cleaning.ipynb` – Generates `relevant_precincts.geojson`
4. `location_merging.ipynb` – Generates `merged_location_data.csv`
5. `predict_turnout.ipynb` – Generates `2026_predictions.csv`
6. `prepare_data_for_opti.ipynb` – Generates `2026_full_data.csv`
7. `gurobi_opt_final.ipynb` – The optimization model
8. `optiguide_analysis.ipynb` – Optiguide what-if analysis
9. `optiguide_script.py` – Helper script used by the above notebook

---

For questions or contributions, contact:

- Ashwin Kandath – [ash.kandath@gmail.com](mailto:ash.kandath@gmail.com)
- Raj Shah – [rajshah@andrew.cmu.edu](mailto:rajshah@andrew.cmu.edu)
- Gareth Minson – [gminson@andrew.cmu.edu](mailto:gminson@andrew.cmu.edu)
