#!/usr/bin/python

import os
import cx_Oracle
import csv
 
# Network drive somewhere
#filename="S:\Output.csv"
#FILE=open(filename,"w");
#output=csv.writer(FILE, dialect='excel')
 
# You can set these in system variables but just in case you didnt
#os.putenv('ORACLE_HOME', '/oracle/product/10.2.0/db_1') 
#os.putenv('LD_LIBRARY_PATH', '/oracle/product/10.2.0/db_1/lib') 
def getRunDBData(rundb_type, identifier):
    connection = cx_Oracle.connect('rundb_admin', 'aDm1n', 'LHCBONR_RUNDB')
    cursor = connection.cursor()
    #out_cursor = connection.cursor()
    #out_cursor = cursor.var(cx_Oracle.CURSOR)
    #bindVarList = {'cur':out_cursor,'dp':'%LHC%IntLumi%', 'ti':'2011-03-25 11:00:00', 'tf':'2011-03-29 11:00:00'}
    #bindVarList = {'cur':out_cursor,'dp':'LHC:LHCCOM/LHC.LHCb.FillLumi.IntLumi_Delivered_StableBeams', 'ti':'2010-10-28 02:00:00', 'tf':'2010-10-28 11:00:00'}

    #dataRunDB = getRunDBData('rundbruns', int(arg3))
    #print dataRunDB
    #dataRunDB = getRunDBData('rundbfillparams', int(arg3))
    #print dataRunDB
    #dataRunDB = getRunDBData('rundbfills', int(arg3))
    #print dataRunDB
    #myShelve.update(dataRunDB)

    if 'rundbrun' in rundb_type:
        stmt = "select * from %s where runid = %d" % (rundb_type, identifier)
    else:
        stmt = "select * from %s where id = %d" % (rundb_type, identifier)
    cursor.execute(stmt)

    output = {}
    #print type(cursor)
    for row in cursor:
        if 'params' in rundb_type:
            output[row[1]] = row[2]
        else:
            output[row[1]] = row[2:]
        #output.writerow(row)
        #print row
    
    cursor.close()
    connection.close()
    #FILE.close()
    return output
###############################################################################

import urllib2
def getRunDBData_url(runnumber):
    run = urllib2.urlopen('https://lbrundb.cern.ch/api/run/133689').read()
    fill = urllib2.urlopen('https://lbrundb.cern.ch/api/fill/3374').read()
    latest_fill = urllib2.urlopen('https://lbrundb.cern.ch/api/fill/latest').read()
    year_totals = urllib2.urlopen('https://lbrundb.cern.ch/api/fill/this_year_totals').read()
    print run+'\n', fill+'\n', latest_fill+'\n', year_totals+'\n'

###############################################################################
#import sys 
#sys.path.append('/group/online/rundb/RunDatabase/python')
#import rundb
#db = rundb.RunDB()
#run_data = db.getrun(79788)
#fill_data = db.getruns(3374)
#print run_data, fill_data
