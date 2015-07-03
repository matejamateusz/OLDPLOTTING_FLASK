#!/usr/bin/python
from __future__ import division
import sys
import time
import math
#import pytz
import json
import shelve
#from matplotlib import pyplot as plt
#from matplotlib import dates
from oracle_wincc import getWinCCData
from datetime import datetime

#local = pytz.timezone('Europe/Amsterdam')

def mktimeUTC(utc_tuple):
    """Generates a UTC time.mktime"""
    """From an input tuple of the type (yyyy,mm,dd,HH,MM,SS,ds,cs,ms)"""
    if len(utc_tuple) == 6:
        utc_type += (0,0,0)
    #account for hourly time change (to be understood)
    return (time.mktime(utc_tuple) - time.mktime((1970, 1, 1, 0, 0, 0, 0, 0, 0))) - (time.mktime((1970, 1, 1, 1, 0, 0, 0, 0, 0)) - time.mktime((1970, 1, 1, 0, 0, 0, 0, 0, 0)))

def mkscatterplt(time1, data1, time2, data2, interval):
    """Creates two lists of values to be plotted in a scatter plot"""
    """Needs time and data lists as input and the last argument is the interval of time correlation"""
    val1 = []
    val2 = []
    if len(data1) == len(data2):
        for i in range(len(data1)):
            if (time1[i] - time2[i] > -interval) and (time1[i] - time2[i] < interval):
                val1.append(data1[i])
                val2.append(data2[i])
    else:
        #try zip
        #data_zipped = zip(zip(data1, time1), zip(data2, time2))
        
        for i in range(len(data1)):
            for j in range(len(data2)):
                if (time1[i] - time2[j] > -interval) and (time1[i] - time2[j] < interval):
                    val1.append(data1[i])
                    val2.append(data2[j])
    
    return val1, val2

def mkjson(index, json_name, myShelve, *args):
    """Generates a json file according to specs of presenter"""
    dict_json = {}
    if len(myShelve[index][args+('values',)]) > 1:
        dict_json['values'] = myShelve[index][args+('values',)]

        #First point in dictionaries
        dict_json['uncertainties'] = [[-0.1,0.1]]
        init_diff = (myShelve[index][args+('offset_time',)][1])-(myShelve[index][args+('offset_time',)][0])
        dict_json['binning'] = [[((myShelve[index][args+('offset_time',)][0])-init_diff), myShelve[index][args+('offset_time',)][0]]]
        #Rest of array
        for i in range(len(myShelve[index][args+('values',)])-1):
            dict_json['uncertainties'].append([-0.1,0.1])
            dict_json['type'] = ["histogram"]
            dict_json['binning'].append([myShelve[index][args+('offset_time',)][i], myShelve[index][args+('offset_time',)][i+1]])
    
        #Graphics info
        splittitle = args[0].split('.')
        yaxis_title = splittitle[len(splittitle)-1]
        title = splittitle[len(splittitle)-2] + '/' + splittitle[len(splittitle)-1]
        dict_json['axis_titles'] = [yaxis_title, 'Offset_time', title]

        #print len(dict_json['values']), len(dict_json['binning']), len(dict_json['uncertainties']), len(myShelve[index][(dp, 'values')]), len(myShelve[index][(dp, 'offset_time')])
    
        #Generate file
        with open(json_name, 'w') as f:
            json.dump(dict_json, f)
