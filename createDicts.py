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

from genericsmk import *

dpFillNumbers = 'LHC:LHCCOM/LHC.LHC.RunControl.FillNumber'
dpRunNumbers = 'LHC:LHCCOM/LHC.LHCb.Internal.RunNumber'
dpStates = 'LHC:LHC_STATE/LHC.State.Text'
runI_start = datetime(2011,03,12,00)
runI_end = datetime(2013,02,15,00) 

def createdictionary_singleFill(dps, fillnumber, dict_fill):
    #Create the key for that runnumber if not already there, if not, don't
    if str(fillnumber) not in dict_fill:
        print 'Updating Fill Numbers'
        #Get fillnumbers and states per fillnumber
        fillnumbers = getWinCCData(dpFillNumbers, runI_start, runI_end)
        #Nested dictionaries for fill number
        if fillnumbers:
            for row in fillnumbers:
                str_key_curr = row[2]
                if str_key_curr not in dict_fill:
                    dict_fill[str_key_curr] = {'start':row[1][:-7]}
    else:
        print 'No need to update Fill Numbers'

    #Fill up the values for that key 
    str_key_curr = str(fillnumber)
    str_key_next = str(fillnumber+1)
    
    if str_key_curr and str_key_next in dict_fill:
        states = getWinCCData(dpStates, dict_fill[str_key_curr]['start'], dict_fill[str_key_next]['start'])                
        if states:
            print 'Updating LHC states'
            for states_row in states:
                dict_fill[str_key_curr][states_row[2].lower()] = states_row[1][:-7]

    #if states are present, get all values for that fill
    values = getWinCCData(dps, dict_fill[str_key_curr]['start'], dict_fill[str_key_next]['start'])
    if values:
        print 'Retrieving %d datapoints' % len(dps)
        dict_json = {}
        utc_time_list = []
        run_time_list = []
        values_list = []
        prev_dp = values[0][0]
        for values_row in values:
            if prev_dp != values_row[0]:
                #Write list in shelve if dp changes
                dict_fill[str_key_curr][(prev_dp,'utc_time')] = utc_time_list
                dict_fill[str_key_curr][(prev_dp,'offset_time')] = run_time_list
                dict_fill[str_key_curr][(prev_dp,'values')] = values_list
                dict_fill[str_key_curr][(prev_dp,'uncertainties')] = ['','']
                dict_fill[str_key_curr][(prev_dp,'binning')] = ['','']
                splittitle = prev_dp.split('.')
                title = splittitle[len(splittitle)-2] + '/' + splittitle[len(splittitle)-1]
                dict_fill[str_key_curr][(prev_dp,'axis_title')] = [title,'']
                #Reset lists
                utc_time_list = []
                run_time_list = []
                values_list = []
            #Store UTC time (to understand the one hour correction)
            utc_time = int(mktimeUTC( (datetime.strptime(values_row[1][:-7], '%Y-%m-%d %H:%M:%S')).timetuple() ))
            utc_time_list.append(utc_time)
            #Store time elapsed since beginning of run (in s)
            if 'physics' in  dict_fill[str_key_curr].keys():
                init_time = int(mktimeUTC( (datetime.strptime(dict_fill[str_key_curr]['physics'], '%Y-%m-%d %H:%M:%S')).timetuple() ))
                sb_time = (utc_time - init_time) / (60.0*60.0)
            else:
                init_time = int(mktimeUTC( (datetime.strptime(dict_fill[str_key_curr]['start'], '%Y-%m-%d %H:%M:%S')).timetuple() ))
                sb_time = (utc_time - init_time) / (60.0)
            run_time_list.append(sb_time)
            #Store values at those times
            values_list.append(values_row[2])
            prev_dp = values_row[0]
                
        #Write last list in shelve 
        dict_fill[str_key_curr][(prev_dp,'utc_time')] = utc_time_list
        dict_fill[str_key_curr][(prev_dp,'offset_time')] = run_time_list
        dict_fill[str_key_curr][(prev_dp,'values')] = values_list
        dict_fill[str_key_curr][(prev_dp,'uncertainties')] = ['','']
        dict_fill[str_key_curr][(prev_dp,'binning')] = ['','']
        splittitle = prev_dp.split('.')
        title = splittitle[len(splittitle)-2] + '/' + splittitle[len(splittitle)-1]
        dict_fill[str_key_curr][(prev_dp,'axis_title')] = [title,'']
        #Reset lists
        utc_time_list = []
        run_time_list = []
        values_list = []
 
    #Add list of RunNumber        
    runnumbers = getWinCCData(dpRunNumbers, dict_fill[str_key_curr]['start'], dict_fill[str_key_next]['start'])  
    prev_dp = dpRunNumbers[0]
    if runnumbers:
        print 'Adding list of Run Numbers'
        for values_row in runnumbers:
            #Store UTC time (to understand the one hour correction)
            utc_time = int(mktimeUTC( (datetime.strptime(values_row[1][:-7], '%Y-%m-%d %H:%M:%S')).timetuple() ))
            utc_time_list.append(utc_time)
            #Store time elapsed since beginning of run (in s)
            if 'physics' in  dict_fill[str_key_curr].keys():
                init_time = int(mktimeUTC( (datetime.strptime(dict_fill[str_key_curr]['physics'], '%Y-%m-%d %H:%M:%S')).timetuple() ))
                sb_time = (utc_time - init_time) / (60.0*60.0)
            else:
                init_time = int(mktimeUTC( (datetime.strptime(dict_fill[str_key_curr]['start'], '%Y-%m-%d %H:%M:%S')).timetuple() ))
                sb_time = (utc_time - init_time) / (60.0)
            run_time_list.append(sb_time)
                
            #Store values at those times
            values_list.append(values_row[2])

        #Write last list in shelve 
        dict_fill[str_key_curr][(prev_dp,'utc_time')] = utc_time_list
        dict_fill[str_key_curr][(prev_dp,'offset_time')] = run_time_list
        dict_fill[str_key_curr][(prev_dp,'values')] = values_list
        dict_fill[str_key_curr][(prev_dp,'uncertainties')] = ['','']
        dict_fill[str_key_curr][(prev_dp,'binning')] = ['','']
        splittitle = prev_dp.split('.')
        title = splittitle[len(splittitle)-2] + '/' + splittitle[len(splittitle)-1]
        dict_fill[str_key_curr][(prev_dp,'axis_title')] = [title,'']
        #Reset lists
        utc_time_list = []
        run_time_list = []
        values_list = []
    else:
        print 'For some reason, Fill Numbers are not present in dictionary'

    return dict_fill

def createdictionary_singleRun(dps, runnumber, dict_run):
    #Create the key for that runnumber if not already there, if not, don't
    if str(runnumber) not in dict_run:
        print 'Updating Run Numbers'
        #Get fillnumbers and states per fillnumber
        runnumbers = getWinCCData(dpRunNumbers, runI_start, runI_end)
        #Nested dictionaries for fill number
        if runnumbers:
            for row in runnumbers:
                str_key_curr = row[2]
                if str_key_curr not in dict_run:
                    dict_run[str_key_curr] = {'start':row[1][:-7]}
    else:
        print 'No need to update Run Numbers'

    #Fill up the values for that key 
    str_key_curr = str(runnumber)
    str_key_next = str(runnumber+1)
    if str_key_curr and str_key_next in dict_run:
        states = getWinCCData(dpStates, dict_run[str_key_curr]['start'], dict_run[str_key_next]['start'])                
        if states:
            print 'Updating LHC states'
            for states_row in states:
                dict_run[str_key_curr][states_row[2].lower()] = states_row[1][:-7]
        else:
            print 'No LHC states updated in this Run Number'

        values = getWinCCData(dps, dict_run[str_key_curr]['start'], dict_run[str_key_next]['start'])
        if values:
            print 'Retrieving %d datapoints' % len(dps)
            dict_json = {}
            utc_time_list = []
            run_time_list = []
            values_list = []
            prev_dp = values[0][0]
            for values_row in values:
                if prev_dp != values_row[0]:
                    #Write list in shelve if dp changes
                    dict_run[str_key_curr][(prev_dp,'utc_time')] = utc_time_list
                    dict_run[str_key_curr][(prev_dp,'offset_time')] = run_time_list
                    dict_run[str_key_curr][(prev_dp,'values')] = values_list
                    dict_run[str_key_curr][(prev_dp,'uncertainties')] = ['','']
                    dict_run[str_key_curr][(prev_dp,'binning')] = ['','']
                    splittitle = prev_dp.split('.')
                    title = splittitle[len(splittitle)-2] + '/' + splittitle[len(splittitle)-1]
                    dict_run[str_key_curr][(prev_dp,'axis_title')] = [title,'']
                    #Reset lists
                    utc_time_list = []
                    run_time_list = []
                    values_list = []
                #Store UTC time (to understand the one hour correction)
                utc_time = int(mktimeUTC( (datetime.strptime(values_row[1][:-7], '%Y-%m-%d %H:%M:%S')).timetuple() ))
                utc_time_list.append(utc_time)
                #Store time elapsed since beginning of run (in s)
                init_time = int(mktimeUTC( (datetime.strptime(dict_run[str_key_curr]['start'], '%Y-%m-%d %H:%M:%S')).timetuple() ))
                run_time = (utc_time - init_time)/(60.0)
                run_time_list.append(run_time)
                #Store values at those times
                values_list.append(values_row[2])
                prev_dp = values_row[0]

            #Write last list in shelve 
            dict_run[str_key_curr][(prev_dp,'utc_time')] = utc_time_list
            dict_run[str_key_curr][(prev_dp,'offset_time')] = run_time_list
            dict_run[str_key_curr][(prev_dp,'values')] = values_list
            dict_run[str_key_curr][(prev_dp,'uncertainties')] = ['','']
            dict_run[str_key_curr][(prev_dp,'binning')] = ['','']
            splittitle = prev_dp.split('.')
            title = splittitle[len(splittitle)-2] + '/' + splittitle[len(splittitle)-1]
            dict_run[str_key_curr][(prev_dp,'axis_title')] = [title,'']
    else:
        print 'For some reason, run numbers are not present in dictionary'

    return dict_run

def createdictionary_timeinterval(dps, start_time, stop_time, dict_interval):
    if 'interval' not in dict_interval.keys():
        dict_interval['interval'] = {}

    fillnumbers = getWinCCData(dpFillNumbers, start_time, stop_time)
    if fillnumbers:
        print 'Updating Fill Numbers'
        for row in fillnumbers:
            str_key_curr = row[2]
            dict_interval['interval'][(str_key_curr, start_time, stop_time)] = row[1][:-7]
    else:
        print 'No Fill Numbers updated in time interval'

    states = getWinCCData(dpStates, start_time, stop_time)
    if states:
        print 'Updating LHC states'
        for states_row in states:
            dict_interval['interval'][(states_row[2].lower(), start_time, stop_time)] = states_row[1][:-7]
    else:
        print 'No LHC states updated in time interval'

    values = getWinCCData(dps, start_time, stop_time)
    if values:
        print 'Retrieving %d datapoints' % len(dps)
        dict_json = {}
        utc_time_list = []
        run_time_list = []
        values_list = []
        prev_dp = values[0][0]
        for values_row in values:
            if prev_dp != values_row[0]:
                #Write list in shelve if dp changes
                dict_interval['interval'][(prev_dp, start_time, stop_time,'utc_time')] = utc_time_list
                dict_interval['interval'][(prev_dp, start_time, stop_time,'offset_time')] = run_time_list
                dict_interval['interval'][(prev_dp, start_time, stop_time,'values')] = values_list
                dict_interval['interval'][(prev_dp, start_time, stop_time,'uncertainties')] = ['','']
                dict_interval['interval'][(prev_dp, start_time, stop_time,'binning')] = ['','']
                splittitle = prev_dp.split('.')
                title = splittitle[len(splittitle)-2] + '/' + splittitle[len(splittitle)-1]
                dict_interval['interval'][(prev_dp, start_time, stop_time,'axis_title')] = [title,'']
                #Reset lists
                utc_time_list = []
                run_time_list = []
                values_list = []
            #Store UTC time (to understand the one hour correction)
            utc_time = int(mktimeUTC( (datetime.strptime(values_row[1][:-7], '%Y-%m-%d %H:%M:%S')).timetuple() ))
            utc_time_list.append(utc_time)
            #Store time elapsed since beginning of run (in s)
            if (start_time, stop_time, 'physics') in  dict_interval['interval'].keys():
                init_time = int(mktimeUTC( (datetime.strptime(dict_interval['interval'][(start_time, stop_time, 'physics')], '%Y-%m-%d %H:%M:%S')).timetuple() ))
                sb_time = (utc_time - init_time) / (60.0*60.0)
            else:
                init_time = start_time
                sb_time = (utc_time - init_time) / (60.0)
            run_time_list.append(sb_time)
            #Store values at those times
            values_list.append(values_row[2])
            prev_dp = values_row[0]
                
        #Write last list in shelve 
        dict_interval['interval'][(prev_dp, start_time, stop_time,'utc_time')] = utc_time_list
        dict_interval['interval'][(prev_dp, start_time, stop_time,'offset_time')] = run_time_list
        dict_interval['interval'][(prev_dp, start_time, stop_time,'values')] = values_list
        dict_interval['interval'][(prev_dp, start_time, stop_time,'uncertainties')] = ['','']
        dict_interval['interval'][(prev_dp, start_time, stop_time,'binning')] = ['','']
        splittitle = prev_dp.split('.')
        title = splittitle[len(splittitle)-2] + '/' + splittitle[len(splittitle)-1]
        dict_interval['interval'][(prev_dp, start_time, stop_time,'axis_title')] = [title,'']
        #Reset lists
        utc_time_list = []
        run_time_list = []
        values_list = []
        
 
    runnumbers = getWinCCData(dpRunNumbers, start_time, stop_time)
    prev_dp = dpRunNumbers[0]
    if runnumbers:
        print 'Updating Run Numbers'
        for values_row in runnumbers:
            #Store UTC time (to understand the one hour correction)
            utc_time = int(mktimeUTC( (datetime.strptime(values_row[1][:-7], '%Y-%m-%d %H:%M:%S')).timetuple() ))
            utc_time_list.append(utc_time)
            #Store time elapsed since beginning of run (in s)
            if (start_time, stop_time, 'physics') in  dict_interval['interval'].keys():
                init_time = int(mktimeUTC( (datetime.strptime(dict_interval['interval'][(start_time, stop_time, 'physics')], '%Y-%m-%d %H:%M:%S')).timetuple() ))
                sb_time = (utc_time - init_time) / (60.0*60.0)
            else:
                init_time = start_time
                sb_time = (utc_time - init_time) / (60.0)
            run_time_list.append(sb_time)

            #Store values at those times
            values_list.append(values_row[2])

        #Write last list in shelve 
        dict_interval['interval'][(prev_dp, start_time, stop_time,'utc_time')] = utc_time_list
        dict_interval['interval'][(prev_dp, start_time, stop_time,'offset_time')] = run_time_list
        dict_interval['interval'][(prev_dp, start_time, stop_time,'values')] = values_list
        dict_interval['interval'][(prev_dp, start_time, stop_time,'uncertainties')] = ['','']
        dict_interval['interval'][(prev_dp, start_time, stop_time,'binning')] = ['','']
        splittitle = prev_dp.split('.')
        title = splittitle[len(splittitle)-2] + '/' + splittitle[len(splittitle)-1]
        dict_interval['interval'][(prev_dp, start_time, stop_time,'axis_title')] = [title,'']
        #Reset lists
        utc_time_list = []
        run_time_list = []
        values_list = []    
    else:
        print 'No Run Numbers updated in time interval'

    return dict_interval
