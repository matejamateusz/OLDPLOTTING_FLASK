from tasks import *
#import ROOT
import json
import sys, os, io
os.environ['TERM'] = 'dumb'
def content():
    with open('json_files/datahistogram-r2.json') as dane:
        data = json.load(dane)
        content = json.dumps(data, ensure_ascii="False")
        print content
content()
