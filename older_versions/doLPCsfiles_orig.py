#!/usr/bin/python
import sys
import time
import math
import pytz
import json
import shelve
from matplotlib import pyplot as plt
from matplotlib import dates
from oracle_wincc import getWinCCData
from datetime import datetime

#declarations
dpFillNumbers = 'LHC:LHCCOM/LHC.LHC.RunControl.FillNumber'
dpRunNumbers = 'LHC:LHCCOM/LHC.LHCb.Internal.RunNumber'
dpStates = 'LHC:LHC_STATE/LHC.State.Text'
dpsLPC = ['LHC:LHCCOM/LHC.LHCb.Internal.Luminosity.LumiInst_GP', 'LHC:LHCCOM/LHC.LHCb.Internal.Luminosity.LumiSpec_GP', 'LHC:LHCCOM/LHC.LHCb.Internal.Luminosity.Mu', 'LHC:LHCCOM/LHC.LHCb.Internal.Luminosity.PileUp', 'LHC:LHCCOM/LHC.LHCb.Internal.Intensity.Beam1.DCBCTtotalIntensity', 'LHC:LHCCOM/LHC.LHCb.Internal.Intensity.Beam2.DCBCTtotalIntensity']
dpsLPC_VeloLumi = ['LHC:LHCCOM/LHC.LHCb.Internal.VELO.VeloLumiRegionPos.x', 'LHC:LHCCOM/LHC.LHCb.Internal.VELO.VeloLumiRegionPos.xErr', 'LHC:LHCCOM/LHC.LHCb.Internal.VELO.VeloLumiRegionPos.y', 'LHC:LHCCOM/LHC.LHCb.Internal.VELO.VeloLumiRegionPos.yErr', 'LHC:LHCCOM/LHC.LHCb.Internal.VELO.VeloLumiRegionPos.z', 'LHC:LHCCOM/LHC.LHCb.Internal.VELO.VeloLumiRegionPos.zErr', 'LHC:LHCCOM/LHC.LHCb.Internal.VELO.VeloLumiRegionPos.sxUnfold', 'LHC:LHCCOM/LHC.LHCb.Internal.VELO.VeloLumiRegionPos.sxUnfoldErr', 'LHC:LHCCOM/LHC.LHCb.Internal.VELO.VeloLumiRegionPos.syUnfold', 'LHC:LHCCOM/LHC.LHCb.Internal.VELO.VeloLumiRegionPos.syUnfoldErr', 'LHC:LHCCOM/LHC.LHCb.Internal.VELO.VeloLumiRegionPos.szUnfold', 'LHC:LHCCOM/LHC.LHCb.Internal.VELO.VeloLumiRegionPos.szUnfoldErr', 'LHC:LHCCOM/LHC.LHCb.Internal.VELO.VeloLumiRegionPos.xslope', 'LHC:LHCCOM/LHC.LHCb.Internal.VELO.VeloLumiRegionPos.xslopeErr', 'LHC:LHCCOM/LHC.LHCb.Internal.VELO.VeloLumiRegionPos.yslope', 'LHC:LHCCOM/LHC.LHCb.Internal.VELO.VeloLumiRegionPos.yslopeErr'] 
dpsLPC_VeloBeam1Gas = ['LHC:LHCCOM/LHC.LHCb.Internal.VELO.VeloBeamShape.VeloBeam1Shape.Xmean', 'LHC:LHCCOM/LHC.LHCb.Internal.VELO.VeloBeamShape.VeloBeam1Shape.XmeanErr', 'LHC:LHCCOM/LHC.LHCb.Internal.VELO.VeloBeamShape.VeloBeam1Shape.Ymean', 'LHC:LHCCOM/LHC.LHCb.Internal.VELO.VeloBeamShape.VeloBeam1Shape.YmeanErr', 'LHC:LHCCOM/LHC.LHCb.Internal.VELO.VeloBeamShape.VeloBeam1Shape.Xslope', 'LHC:LHCCOM/LHC.LHCb.Internal.VELO.VeloBeamShape.VeloBeam1Shape.XslopeErr', 'LHC:LHCCOM/LHC.LHCb.Internal.VELO.VeloBeamShape.VeloBeam1Shape.Yslope', 'LHC:LHCCOM/LHC.LHCb.Internal.VELO.VeloBeamShape.VeloBeam1Shape.YslopeErr', 'LHC:LHCCOM/LHC.LHCb.Internal.VELO.VeloBeamShape.VeloBeam1Shape.XsigmaUnfold', 'LHC:LHCCOM/LHC.LHCb.Internal.VELO.VeloBeamShape.VeloBeam1Shape.XsigmaUnfoldErr', 'LHC:LHCCOM/LHC.LHCb.Internal.VELO.VeloBeamShape.VeloBeam1Shape.YsigmaUnfold', 'LHC:LHCCOM/LHC.LHCb.Internal.VELO.VeloBeamShape.VeloBeam1Shape.YsigmaUnfoldErr']
dpsLPC_VeloBeam2Gas =  ['LHC:LHCCOM/LHC.LHCb.Internal.VELO.VeloBeamShape.VeloBeam2Shape.Xmean', 'LHC:LHCCOM/LHC.LHCb.Internal.VELO.VeloBeamShape.VeloBeam2Shape.XmeanErr', 'LHC:LHCCOM/LHC.LHCb.Internal.VELO.VeloBeamShape.VeloBeam2Shape.Ymean', 'LHC:LHCCOM/LHC.LHCb.Internal.VELO.VeloBeamShape.VeloBeam2Shape.YmeanErr', 'LHC:LHCCOM/LHC.LHCb.Internal.VELO.VeloBeamShape.VeloBeam2Shape.Xslope', 'LHC:LHCCOM/LHC.LHCb.Internal.VELO.VeloBeamShape.VeloBeam2Shape.XslopeErr', 'LHC:LHCCOM/LHC.LHCb.Internal.VELO.VeloBeamShape.VeloBeam2Shape.Yslope', 'LHC:LHCCOM/LHC.LHCb.Internal.VELO.VeloBeamShape.VeloBeam2Shape.YslopeErr', 'LHC:LHCCOM/LHC.LHCb.Internal.VELO.VeloBeamShape.VeloBeam2Shape.XsigmaUnfold', 'LHC:LHCCOM/LHC.LHCb.Internal.VELO.VeloBeamShape.VeloBeam2Shape.XsigmaUnfoldErr', 'LHC:LHCCOM/LHC.LHCb.Internal.VELO.VeloBeamShape.VeloBeam2Shape.YsigmaUnfold', 'LHC:LHCCOM/LHC.LHCb.Internal.VELO.VeloBeamShape.VeloBeam2Shape.YsigmaUnfoldErr']
dpsBKG = ['LHC:BLS/bls01.Parameter.Readings.DIP.RunningSums', 'LHC:BLS/bls02.Parameter.Readings.DIP.RunningSums', 'BCM:BCM_DP_S0.RS2_SUM.fluxrel', 'BCM:BCM_DP_S1.RS2_SUM.fluxrel', 'LHC:LHCCOM/LHC.LHCb.Internal.Intensity.Beam1.DCBCTtotalIntensity', 'LHC:LHCCOM/LHC.LHCb.Internal.Intensity.Beam2.DCBCTtotalIntensity', 'LHC:BLS/bls09.Parameter.Readings.Intensity.BX01_TRIGGER_RATE_INST', 'LHC:BLS/bls09.Parameter.Readings.Intensity.BX10_TRIGGER_RATE_INST', 'LHC:BLS/bls09.Parameter.Readings.Intensity.BX00_TRIGGER_RATE_INST']
dpsRates = ['LHC:LHCCOM/LHC.LHCb.Internal.TriggerRates.TrgRate_L0', 'LHC:LHCCOM/LHC.LHCb.Internal.TriggerRates.TrgRate_calo_bb', 'ECS:LHCb_RunInfoCond.Operation.Instant.HLTPhysRate', 'LHC:LHCCOM/LHC.LHCb.Internal.Efficiencies.TriggerLivetime_Lumi', 'LHC:LHCCOM/LHC.LHCb.Internal.RunNumber']
dpsBeam = ['LHC:BPIM/bpim01.Parameter.Readings.DIP.Timing.Phase_zero', 'LHC:BPIM/bpim01.Parameter.Readings.DIP.Timing.deltaT', 'LHC:LHCCOM/LHC.LHCb.Internal.VELO.VeloLumiRegionPos.sxUnfold', 'LHC:LHCCOM/LHC.LHCb.Internal.VELO.VeloLumiRegionPos.syUnfold', 'LHC:LHCCOM/LHC.LHCb.Internal.VELO.VeloLumiRegionPos.szUnfold', 'LHC:LHCCOM/LHC.LHCb.Internal.VELO.VeloLumiRegionPos.x', 'LHC:LHCCOM/LHC.LHCb.Internal.VELO.VeloLumiRegionPos.y', 'LHC:LHCCOM/LHC.LHCb.Internal.VELO.VeloLumiRegionPos.z', 'LHC:LHCCOM/LHC.LHCb.Internal.Timing.OTTrend']
dpsLumi = ['ECS:LHCbEfficiency.ComponentsLumi.LHC', 'ECS:LHCbEfficiency.ComponentsLumi.DAQLiveTime', 'LHC:LHCCOM/LHC.LHCb.Internal.Luminosity.LumiInst_GP', 'LHC:LHCCOM/LHC.LHCb.Internal.TriggerRates.TrgRateLumi_GP', 'LHC:LHCCOM/LHC.LHCb.Internal.Luminosity.LumiInst_BRAN_4L8', 'LHC:LHCCOM/LHC.LHCb.Internal.Luminosity.LumiInst_BRAN_4R8', 'LHC:LHCCOM/LHC.LHCb.Internal.Luminosity.LumiInst_BLS_Cside', 'LHC:LHCCOM/LHC.LHCb.Internal.Luminosity.LumiInst_BLS_Aside', 'LHC:LHCCOM/LHC.LHCb.Internal.Luminosity.LumiSpec_GP', 'LHC:LHCCOM/LHC.LHCb.Internal.Luminosity.PileUp', 'LHC:LHCCOM/LHC.LHCb.Internal.Luminosity.Mu']
dpsEff = ['LHC:LHCCOM/LHC.LHCb.Internal.Efficiencies.TimeTotal', 'LHC:LHCCOM/LHC.LHCb.Internal.Efficiencies.ResultsTime.HV', 'LHC:LHCCOM/LHC.LHCb.Internal.Efficiencies.ResultsTime.VELO', 'LHC:LHCCOM/LHC.LHCb.Internal.Efficiencies.ResultsTime.DAQ', 'LHC:LHCCOM/LHC.LHCb.Internal.Efficiencies.ResultsTime.DAQLiveTime', 'LHC:LHCCOM/LHC.LHCb.Internal.Efficiencies.LumiTotal', 'LHC:LHCCOM/LHC.LHCb.Internal.Efficiencies.ResultsLumi.HV', 'LHC:LHCCOM/LHC.LHCb.Internal.Efficiencies.ResultsLumi.VELO', 'LHC:LHCCOM/LHC.LHCb.Internal.Efficiencies.ResultsLumi.DAQ', 'LHC:LHCCOM/LHC.LHCb.Internal.Efficiencies.ResultsLumi.DAQLiveTime']

runI_start = datetime(2011,03,12,00)
runI_end = datetime(2013,02,15,00) 
local = pytz.timezone('Europe/Amsterdam')

data = {}
fig = []
ax = []
dict_fill = {}
dict_interval = {}
dpPatterns = []

def utc_mktime(utc_tuple):
    if len(utc_tuple) == 6:
        utc_type += (0,0,0)
    #account for hourly time change (to be understood)
    return (time.mktime(utc_tuple) - time.mktime((1970, 1, 1, 0, 0, 0, 0, 0, 0))) - (time.mktime((1970, 1, 1, 1, 0, 0, 0, 0, 0)) - time.mktime((1970, 1, 1, 0, 0, 0, 0, 0, 0)))

def mk_json(index, dp, json_name, myShelve):
    dict_json = {}
    dict_json['values'] = myShelve[index+'/'+dp+'/values']
    dict_json['uncertainties'] = ["",""]
    dict_json['binning'] = ["",""]
    splittitle = dp.split('.')
    title = splittitle[len(splittitle)-2] + "/" + splittitle[len(splittitle)-1]
    dict_json['axis_title'] = [title,"Population"]
                               
    with open(json_name, 'w') as f:
        json.dump(dict_json, f)

def print_trend(index, dps, name):
    myShelve = shelve.open(name)
    index_col = int(math.ceil(math.sqrt(len(dps))))
    index_row = int(math.sqrt(len(dps)))
    splittitle = []
    f1 = plt.figure()
    i = 0
    for dp in dps:
        try:
            ax1 = f1.add_subplot(index_col, index_row, i+1)
            ax1.plot(myShelve[str(index)+'/'+dp+'/offset_time'], myShelve[str(index)+'/'+dp+'/values'])   
            splittitle = dp.split('.')
            title = splittitle[len(splittitle)-2] + "/" + splittitle[len(splittitle)-1]
            ax1.set_title(title)
            ax1.set_ylabel('Values')
            if 'PHYSICS' in myShelve[str(index)]:
                ax1.axvline(0, color='r', linestyle='--')
                ax1.set_xlabel('Time since Stable Beams (h)')
            else:
                ax1.set_xlabel('Time since beginning of run (min)')
            i += 1    
        except:
            print dp + " has no values for trending."
            
    myShelve.close()

def print_histo(index, dps, name):
    myShelve = shelve.open(name)
    index_col = int(math.ceil(math.sqrt(len(dps))))
    index_row = int(math.sqrt(len(dps)))
    f2 = plt.figure()
    i = 0
    for dp in dps:
        try:
            ax2 = f2.add_subplot((index_col*100)+(index_row*10)+(i+1))
            ax2.hist(myShelve[str(index)+'/'+dp+'/values'], bins=100)
            splittitle = dp.split('.')
            title = splittitle[len(splittitle)-2] + "/" + splittitle[len(splittitle)-1]
            ax2.set_title(title)
            i += 1
        except:
            print dp + " has no values for histogramming."
    myShelve.close()

def mkscatterplt(time1, data1, time2, data2, interval):
    val1 = []
    val2 = []
    if len(data1) == len(data2):
        for i in range(len(data1)):
            val1.append(data1[i])
            val2.append(data2[i])
    else:
        for i in range(len(data1)):
            for j in range(len(data2)):
                if (time1[i] - time2[j] > -interval) and (time1[i] - time2[j] < interval):
                    val1.append(data1[i])
                    val2.append(data2[j])
    
    return val1, val2

def print_scatter(index, dps, name):
    myShelve = shelve.open(name)
    index_col = int(math.ceil(math.sqrt(len(dps)/2)))
    index_row = int(math.sqrt(len(dps)/2))
    f3 = plt.figure()
    scatter_datax = []
    scatter_datay = []
    for i in range(len(dps)/2):
        try:
            ax3 = f3.add_subplot((index_col*100)+(index_row*10)+(i+1))
            scatter_datax, scatter_datay = mkscatterplt(myShelve[str(index)+'/'+dps[2*i]+'/utc_time'], myShelve[str(index)+'/'+dps[2*i]+'/values'], myShelve[str(index)+'/'+dps[2*i+1]+'/utc_time'], myShelve[str(index)+'/'+dps[2*i+1]+'/values'], 3)
            ax3.scatter(scatter_datax, scatter_datay)
            splittitle = dps[2*i].split('.') + dps[2*i+1].split('.')
            title_x = splittitle[len(splittitle)/2-2] + "/" + splittitle[len(splittitle)/2-1]
            title_y = splittitle[len(splittitle)-2] + "/" + splittitle[len(splittitle)-1]
            ax3.set_title(title_y + " vs. " + title_x)
            ax3.set_xlabel(title_x)
            ax3.set_ylabel(title_y)
        except:
            print dps[2*i] + " or " + dps[2*i+1] + " have no values for plotting."
    myShelve.close()

def write_to_file(index, dps, data_file):
    for dp in dps:
        filetitle = dp.replace(".", "_")
        out_file = open(filetitle+".txt","w")
        
    
def createdictionary_singleFill(dps, fillnumber):
    #Get fillnumbers and states per fillnumber
    fillnumbers = getWinCCData(dpFillNumbers, runI_start, runI_end)
    #Nested dictionaries for fill number
    if fillnumbers:
        for row in fillnumbers:
            dict_fill[int(row[2])] = {"start":row[1][:-7]}
            if int(row[2]) == fillnumber + 1:
                states = getWinCCData(dpStates, dict_fill[row[2]-1]['start'], dict_fill[row[2]]['start'])                
                if states:
                    for states_row in states:
                        dict_fill[row[2]-1][states_row[2]] = states_row[1][:-7]
                    #if states are present, get all values for that fill
                    values = getWinCCData(dps, dict_fill[row[2]-1]['start'], dict_fill[row[2]]['start'])
                    if values:
                        print "Retrieving %d datapoints." % len(dps)
                        for values_row in values:
                            if not values_row[0] in dict_fill[row[2]-1]: 
                            #Initialize empty dictionaries and list if not yet done for that dp
                                dict_fill[row[2]-1][values_row[0]] = {}
                                dict_fill[row[2]-1][values_row[0]]['utc_time'] = []
                                dict_fill[row[2]-1][values_row[0]]['offset_time'] = []
                                dict_fill[row[2]-1][values_row[0]]['values'] = []

                                #Different ways to generate times -- for the record
                                #print dates.date2num(datetime.strptime(values_row[1][:-7], '%Y-%m-%d %H:%M:%S')) -- Python generic time
                                #print int(utc_mktime( (datetime.strptime(values_row[1][:-7], '%Y-%m-%d %H:%M:%S')).timetuple() ))) -- UTC time
                                #local_dt = local.localize(((datetime.strptime(values_row[1][:-7], '%Y-%m-%d %H:%M:%S'))), is_dst = None)
                                #print local_dt.astimezone(pytz.utc) -- Local time

                            #Store UTC time
                            utc_time = int(utc_mktime( (datetime.strptime(values_row[1][:-7], '%Y-%m-%d %H:%M:%S')).timetuple() ))
                            dict_fill[row[2]-1][values_row[0]]['utc_time'].append(utc_time)
                            #Store time elapsed since STABLE BEAMS declaration (in s, positive if after SB, negative if before)
                            if 'PHYSICS' in  dict_fill[row[2]-1]:
                                init_time = int(utc_mktime( (datetime.strptime(dict_fill[row[2]-1]['physics'], '%Y-%m-%d %H:%M:%S')).timetuple() ))
                            else:
                                init_time = int(utc_mktime( (datetime.strptime(dict_fill[row[2]-1]['start'], '%Y-%m-%d %H:%M:%S')).timetuple() ))
                            sb_time = (utc_time - init_time) / (60.0*60.0)
                            dict_fill[row[2]-1][values_row[0]]['offset_time'].append(sb_time)
                            #Store value at that time
                            dict_fill[row[2]-1][values_row[0]]['values'].append(values_row[2])
                    
                    #Add list of RunNumber        
                    runnumbers = getWinCCData(dpRunNumbers, dict_fill[row[2]-1]['start'], dict_fill[row[2]]['start'])
                    
                    if runnumbers:
                        for runnumbers_row in runnumbers:
                            if not dpRunNumbers in dict_fill[row[2]-1]:
                                dict_fill[row[2]-1][dpRunNumbers] = {}
                                dict_fill[row[2]-1][dpRunNumbers]['utc_time'] = []
                                dict_fill[row[2]-1][dpRunNumbers]['offset_time'] = []
                                dict_fill[row[2]-1][dpRunNumbers]['values'] = []

                            #Store UTC time
                            utc_time = int(utc_mktime( (datetime.strptime(runnumbers_row[1][:-7], '%Y-%m-%d %H:%M:%S')).timetuple() ))
                            dict_fill[row[2]-1][dpRunNumbers]['utc_time'].append(utc_time)
                            #Store time elapsed since STABLE BEAMS declaration (in s)
                            if 'PHYSICS' in  dict_fill[row[2]-1]:
                                init_time = int(utc_mktime( (datetime.strptime(dict_fill[row[2]-1]['physics'], '%Y-%m-%d %H:%M:%S')).timetuple() ))
                                sb_time = (utc_time - init_time) / (60.0*60.0)
                            else:
                                init_time = int(utc_mktime( (datetime.strptime(dict_fill[row[2]-1]['start'], '%Y-%m-%d %H:%M:%S')).timetuple() ))
                                sb_time = (utc_time - init_time) / (60.0)
                            dict_fill[row[2]-1][dpRunNumbers]['offset_time'].append(sb_time)
                            #Store values at those times
                            dict_fill[row[2]-1][dpRunNumbers]['values'].append(runnumbers_row[2])

    #After massage, change fill numbers key from int(s) to str for usage in shelve
    for k in dict_fill.keys():
        dict_fill[str(k)] = dict_fill.pop(k)
    return dict_fill

def createdictionary_singleRun(dps, runnumber, dict_run):
    #Create the key for that runnumber if not already there, if not, don't
    if str(runnumber) not in dict_run:
        print "Updating Run Numbers"
        #Get fillnumbers and states per fillnumber
        runnumbers = getWinCCData(dpRunNumbers, runI_start, runI_end)
        #Nested dictionaries for fill number
        if runnumbers:
            for row in runnumbers:
                str_key_curr = str(int(row[2]))
                if str_key_curr not in dict_run:
                    dict_run[str_key_curr] = {"start":row[1][:-7]}
    else:
        print "No need to update Run Numbers"
    
    #Fill up the values for that key 
    str_key_curr = str(runnumber)
    str_key_next = str(runnumber+1)
    if str_key_curr and str_key_next in dict_run:
        values = getWinCCData(dps, dict_run[str_key_curr]['start'], dict_run[str_key_next]['start'])
        if values:
            print "Retrieving %d datapoints" % len(dps)
            dict_json = {}
            utc_time_list = []
            run_time_list = []
            values_list = []
            prev_dp = values[0][0]
            for values_row in values:
                if prev_dp != values_row[0]:
                    #Write list in shelve if dp changes
                    dict_run[str_key_curr+'/'+prev_dp+'/utc_time'] = utc_time_list
                    dict_run[str_key_curr+'/'+prev_dp+'/offset_time'] = run_time_list
                    dict_run[str_key_curr+'/'+prev_dp+'/values'] = values_list
                    dict_run[str_key_curr+'/'+prev_dp+'/uncertainties'] = []
                    dict_run[str_key_curr+'/'+prev_dp+'/binning'] = []
                    dict_run[str_key_curr+'/'+prev_dp+'/axis_title'] = prev_dp
                    utc_time_list = []
                    run_time_list = []
                    values_list = []
                #Store UTC time (to understand the one hour correction)
                utc_time = int(utc_mktime( (datetime.strptime(values_row[1][:-7], '%Y-%m-%d %H:%M:%S')).timetuple() ))
                utc_time_list.append(utc_time)
                #Store time elapsed since beginning of run (in s)
                init_time = int(utc_mktime( (datetime.strptime(dict_run[str_key_curr]['start'], '%Y-%m-%d %H:%M:%S')).timetuple() ))
                run_time = (utc_time - init_time)/(60.0)
                run_time_list.append(run_time)
                #Store values at those times
                values_list.append(values_row[2])
                prev_dp = values_row[0]

            #Write last list in shelve
            dict_run[str_key_curr+'/'+prev_dp+'/utc_time'] = utc_time_list
            dict_run[str_key_curr+'/'+prev_dp+'/offset_time'] = run_time_list
            dict_run[str_key_curr+'/'+prev_dp+'/values'] = values_list
            dict_run[str_key_curr+'/'+prev_dp+'/uncertainties'] = []
            dict_run[str_key_curr+'/'+prev_dp+'/binning'] = []
            dict_run[str_key_curr+'/'+prev_dp+'/axis_title'] = prev_dp 
    else:
        print "For some reason, run numbers are not present in dictionary"

    return dict_run

def createdictionary_timeinterval(dps, start_time, stop_time):
    values = getWinCCData(dps, start_time, stop_time)
    if values:
        dict_interval['interval'] = {"start":start_time}
        states = getWinCCData(dpStates, start_time, stop_time)
        if states:
            for states_row in states:
                dict_interval['interval'][states_row[2]] = states_row[1][:-7]
        print "Retrieving %d datapoints." % len(dps)
        for values_row in values:
            if not values_row[0] in dict_interval['interval']:
                #Initialize empty dictionaries and listst
                dict_interval['interval'][values_row[0]] = {}
                dict_interval['interval'][values_row[0]]['utc_time'] = []
                dict_interval['interval'][values_row[0]]['offset_time'] = []
                dict_interval['interval'][values_row[0]]['values'] = []
                
            #Store UTC time (to understand the one hour correction)
            utc_time = int(utc_mktime( (datetime.strptime(values_row[1][:-7], '%Y-%m-%d %H:%M:%S')).timetuple() ))
            dict_interval['interval'][values_row[0]]['utc_time'].append(utc_time)
            #Store time elapsed since beginning of run (in s)
            if 'PHYSICS' in dict_interval['interval']:
                init_time = int(utc_mktime( (datetime.strptime(dict_interval['interval']['physics'], '%Y-%m-%d %H:%M:%S')).timetuple() ))
                sb_time = (utc_time - init_time) / (60.0*60.0)
            else:
                init_time = int(utc_mktime( start_time.timetuple() ))
                sb_time = (utc_time - init_time) / (60.0)
            dict_interval['interval'][values_row[0]]['offset_time'].append(sb_time)
            #Store values at those times
            dict_interval['interval'][values_row[0]]['values'].append(values_row[2])

    return dict_interval

#This is the main of the script
#Massage python arguments
cmdargs = str(sys.argv)
if '-help' in cmdargs:
    print "-----------------------------------------------------------------------------------------------------"
    print "This is a Python script to retrieve data from the OracleDB archive. It is meant to generate a Python dictionary with few selected datapoints organized either per fill or per run."
    print "Below is a description of the arguments and a set of options to be chosen from:"
    print "Main arguments:"
    print "     -f followed by (int)<<fill number>>"
    print "     -r followed by (int)<<run number>>"
    print "     -i followed by start and stop time in this form YYYY,MM,DD,HH,MM/YYYY,MM,DD,HH,MM"
    print "Main options can be:"
    print "     -L for LPC files and datapoints"
    print "     -S for generic summary datapoints connecting to running conditions"
    print "     -E for a list of datapoints stored in an external file followed by the list separate by a comma with no additional spaces"
    print "     -T for a generic set of datapoints for test"
    print "Final options are:"
    print "     -trend for trending"
    print "     -histo for histogramming"
    print "     -scatter for scatter plot"
    print "     -file for writing to file"
    print "-----------------------------------------------------------------------------------------------------"
    print "The script is under continuous development. Contact federico.alessio@cern.ch for any questions/suggestions."
else:
    start_script = time.time()

    arg1, arg2, arg3, arg4, arg5 = cmdargs.split(", ")
    arg1 = arg1.strip("'")
    arg2 = arg2.strip("'")
    arg3 = arg3.strip("'")
    arg4 = arg4.strip("'")
    arg5 = arg5.strip("'").strip("']")
    
    #Choose what kind of summary to make
    if arg4 == '-L':
        dpPatterns = dpsLPC + dpsLPC_VeloLumi + dpsLPC_VeloBeam1Gas + dpsLPC_VeloBeam2Gas
    elif arg4 == '-S':
        dpPatterns = dpsBKG + dpsLumi + dpsRates + dpsBeam + dpsEff
    elif arg4 == '-T':
        dpPatterns = dpsLPC
    elif '-E' in arg4:
        arg4 = arg4.strip("-E")
        dpPatterns = arg4.split(',')

    #According to argument, call function
    if arg2 == '-f' or arg2 == '-r':
        arg3 = int(arg3)
        if arg2 == '-f':
            dict_name = 'dict_fill'
        elif arg2 == '-r':
            dict_name = 'dict_run'

        #Get dictionary and modify if needed    
        myShelve = shelve.open(dict_name, writeback = True)        
        if str(arg3) not in myShelve.keys() or (str(arg3)+'/'+dpPatterns[0]+'/values') not in myShelve.keys():
            print "Data not cached yet"
            if arg2 == '-f':
                data = createdictionary_singleFill(dpPatterns, arg3, myShelve)
            elif arg2 == '-r':
                data = createdictionary_singleRun(dpPatterns, arg3, myShelve)
            myShelve.update(data)
        else:
            print "Data already cached"
    
        i = 0
        for dp in dpPatterns:
            mk_json(str(arg3), dp, 'histogram_'+str(i)+'.json', myShelve)
            i += 1
        myShelve.close()

    elif arg2 == '-i':
        arg3_a, arg3_b = arg3.split("/")
        arg3_a = arg3_a.split(",")
        start = datetime(int(arg3_a[0]), int(arg3_a[1]), int(arg3_a[2]), int(arg3_a[3]), int(arg3_a[4]))
        arg3_b = arg3_b.split(",")
        stop = datetime(int(arg3_b[0]), int(arg3_b[1]), int(arg3_b[2]), int(arg3_b[3]), int(arg3_b[4]))
        data = createdictionary_timeinterval(dpPatterns, start, stop)
        #Change arg3 for the graphical part
        arg3 = 'interval'
    
    #Graphical part
    if arg5 == '-trend':
        print_trend(arg3, dpPatterns, dict_name) 
    elif arg5 == '-histo':
        print_histo(arg3, dpPatterns, dict_name)
    elif arg5 == '-scatter':
        print_scatter(arg3, dpPatterns, dict_name)
    else:
        print "No graphic requested"

    end_script = time.time()
    print "Script took %3.2f s to complete." % (end_script - start_script)

    #Show everything
    plt.show()

#Write file
#filename = "/group/online/tfc/Python/%d_lumi_LHCb.txt" % arg2
#out_file = open(filename, "w")
#for i in range(len(data[arg2][dpPatterns[0]]['values'])):
#    line = "%d 1 %4.6f %4.6f 0.0 0.0\n" % (data[arg2][dpPatterns[0]]['utc_time'][i], data[arg2][dpPatterns[0]]['values'][i], (data[arg2][dpPatterns[0]]['values'][i])/100.0*5.0)
#    out_file.write(line)
#out_file.close()
