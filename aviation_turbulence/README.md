# Data Curation for Turbulence Detection Based on Pilot Reports

This repository contains code and instructions for processing turbulence data from pilot reports (PIREPs) and preparing it for machine learning applications.

## Data Processing Steps

1. Download and Process PIREP Data
    a. Run `PIREP_downloads.ipynb`
       - Downloads historical PIREP data from Iowa State University archive (2003-present)
       - Creates "pirep_downloads" folder containing monthly data files
       - Combines all data into "all_pireps.csv"

    b. Run `turb_eda_preprocessing.ipynb` 
       - Performs exploratory data analysis
       - Adds new columns and filters data
       - Creates "csv_fl_rem.csv" in "updated_CSVs" directory
       - Generates flight-level specific files:
         - low_fl.csv
         - med_fl.csv  
         - high_fl.csv

    c. Run `modg_preprocess.ipynb`
       - Filters for moderate-or-greater (MODG) turbulence reports
       - Downloads additional filtered data
       - Creates "csv_modg_all.csv" in updated_CSVs folder
       - Generates MODG flight-level specific files:
         - low_fl_modg.csv
         - med_fl_modg.csv
         - high_fl_modg.csv

    d. Optionally run `convert2riskmap.ipynb` to visualize PIREP spatial distribution

2. Grid the PIREPs
    - Run grid_pireps code after configuring input/output options
    - Select appropriate PIREP CSV file and save location

3. Prepare Atmospheric Data
    - Format data to match sample files:
      - MERRA2_sample_H.nc
      - MERRA2_sample_U.nc
    - Note: PIREPs are gridded to MERRA-2 grid; adjust gridding script if using different atmospheric model

4. Generate Training Data
    - Run `make_training_data.py` to create deep learning training files

5. Train Neural Network
    - Sample model provided in neuralnet directory
    - Run `train_TurbulenceNN.py` to train model
    - Sample weights and normalization parameters included

6. Run Model
    - Execute `plot_merra2_turbulence.py` to generate predictions
