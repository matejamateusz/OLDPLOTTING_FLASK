#!/usr/bin/python

from oracle_wincc import getWinCCData
from datetime import datetime

dpPatterns = ['%OTDCSGASMON:Input_gas.Fit_spectra%', '%VTCS_PA_%', 'doesnotexist', '%HRCMATN01%Channel2%']
#dpPatterns = 'somedp'
ti = datetime(2015,03,23,17)
tf = '2015-03-23 17:15:00'
data = getWinCCData(dpPatterns, ti, tf)
if data:
    for row in data:
        print row
