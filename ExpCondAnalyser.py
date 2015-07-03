#!/usr/bin/python
from __future__ import division
import sys
import shelve
import time
#from matplotlib import pyplot as plt
from oracle_wincc import getWinCCData
from oracle_rundb3 import getRunDBData
from datetime import datetime

from createDicts import *
from genericsmk import *
#from genericsprint import *

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

data = {}
dpPatterns = []
        
#This is the main of the script
#Massage python arguments
if '-help' in sys.argv:
    print '-----------------------------------------------------------------------------------------------------'
    print 'This is a Python script to retrieve data from the OracleDB archive. It is meant to generate a Python dictionary with few selected datapoints organized either per fill or per run.'
    print 'Below is a description of the arguments and a set of options to be chosen from:'
    print 'Main arguments:'
    print '     -f followed by (int)<<fill number>>'
    print '     -r followed by (int)<<run number>>'
    print '     -i followed by start and stop time in this form YYYY,MM,DD,HH,MM/YYYY,MM,DD,HH,MM'
    print '     -frange followed by (int)<<initial fill number>>/(int)<<final fill number>>'
    print '     -rrange followed by (int)<<initial run number>>/(int)<<final run number>>'
    print 'Main options can be:'
    print '     -L for LPC files and datapoints'
    print '     -S for generic summary datapoints connecting to running conditions'
    print '     -E for a list of datapoints stored in an external file followed by the list separate by a comma with no additional spaces'
    print '     -T for a generic set of datapoints for test'
    print 'Final options are:'
    print '     -trend for trending'
    print '     -histo for histogramming'
    print '     -scatter for scatter plot'
    print '     -file for writing to file'
    print '     -LPC for generating files for LPC'
    print '-----------------------------------------------------------------------------------------------------'
    print 'The script is under continuous development. Contact federico.alessio@cern.ch for any questions/suggestions.'
else:
    start_script = time.time()

    arg1, arg2, arg3, arg4, arg5 = sys.argv

    #Choose what kind of summary to make
    if arg4 == '-L':
        dpPatterns = dpsLPC + dpsLPC_VeloLumi + dpsLPC_VeloBeam1Gas + dpsLPC_VeloBeam2Gas
    elif arg4 == '-S':
        dpPatterns = dpsBKG + dpsLumi + dpsRates + dpsBeam + dpsEff
    elif arg4 == '-T':
        dpPatterns = dpsLPC
    elif '-E' in arg4:
        arg4 = arg4.strip('-E')
        dpPatterns = arg4.split(',')

    #Choose corresponding dictionary
    if arg2 == '-f' or arg2 == '-frange':
        dict_name = 'dictionaries/dict_fill'
        graph_arg2 = dpPatterns
    elif arg2 == '-r' or agr2 == '-rrange':
        dict_name = 'dictionaries/dict_run'
        graph_arg2 = dpPatterns
    elif arg2 == '-i':
        dict_name = 'dictionaries/dict_interval'
        graph_arg2 = (dpPatterns, start, stop)

    #Get the dictionary which is already cached somewhere
    myShelve = shelve.open(dict_name, writeback = True) 
    
    #According to argument, call function
    if arg2 == '-f' or arg2 == '-r':
        #Get dictionary and modify if needed
        dpPatterns_tuples = []
        #
        for dps in dpPatterns:
            dpPatterns_tuples.append((dps,'values'))
        #
        if arg3 in myShelve.keys() and all(dpkeys in myShelve[arg3].keys() for dpkeys in dpPatterns_tuples):
            print 'Data already cached'
        else:
            print 'Data not cached yet'
            if arg2 == '-f':
                data = createdictionary_singleFill(dpPatterns, int(arg3), myShelve)
            elif arg2 == '-r':
                dataRunDB = getRunDBData('rundbrunparams', int(arg3))
                myShelve.update(dataRunDB)
                data = createdictionary_singleRun(dpPatterns, int(arg3), myShelve)
            myShelve.update(data)
    elif arg2 == '-i':
        arg3_a, arg3_b = arg3.split('/')
        arg3 = 'interval'
        start_times = map(int, arg3_a.split('/'))
        start = datetime(start_times[0], start_times[1], start_times[2], start_times[3], start_times[4])
        stop_times = map(int, arg3_b.split(','))
        stop = datetime(stop_times[0], stop_times[1], stop_times[2], stop_times[3], stop_times[4])
        if arg3 not in myShelve.keys() or (dpPatterns[0], start, stop, 'values') not in myShelve[arg3].keys():
            print 'Data not cached yet'
            data = createdictionary_timeinterval(dpPatterns, start, stop, myShelve)
            myShelve.update(data)
        else:
            print 'Data already cached'

    #Make the json for the presenter
    i = 0
    for dp in dpPatterns:
        if arg2 == '-i-':
            if (dp, start, stop, 'values') in myShelve[arg3].keys():
                mkjson(str(arg3), 'json_files/datahistogram'+arg2+str(i)+'.json', myShelve, dp, start, stop)
                i += 1
        else:
            if (dp, 'values') in myShelve[arg3].keys():
                mkjson(str(arg3), 'json_files/datahistogram'+arg2+str(i)+'.json', myShelve, dp)
                i += 1
    
    myShelve.close()

    #Graphical part
    if '-trend' in arg5:
        print_trend(arg3, graph_arg2, dict_name) 
    if '-histo' in arg5:
        print_histo(arg3, graph_arg2, dict_name) 
    if '-scatter' in arg5:
        print_scatter(arg3, graph_arg2, dict_name) 
    if '-file' in arg5:
        print_file(arg3, graph_arg2, dict_name) 
     
    #if '-LPC' in arg5:
    #    if arg2 == '-i':
            #print_file_LPC(arg3, (start, stop, dpPatterns), dict_name) 
    #    else:
            #print_file_LPC(arg3, dpPatterns, dict_name) 
    #else:
    #    print 'No graphic requested'

    end_script = time.time()
   # print 'Script took %3.2f s to complete.' % (end_script - start_script)
    
    if '-trend' or '-histo' or '-scatter' in arg5:
        #Show everything
        #plt.show()
        pass
