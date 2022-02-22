# Setup

python 3.7

python -m pip install --upgrade pip

pip install -r requirements.txt

# Basic usage:
- it has been tested on data/input/a.xlsx and b.xlsx
- go to helpers/xls_extractor.py
- run: 
	python xls_extractor.py /data/input/a.xlsx
	python xls_extractor.py /data/input/b.xlsx
- this script is using helpers and helpers/resources folder.
- it automatically detects headers from tables and creates df of it. In many cases there are 1-4 letter mistakes in headers (eg. x in place of +) so script is able to detect these small differences and assume that if there are up to 4 characters differece we can treat these headers as the same. In b.xlsx there are 2 different tables (they are different by 1 column), as an output there are 2 dfs.
- it detects data rows and differenciates it from data that is in the file but not in table structure and puts it into seperate .txt file
- output files are stored in data/output directory

# Plugins:
- zip
- load df or csv file to the db

# Output Managers:
- Different path managers to store data in local / remote or on Hadoop cluster.
- all placed in: helpers/base.py
- helped to decouple xls_extractor from path_manager - now we can use different path_managers depending on our task.

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
