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

logger = Logger()

app = Flask(__name__)
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
    return {"test_json","this is a test"}

@app.route('/eventchooser',methods=['POST'])
def eventchooser():

    return render_template('eventsummary.html',eventid=session['eventid'],eventname=session['eventname'],n_sessions=str(n_sessions),n_filters=str(n_filters),accountname=session['accountname'],eventtype=session['eventtype'])
 
def plot_tag_counts(user_data):

    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn
    import hashlib

    from matplotlib import rcParams
    rcParams.update({'figure.autolayout': True})

    df = pd.DataFrame(map(lambda x: x[1],user_data),columns=['count'],index=map(lambda x: x[0],user_data))
    df = df.sort_values(by='count',ascending=True)

    plt.figure()
    df.plot(kind='barh',legend=False,alpha=0.8)
    plt.xlabel('Tags completed')
    filename = 'static/tag_counts.png'
    plt.savefig(filename)

    return hashlib.md5(open(filename,'rb').read()).hexdigest()

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5050)
