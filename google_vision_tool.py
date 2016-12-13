#!/usr/bin/env python

import sys
import os

reload(sys)
sys.setdefaultencoding('utf-8')

import pandas as pd
import numpy as np

import json
import requests
import psycopg2

import google_code



def push_to_database(result_json,table_name):

    result_json = result_json['responses']

    conn = psycopg2.connect("dbname='analytics' user='etl' host='10.223.192.6' password='s0.Much.Data' port='5432'")
    cur = conn.cursor()

    print google_code.DETECTION_TYPES
    
    for entry in result_json:
        input_list = []
        if len(entry.keys()) == 0:
            continue
        for key in ['filename','faceAnnotations','labelAnnotations','safeSearchAnnotation','textAnnotations']:
            if key in entry:
                input_list.append(json.dumps(entry[key]))
            else:
                input_list.append(None)

        format_string = ','.join(['%s' for i in np.arange(len(input_list))])
        insert_string = """INSERT INTO """ + table_name + """ VALUES (""" + format_string + """)"""

        cur.execute(insert_string,tuple(input_list))
        conn.commit()

    cur.close()
    conn.close()
                        
    return 1

def google_call(payload):
    
    #payload = open(filepath, 'rb').read()
    response = requests.post(url='https://vision.googleapis.com/v1/images:annotate?key=AIzaSyB-Nn689M8B9UKSP6mfrQiKbgDHHfBpr-U',data=json.dumps(payload),headers={'Content-Type': 'application/json'})

    #return json.loads(response.text)
    return response.text

def build_payload(image_list_file):

    input_lines = file(image_list_file,'r').readlines()
    google_code.main(input_lines,'payload.json')    

    return json.load(file('payload.json')),map(lambda x: x.split()[0],input_lines)

def main():

    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = 'files_to_analyze.csv'

    if len(sys.argv) > 2:
        tablename = sys.argv[2]
    else:
        tablename = 'ben.image_vision_test'

    try:
        payload,imagepath_list = build_payload(filepath)
    except:
        print 'ERROR Unable to build payload for API call. Make sure file exists'
        raise        

    try:
        result = google_call(payload)
        result_json = json.loads(result)        
        print 'LOG Succesful API call'        
    except:
        print 'ERROR Failed API call'
        raise
    
    for i,entry in enumerate(result_json['responses']):
        entry['filename'] = imagepath_list[i]

    print result_json['responses'][0].keys()
    print result_json['responses'][1].keys()    
        
    try:
        push_to_database(result_json,tablename)
    except:
        print 'ERROR Unable to push to database. Make sure table is consistent with input schema'
        raise

    return 1
    

if __name__ == "__main__":
    
    main()

    
    
