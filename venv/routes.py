from venv import app
from flask import Flask, render_template, request, flash, session, redirect, url_for, jsonify
#import LOGIN.forms
from venv.forms import ContactForm, SignupForm, SigninForm
from flask.ext.mail import Message, Mail
from venv.models import db, User
from venv.tasks import *
from subprocess import Popen, PIPE
#import ROOT
import os
import json
os.environ['TERM'] = 'dumb'
mail = Mail()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/home/_select')
def select():
    selected_histogram = request.args.get('a')
    print selected_histogram
    from subprocess import call 
    call(['python', 'ExpCondAnalyser.py', '-r', str(selected_histogram), '-T', '-bla'])
    return jsonify(result=selected_histogram)


@app.route('/data/histogram0.json')
def histodata0():
    final_content_0 = eval(Popen(['python', 'venv/get_json0.py'], stdout=PIPE).communicate()[0])
    return jsonify(**final_content_0)

@app.route('/data/histogram1.json')
def histodata1():
    final_content_1 = eval(Popen(['python', 'venv/get_json1.py'], stdout=PIPE).communicate()[0])
    return jsonify(**final_content_1)

@app.route('/data/histogram2.json')
def histodata2():
    final_content_2 = eval(Popen(['python', 'venv/get_json2.py'], stdout=PIPE).communicate()[0])
    return jsonify(**final_content_2)

@app.route('/data/histogram3.json')
def histodata3():
    final_content_3 = eval(Popen(['python', 'venv/get_json3.py'], stdout=PIPE).communicate()[0])
    return jsonify(**final_content_3)

@app.route('/data/histogram4.json')
def histodata4():
    final_content_4 = eval(Popen(['python', 'venv/get_json4.py'], stdout=PIPE).communicate()[0])
    return jsonify(**final_content_4)

@app.route('/data/histogram5.json')
def histodata5():
    final_content_5 = eval(Popen(['python', 'venv/get_json5.py'], stdout=PIPE).communicate()[0])
    return jsonify(**final_content_5)

@app.route('/data/histogram6.json')
def histodata6():
    final_content_6 = eval(Popen(['python', 'venv/get_json6.py'], stdout=PIPE).communicate()[0])
    return jsonify(**final_content_6)

@app.route('/data/histogram7.json')
def histodata7():
    final_content_7 = eval(Popen(['python', 'venv/get_json7.py'], stdout=PIPE).communicate()[0])
    return jsonify(**final_content_7)

