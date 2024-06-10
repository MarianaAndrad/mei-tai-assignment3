# LAB03 - Music and Genre Likeness Using Information distances


## Authors
- Filipe Silveira - 97981
- Mariana Andarde - 103823
- Vicente Barros - 97787

# Overview

## Repository structure
- `analysis/` - Analysis of the project
- `cache/` - Cache files
- `database/` - Database files
- `datasets/` - Datasets used in the project
- `GetMaxFreqs/` - Source code for the GetMaxFreqs program
- `report/` - Report of the project
- `src/` - Source code of the project
- `generate_data.sh` - Script to generate the data
- `generate_best_data.sh` - Script to generate the best data
- `run.sh` - Script to run the project

## How to run the application
To run the application, follow these steps:

1. Create a virtual environment using the command `python -m venv venv`
2. Activate the virtual environment using the command `source venv/bin/activate`
3. Install the requirements using the command `pip install -r requirements.txt`
4. Ensure that there is a version called EXAMPLE in the database folder for demonstrations purposes download the file from the urls
5. Go to the `src/` folder and run the command `streamlit run app.py`

# Results
## Test done to determine the best parameters to use in the GetMaxFreqs program
The results of the project are in the `src/results` folder. To generate the results, run the `generate_data.sh` script and the results will be generated in folder.

## To determinate the impact of noise levels
The results of the project are in the `src/results` folder. To generate the results, run the `generate_best_data.sh` script and the results will be generated in folder.

## Generate graphs
To generate the graphs, run the file `analysis/graphs_generate.py` and the graphs will be generated in the `analysis/plots` folder.

