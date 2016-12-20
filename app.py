#!/usr/bin/env python

import matplotlib

matplotlib.use('Agg')

import sys
import os
import datetime

from flask import Flask, render_template, request, redirect, url_for, abort, session,flash
from flask.ext.session import Session
from redis import Redis

import pickle
import json

import random

app = Flask(__name__)
app.debug = True
app.config['SESSION_TYPE'] = 'redis'
Session(app)

@app.route('/')
def index():
    #for key in session.keys():
    #    session.pop(key, None)
    #session.clear()
    #session.new = True
    #session['sessionid'] = os.urandom(24)
    #session['count'] = 1
    return redirect( url_for('image_chooser') )

@app.route('/image_chooser',methods=['GET'])
def eventchooser():

    return render_template('eventsummary.html')

@app.route('/image_results',methods=['POST'])
def image_results():

    session['eventid'] = request.form['eventid']

    image_url_list = fetch_images(session['eventid'])

    if image_url_list == -999:
        return "Ben doesn't know SQL."
    
    return render_template('image_results.html',image_url_list=image_url_list)

def fetch_images(eventid):

    sql_query = """
                SELECT 'https://d3dhqk2br2olrw.cloudfront.net/' || LOWER(ucii.externalimageid) || '.jpg' AS ImageURL
                FROM PUBLIC.Ratings_UserCheckIns UCI
                JOIN PUBLIC.Ratings_UserCheckInImages UCII
                ON UCI.CheckInId = UCII.CheckInId
                WHERE UCI.ApplicationId = UPPER('%s')
                """ % eventid

    conn = psycopg2.connect("dbname='analytics' user='etl' host='10.223.192.6' password='s0.Much.Data' port='5432'")
    cur = conn.cursor()

    try:
        cur.execute(sql_query)
    except:
        return -999

    entries = cur.fetchall()

    cur.close()
    conn.close()

    return entries

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5050)
