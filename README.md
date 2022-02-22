# Setup
python 3.7
python -m pip install --upgrade pip
pip install -r requirements.txt

# Basic usage:
- it has been tested on data/input/a.xlsx and b.xlsx
- go to helpers/xls_extractor.py
- run:python xls_extractor.py ../data/input/a.xlsx
- this script is using helpers and helpers/resources folder.
- it automatically detects headers from tables and titles from sheet and creates df of it.
- it detects data rows and differenciates it from data that is in the file but not in table structure and puts it into seperate .txt file

# Plugins:
- zip
- load df or csv file to the db

# Scenarios:
- scenario1 - zip
- scenario3 - zip + load to db 

# Extract
Factory pattern - for extractors from different sources:
- Data in tabular format - df
- Other data - .txt file
Solution is to list the files and then load them in parallel process them, merge them and get the counts with all nuts and bolts in place.
TODO: format detection and extractors for different data types.

# Transform
zip files

# Load
for now only for sending notifications and loading to the db