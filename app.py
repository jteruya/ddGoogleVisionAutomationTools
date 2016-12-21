#!/usr/bin/env python

import matplotlib

matplotlib.use('Agg')

import sys
import os
import datetime
import unicodedata as ucd

from flask import Flask, render_template, request, redirect, url_for, abort, session,flash
from flask.ext.session import Session
from redis import Redis

import pickle
import json

import random
import psycopg2

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
def image_chooser():

    return render_template('imagebrowser.html')

@app.route('/image_results',methods=['POST'])
def image_results():

    session['eventid'] = request.form['eventid']
    session['keyword'] = request.form['keyword']

    image_url_list = fetch_images(session['eventid'],session['keyword'])

    if image_url_list == -999:
        return "Ben doesn't know SQL."
    
    return render_template('image_results.html',image_url_list=image_url_list)

def fetch_images(eventid,keyword):

    sql_query = """
                SELECT distinct 'https://d3dhqk2br2olrw.cloudfront.net/' || LOWER(ucii.externalimageid) || '.jpg' AS ImageURL
                FROM PUBLIC.Ratings_UserCheckIns UCI
                JOIN PUBLIC.Ratings_UserCheckInImages UCII
                ON UCI.CheckInId = UCII.CheckInId
                join jt.compute_vision_hackday b
                on UPPER(UCI.Applicationid)=upper(b.applicationid)
                and LOWER(ucii.externalimageid)=lower(b.imagefilename)
                WHERE UCI.ApplicationId = upper('%s')
                and 
               ( 
               ((lower((LabelAnnotations->>0)::JSONB->>'description') like lower('%s'))
                and cast(((LabelAnnotations->>0)::JSONB->>'score')as decimal)>.5)
                or ((lower((LabelAnnotations->>1)::JSONB->>'description') like lower('%s'))
                and cast(((LabelAnnotations->>1)::JSONB->>'score')as decimal)>.5)
                or ((lower((LabelAnnotations->>2)::JSONB->>'description') like lower('%s'))
                and cast(((LabelAnnotations->>2)::JSONB->>'score')as decimal)>.5)
                or ((lower((LabelAnnotations->>3)::JSONB->>'description') like lower('%s'))
                and cast(((LabelAnnotations->>3)::JSONB->>'score')as decimal)>.5)
                or ((lower((LabelAnnotations->>4)::JSONB->>'description') like lower('%s'))
                and cast(((LabelAnnotations->>4)::JSONB->>'score')as decimal)>.5)
                or ((lower((LabelAnnotations->>5)::JSONB->>'description') like lower('%s'))
                and cast(((LabelAnnotations->>5)::JSONB->>'score')as decimal)>.5)
                or ((lower((LabelAnnotations->>6)::JSONB->>'description') like lower('%s'))
                and cast(((LabelAnnotations->>6)::JSONB->>'score')as decimal)>.5)
                or ((lower((LabelAnnotations->>7)::JSONB->>'description') like lower('%s'))
                and cast(((LabelAnnotations->>7)::JSONB->>'score')as decimal)>.5)
                or ((lower((LabelAnnotations->>8)::JSONB->>'description') like lower('%s'))
                and cast(((LabelAnnotations->>8)::JSONB->>'score')as decimal)>.5)
                or (lower((textannotations->>0)::JSONB->>'description') like lower('%s'))
                or (lower((textannotations->>1)::JSONB->>'description') like lower('%s'))
                or (lower((textannotations->>2)::JSONB->>'description') like lower('%s'))
                or (lower((textannotations->>3)::JSONB->>'description') like lower('%s'))
                or (lower((textannotations->>4)::JSONB->>'description') like lower('%s'))
                or (lower((textannotations->>5)::JSONB->>'description') like lower('%s'))
                or (lower((textannotations->>6)::JSONB->>'description') like lower('%s'))
                or (lower((textannotations->>7)::JSONB->>'description') like lower('%s'))
                or (lower((textannotations->>8)::JSONB->>'description') like lower('%s'))                           
                )
                """ % (eventid,("%"+keyword+"%"),("%"+keyword+"%"),("%"+keyword+"%"),
                ("%"+keyword+"%"),("%"+keyword+"%"),("%"+keyword+"%"),("%"+keyword+"%"),
                ("%"+keyword+"%"),("%"+keyword+"%"),("%"+keyword+"%"),("%"+keyword+"%"),("%"+keyword+"%"),
                ("%"+keyword+"%"),("%"+keyword+"%"),("%"+keyword+"%"),("%"+keyword+"%"),
                ("%"+keyword+"%"),("%"+keyword+"%"))
    conn = psycopg2.connect("dbname='analytics' user='etl' host='10.223.192.6' password='s0.Much.Data' port='5432'")
    cur = conn.cursor()

    try:
        cur.execute(sql_query)
    except:
        raise
        return -999

    entries = map(lambda x: x[0].strip('\n'),cur.fetchall())

    cur.close()
    conn.close()

    return entries

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5050)
