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
    
    results = cur.fetchall()
    
    # Close Connection to Robin
    cur.close()
    conn.close()
                        
    return results

# Download a set of images.
def download_images(image_count, results = []):
        
    # Download the images
    for i in range(0, image_count - 1):
        urllib.urlretrieve(str(results[i][0]), "images/" + results[i][1])
    
# Get all of the images in the images directory into a txt file.
def get_image_list():
    # Look for images successfully downloaded into images folder
    files = glob.glob ('images/*.jpg')
    
    # Create a file
    with open('images.txt', 'w+') as in_files:
        for eachfile in files: in_files.write(eachfile+' 1:10 2:10 3:10 4:10 5:10 6:10\n')

# Remove all of the images in the images directory.
def remove_images():
    files = glob.glob('images/*.jpg')
        
    for f in files:
        os.remove(f)    

# Cycle through all of the images and perform all of the subtasks
def cycle_through_images(start, stop, max, results = []):

    filepath = "images.txt"
    tablename = "ben.compute_vision_hackday"

    # Cycle through all of the images from start to stop in max increments.
    while (start <= stop):

        new_results = results[start:(start + max - 1)]

        print("Retrieving " + str(start) + " to " + str(start+max) + " images.")
        print new_results

        remove_images()

        download_images(max, new_results)
        
        # Create input text file
        get_image_list()
        
        # Call Ben's Script
        google_vision_tool.main(filepath, tablename)

        # Reset to next set
        start = start + max


def main():
    
    # Set Initial Values
    max = 10

    # Get Arguments
    try: 
        applicationId = sys.argv[1]
        print("Getting Images for ApplicationId:" + applicationId +"\n")
    except IndexError as err:
        print 'ERROR: Missing Input Parameter'
        exit()  
    
    # Empty SQL Results
    results = []
    
    # Get all of the images associated with the event
    results = get_event_images(applicationId)
    print("There are " + str(len(results)) + " images related to this event\n")

    # Download the images
    start = 0
    stop = (len(results) - 1)
    cycle_through_images(start, stop, max, results)
    
    # Delete Images
    remove_images()
    
if __name__ == "__main__":
    
    main()

