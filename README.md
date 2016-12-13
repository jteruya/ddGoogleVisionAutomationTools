# GoogleVisionAutomationTools

google_vision_tool.py
-> This script takes a set of images that are stored locally, builds a JSON payload that is compatible with the Google vision API, calls the API, and pushes the result of the request to a table that has already been defined on Robin.  

The dependencies are the following:  
Python 2  
psycopg2 (pip install psycopg2)  

To run from the command line:  
git clone git@ddgit.me:bcerio/GoogleVisionAutomationTools.git  
cd GoogleVisionAutomationTools  
python google_vision_tool.py files_to_analyze.csv ben.compute_vision_hackday  

The first command line argument is the file containing the image files and Google API parameters. An example file, files_to_analyze.csv, is included in the repo. The contents of the example file are:  

test1.jpg 1:10 2:10 3:10 4:10 5:10 6:10  
test2.jpg 1:10 2:10 3:10 4:10 5:10 6:10  

The first column is the path to the image file locally. The remaining columns specify what features to use and the max number of results: <feature_index>:<max_results>, where  

TYPE_UNSPECIFIED: 0  
FACE_DETECTION: 1  
LANDMARK_DETECTION: 2  
LOGO_DETECTION: 3  
LABEL_DETECTION: 4  
TEXT_DETECTION: 5  
SAFE_SEARCH_DETECTION: 6  

You must adhere to this format for the script to run properly.  

The second command line argument is the name of the table on Robin where the result will be pushed. It has the following structure:  

CREATE TABLE
ben.compute_vision_hackday
(
        imagefilename TEXT,
        faceannotations JSONB,
        labelannotations JSONB,
        safesearchannotation JSONB,
        textannotations JSONB,
        landmarkannotations JSONB,
        logoannotations JSONB
);
