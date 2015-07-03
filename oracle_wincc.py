import cx_Oracle

def is_sequence(arg):
    return (not hasattr(arg, "strip") and
            hasattr(arg, "__getitem__") or
            hasattr(arg, "__iter__"))

def _checkDates(ti, tf):
    from datetime import datetime

    if isinstance(ti, str):
        ti = datetime.strptime(ti, '%Y-%m-%d %H:%M:%S')
    if isinstance(tf, str):
        tf = datetime.strptime(tf, '%Y-%m-%d %H:%M:%S')

    if ti > tf:
            return False

    ti = _changeToTz(ti, 'utc')
    tf = _changeToTz(tf, 'utc')

    return ti, tf

def _changeToTz(ts, tzone, oracleTs=False):
    from datetime import datetime
    from dateutil import tz

    if oracleTs:
        ts = ts[:-3] #strip the last three digits from the millisecond part of the oracle timestamp
        ts = datetime.strptime(ts, '%Y.%m.%d %H:%M:%S.%f')

    if tzone.lower() == 'utc':
        ts = ts.replace(tzinfo=tz.tzlocal())
        if oracleTs:
            #ts = ts.astimezone(tz.tzutc()).__str__().split('+')[0]
            ts = ts.astimezone(tz.tzutc()).strftime('%Y-%m-%d %H:%M:%S.%f')
        else:
            ts = ts.astimezone(tz.tzutc()).strftime('%Y-%m-%d %H:%M:%S')
    elif tzone.lower() == 'local':
        ts = ts.replace(tzinfo=tz.tzutc())
        if oracleTs:
            #ts = ts.astimezone(tz.tzlocal()).__str__().split('+')[0]
            ts = ts.astimezone(tz.tzlocal()).strftime('%Y-%m-%d %H:%M:%S.%f')
        else:
            ts = ts.astimezone(tz.tzlocal()).strftime('%Y-%m-%d %H:%M:%S')

    return ts

def getWinCCData(dpPatterns, ti, tf):
    #print dpPatterns, ti, tf
    if not _checkDates(ti, tf):
        print 'Final date cannot be before initial date!'
        return
    ti, tf = _checkDates(ti, tf)

    schemaDict = {}
    if isinstance(dpPatterns, list):
        for pattern in dpPatterns:
            schema = getSchema(pattern)
            if schema:
               schemaDict[pattern]=schema
    elif isinstance(dpPatterns, str):
        schema = getSchema(dpPatterns)
        if schema:
            schemaDict[dpPatterns]=schema

    if not schemaDict:
        return

    #print schemaDict

    sql_elements = ''
    for key in schemaDict.keys():
        for schema in schemaDict[key]:
            sql_elements+=' UNION ALL SELECT rdbhelpers_elementsObject(element_id, element_name, \'E\', 0, \''+schema+'\') FROM '+schema+'.elements_all WHERE element_name LIKE \''+key+'\''
    #sql_elements=sql_elements.lstrip("UNION ALL")+';'
    sql_elements=sql_elements[10:]+';'

    #print sql_elements

    stmt='''
    declare
    rc SYS_refcursor;
    begin
    open rc for
    '''
    #stmt+='  SELECT rdbhelpers_elementsObject(element_id, element_name, \'E\', 0, \''+schema+'\') FROM '+schema+'.elements_all WHERE element_name LIKE :dp;'
    stmt+=sql_elements
    stmt+='''
      :cur := rdbHelpers.getHistory(rc,
                                    'NAME, TS_PVSS, OFFVALUE_NUMBER, OFFVALUE_STRING',
                                    to_timestamp (:ti, 'YYYY-MM-DD HH24:MI:SS'),
                                    to_timestamp (:tf, 'YYYY-MM-DD HH24:MI:SS'));
    end;
    '''
    #print stmt

    connection = cx_Oracle.connect('a362_lb', 'lb_wr1ter', 'LHCBONR_PVSSPROD')
    cursor = connection.cursor()
    out_cursor = connection.cursor()
    bindVarList = {'cur':out_cursor, 'ti':ti, 'tf':tf}
    cursor.execute(stmt, bindVarList)

    data = []
    for row in out_cursor:
        #print row
        #data.append(row)
        value = row[2] if row[2]!=None else row[3]
        data.append((row[0], _changeToTz(row[1], 'local', True), value))
    cursor.close()
    connection.close()

    return data

def getSchema(dp):
    schemas = ['A362_CALO',
               'A362_DSS',
               'A362_GSS',
               'A362_INF',
               'A362_LB',
               'A362_LHC',
               'A362_MAGNET',
               'A362_MUON',
               'A362_OT',
               'A362_RICH',
               'A362_ST',
               'A362_TRG',
               'A362_VELO']

    connection = cx_Oracle.connect('a362_lb', 'lb_wr1ter', 'LHCBONR_PVSSPROD')
    cursor = connection.cursor()
    bindVarList = {'dp':dp}
    dpSchema = []
    for schema in schemas:
        stmt = 'SELECT count(*) FROM (SELECT DISTINCT element_id, element_name FROM '+schema+'.elements_all WHERE element_name like :dp)'
        #print dp, stmt
        cursor.execute(stmt, bindVarList)
        res = cursor.fetchone()
        if res[0]>0:
            #print schema, res[0]
            dpSchema.append(schema)

    if not dpSchema:
        print 'WARNING: No datapoint found for pattern \''+dp+'\'.'
    cursor.close()
    connection.close()
    return dpSchema


if __name__=="__main__":
    from datetime import datetime
    import os
    os.putenv('TNS_ADMIN', '/sw/oracle/linux/network/admin/')
    dpPatterns = ['%LHC:LHC_STATE%', '%VTCS_PA_%', 'naoexiste']
    #dpPatterns = '%istoelixo%'
    ti = '2015-03-27 11:00:00'
    ti = datetime(2015,03,30)
    tf = '2015-03-30 00:15:00'
    data = getWinCCData(dpPatterns, ti, tf)
    if data:
        for row in data:
            print row
