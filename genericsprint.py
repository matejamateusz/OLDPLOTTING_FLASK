#!/usr/bin/python
from __future__ import division
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

from genericsmk import *

def print_trend(index, dpss, name):
    """Print a trend plot by loading a shelve from disk and plotting specific datapoints and data"""
    """Needs an index, datapoints names and the name of the shelve"""
    myShelve = shelve.open(name)
    
    if index == 'interval':
        dps = dpss[2]
    else:
        dps = dpss

    index_col = int(math.ceil(math.sqrt(len(dps))))
    index_row = int(math.sqrt(len(dps)))
    splittitle = []
    f1 = plt.figure()
    i = 0
    
    for dp in dps:
        try:
            ax1 = f1.add_subplot(index_col, index_row, i+1)
            if index == 'interval':
                ax1.plot(myShelve[str(index)][(dpss[0], dpss[1], dp, 'offset_time')], myShelve[str(index)][(dpss[0], dpss[1], dp, 'values')])   
                if (dpss[0], dpss[1], 'physics') in myShelve[str(index)].keys():
                    ax1.axvline(0, color='r', linestyle='--')
                    ax1.set_xlabel('Time since Stable Beams (h)')
                else:
                    ax1.set_xlabel('Time since beginning of run (min)')
            else:
                ax1.plot(myShelve[str(index)][(dp,'offset_time')], myShelve[str(index)][(dp,'values')])   
                if 'physics' in myShelve[str(index)].keys():
                    ax1.axvline(0, color='r', linestyle='--')
                    ax1.set_xlabel('Time since Stable Beams (h)')
                else:
                    ax1.set_xlabel('Time since beginning of run (min)')

            splittitle = dp.split('.')
            title = splittitle[len(splittitle)-2] + '/' + splittitle[len(splittitle)-1]
            ax1.set_title(title)
            ax1.set_ylabel('Values')
            
            i += 1    
        except:
            print dp + ' has no values for trending.'
            
    myShelve.close()

def print_histo(index, dpss, name):
    """Print an histogram by loading a shelve from disk and plotting specific datapoints and data"""
    """Needs an index, datapoints names and the name of the shelve"""
    myShelve = shelve.open(name)
    
    if index == 'interval':
        dps = dpss[2]
    else:
        dps = dpss

    index_col = int(math.ceil(math.sqrt(len(dps))))
    index_row = int(math.sqrt(len(dps)))
    f2 = plt.figure()
    i = 0
    
    for dp in dps:
        try:
            ax2 = f2.add_subplot((index_col*100)+(index_row*10)+(i+1))
            if index == 'interval':
                ax2.hist(myShelve[str(index)][(dpss[0], dpss[1], dp, 'values')], bins=100)
            else:
                ax2.hist(myShelve[str(index)][(dp,'values')], bins=100)
            
            splittitle = dp.split('.')
            title = splittitle[len(splittitle)-2] + '/' + splittitle[len(splittitle)-1]
            ax2.set_title(title)
            i += 1
        except:
            print dp + ' has no values for histogramming.'
    myShelve.close()

def print_scatter(index, dpss, name):
    myShelve = shelve.open(name)

    if index == 'interval':
        dps = dpss[2]
    else:
        dps = dpss

    index_col = int(math.ceil(math.sqrt(len(dps)/2)))
    index_row = int(math.sqrt(len(dps)/2))
    f3 = plt.figure()
    scatter_datax = []
    scatter_datay = []

    for i in range(len(dps)/2):
        try:
            ax3 = f3.add_subplot((index_col*100)+(index_row*10)+(i+1))
            if index == 'interval':
                scatter_datax, scatter_datay = mkscatterplt(myShelve[str(index)][(dpss[0], dpss[1], dps[2*i], 'utc_time')], myShelve[str(index)][(dpss[0], dpss[1], dps[2*i], 'values')], myShelve[str(index)][(dpss[0], dpss[1], dps[2*i+1],'utc_time')], myShelve[str(index)][(dpss[0], dpss[1], dps[2*i+1],'values')], 3)
            else:
                scatter_datax, scatter_datay = mkscatterplt(myShelve[str(index)][(dps[2*i],'utc_time')], myShelve[str(index)][(dps[2*i],'values')], myShelve[str(index)][(dps[2*i+1],'utc_time')], myShelve[str(index)][(dps[2*i+1],'values')], 3)
            ax3.scatter(scatter_datax, scatter_datay)
            splittitle = dps[2*i].split('.') + dps[2*i+1].split('.')
            title_x = splittitle[len(splittitle)/2-2] + '/' + splittitle[len(splittitle)/2-1]
            title_y = splittitle[len(splittitle)-2] + '/' + splittitle[len(splittitle)-1]
            ax3.set_title(title_y + ' vs. ' + title_x)
            ax3.set_xlabel(title_x)
            ax3.set_ylabel(title_y)
        except:
            print dps[2*i] + ' or ' + dps[2*i+1] + ' have no values for plotting.'
    myShelve.close()

def print_file(index, dpss, name):
    myShelve = shelve.open(name)

    if index == 'interval':
        dps = dpss[2]
    else:
        dps = dpss

    for dp in dps:
        splittitle = dp.split('.')
        filetitle = str(index) + '_' + splittitle[len(splittitle)-2] + '_' + splittitle[len(splittitle)-1]
        with open('output_files/'+filetitle+'.txt','w') as output_file:
            if index == 'interval':
                for i in range(len(myShelve[str(index)][(dpss[0], dpss[1], dp, 'values')])):
                    line = '%d %4.6f\n' % (myShelve[str(index)][(dpss[0], dpss[1], dp, 'utc_time')][i], myShelve[str(index)][(dpss[0], dpss[1], dp, 'values')][i])
                    output_file.write(line)        
            else:
                for i in range(len(myShelve[str(index)][(dp, 'values')])):
                    line = '%d %4.6f\n' % (myShelve[str(index)][(dp, 'utc_time')][i], myShelve[str(index)][(dp, 'values')][i])
                    output_file.write(line)
    myShelve.close()

#Write file
#filename = '/group/online/tfc/Python/%d_lumi_LHCb.txt' % arg2
#output_file = open(filename, 'w')
#for i in range(len(data[arg2][dpPatterns[0]]['values'])):
#    line = '%d 1 %4.6f %4.6f 0.0 0.0\n' % (data[arg2][dpPatterns[0]]['utc_time'][i], data[arg2][dpPatterns[0]]['values'][i], (data[arg2][dpPatterns[0]]['values'][i])/100.0*5.0)
#    output_file.write(line)
#output_file.close()
