#!/usr/bin/python

import urllib
import psycopg2
import glob
import sys
import os
import google_vision_tool

# Get Image URLs from Event
def get_event_images(applicationId):
    
    # Get Connection to Robin
    conn = psycopg2.connect("dbname='analytics' user='etl' host='10.223.192.6' password='s0.Much.Data' port='5432'")
    cur = conn.cursor()
    
    # Query Results List
    results = []
    
    # SQL Query to get Images
    image_list_sql = """SELECT 'https://d3dhqk2br2olrw.cloudfront.net/' || LOWER(ucii.externalimageid) || '.jpg' AS ImageURL, LOWER(ucii.externalimageid) || '.jpg' AS FileName FROM PUBLIC.Ratings_UserCheckIns UCI JOIN PUBLIC.Ratings_UserCheckInImages UCII ON UCI.CheckInId = UCII.CheckInId WHERE UCI.ApplicationId = UPPER('""" + applicationId + """');"""
    
    # Execute SQL Query
    cur.execute(image_list_sql)
    
    # Get all records into a list
    results = cur.fetchall()
    
    # Close Connection to Robin
    cur.close()
    conn.close()
                        
    return results

# Download a set of images.
def download_images(results = []):
        
    # Download the images
    for i in range(0, len(results)):
        try:
            urllib.urlretrieve(str(results[i][0]), "images/" + results[i][1])
        except:
            print("Unable to load the file: " + results[i][1] + "\n")
            pass 
    
# Get all of the images in the images directory into a txt file.
def get_image_list(file_name):

    # Look for images successfully downloaded into images folder
    files = glob.glob ('images/*.jpg')
    
    # Create list of images in the directory
    with open(file_name, 'w+') as in_files:
        for eachfile in files: in_files.write(eachfile +' 1:10 2:10 3:10 4:10 5:10 6:10\n')

# Remove all of the images in the images directory.
def remove_images():

    # Retreive all .jpg files in the images directory
    files = glob.glob('images/*.jpg')
    
    # Cycle through and delete all jpg files.    
    for f in files:
        os.remove(f)    

def clear_output_table(output_table_name, applicationId):

    conn = psycopg2.connect("dbname='analytics' user='etl' host='10.223.192.6' password='s0.Much.Data' port='5432'")
    cur = conn.cursor()

    # Clear out table for specific applicationids
    delete_string = """DELETE FROM """ + output_table_name + """ WHERE ApplicationId = '""" + applicationId + """'"""
    cur.execute(delete_string)
    conn.commit()

    cur.close()
    conn.close()


# Cycle through all of the images and perform all of the subtasks
def cycle_through_images(results_start_index, results_stop_index, dl_image_max, application_Id, results = []):

    file_name = "images.txt"
    output_table_name = "JT.Compute_Vision_Hackday"

    # Clear output table
    clear_output_table(output_table_name, application_Id)

    # Cycle through all of the images in the results image
    while (results_start_index <= results_stop_index):

        # Set the new increment for iteration of the for loop
        results_new_end = results_start_index + dl_image_max

        # Get the subset of images from the image list
        new_results = results[results_start_index:results_new_end]

        # Get the true subset end index
        if results_stop_index < results_new_end:
            results_new_end = results_stop_index + 1

        # Display where in the image list the for loop is processing.
        print("Retrieving " + str(results_start_index + 1) + " to " + str(results_new_end) + " images of " + str(results_stop_index + 1) + " total images.")

        # Remove any images in the images directory
        remove_images()

        # Download the new images
        download_images(new_results)
        
        # Create input text file
        get_image_list(file_name)
        
        # Call Ben's Script
        google_vision_tool.main(file_name, output_table_name, application_Id)

        # Reset to next set
        results_start_index= results_start_index + dl_image_max



def main():
    
    # Set Max Image Download Number
    dl_image_max = 10

    # Get Event ID Argument
    try: 
        application_Id = sys.argv[1]
        print("Getting Images for ApplicationId: " + application_Id + "\n")
    except IndexError as err:
        print 'ERROR: Missing ApplicationId Input Parameter'
        exit()  

        
    # Initialize SQL Results
    results = []
    
    # Get all of the images associated with an event
    results = get_event_images(application_Id)
    print("There are " + str(len(results)) + " images related to this event\n")

    # Download the images
    results_start_index = 0
    results_stop_index = (len(results) - 1)
    cycle_through_images(results_start_index, results_stop_index, dl_image_max, application_Id, results)
    
    # Delete Images - Final Time
    remove_images()

    print "Done\n"
    
if __name__ == "__main__":
    
    main()

