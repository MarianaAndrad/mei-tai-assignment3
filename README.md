# LAB03 - Music and Genre Likeness Using Information distances


## Authors
- Filipe Silveira - 97981
- Mariana Andarde - 103823
- Vicente Barros - 97787

# Overview
This project aims to analyze the similarity between music genres using information distances.
The project uses the _GetMaxFreqs_ program to extract the maximum frequency of the audio files and then 
calculates the information distance between the audio files. The project uses the information distance to 
calculate the similarity between the audio files and then uses the similarity to calculate the similarity between the genres.

## Repository structure
- `analysis/` - Folder is used for the analysis of the results and to store the analysis.
- `cache/` - Folder is used to avoid recalculating the compression length.
- `database/` - Folder contains our database with our audio files and their signatures.
- `datasets/` - Folder contains all of our music files organized by source and their sub-folders organized by genre.
- `GetMaxFreqs/` - Source code for the GetMaxFreqs program
- `deliveries/` - Folder contains the deliveries of the project (report, and video).
- `src/` - Directory serves as the main container for all our source files. It includes several key Python scripts that handle various aspects of our audio processing and analysis pipeline.
- `generate_data.sh` - Script to generate the database for different parameters using the GetMaxFreqs program
- `generate_best_data.sh` - Script to generate the database for different noise levels using the best parameters found in the previous step using the GetMaxFreqs program

## How to run the application
To run the application, follow these steps:

1. Create a virtual environment using the command `python -m venv venv`
2. Activate the virtual environment using the command `source venv/bin/activate`
3. Install the requirements using the command `pip install -r requirements.txt`
4. Ensure that there is a version called EXAMPLE in the database folder for demonstrations purposes download the file from the urls
5. Go to the `src/` folder and run the command `streamlit run app.py`

# Results
The results of our analysis can be through this [link](https://mega.nz/folder/QTslDQpB#RuQ-gC7EBgRQ8EowLEQDJA).

## Test done to determine the best parameters to use in the GetMaxFreqs program
The results of the project are in the `src/results` folder. To generate the results, run the `generate_data.sh` script and the results will be generated in folder.

## To determinate the impact of noise levels
The results of the project are in the `src/results` folder. To generate the results, run the `generate_best_data.sh` script and the results will be generated in folder.

## Generate graphs
To generate the graphs, run the file `analysis/graphs_generate.py` and the graphs will be generated in the `analysis/plots` folder.
