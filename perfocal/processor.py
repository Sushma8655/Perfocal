import os
from collections import defaultdict
from datetime import datetime, timedelta
from . import admin
from mindsphere_core import RestClientConfig, AppCredentials
from mindsphere_core import serialization_filter
from mindsphere_core.exceptions import MindsphereError
from iottsbulk.clients.read_operations_client import ReadOperationsClient
from iottsbulk.models.retrieve_timeseries_request import RetrieveTimeseriesRequest

AppName = os.environ['MDSP_OS_VM_APP_NAME']
AppVersion = os.environ['MDSP_OS_VM_APP_VERSION']
HostTenant = os.environ['MDSP_HOST_TENANT']
UserTenant = os.environ['MDSP_USER_TENANT']

x = datetime.now()

class processvalue:
    def __init__(
            self,
            id_new=None,
            property_set_name=None,
            _from=None,
            to=None,
            DataHandshakeConfig=None
    ):
        self.DataHandshakeConfig = DataHandshakeConfig
        self.id = id_new
        self.property_set_name = property_set_name
        self._from = _from
        self.to = to
        self.DataHandshakeConfig = ReadOperationsClient()
        self.DataHandshakeConfig.rest_client_config = RestClientConfig()
        self.DataHandshakeConfig.mindsphere_credentials = AppCredentials(app_name=AppName, app_version=AppVersion,
                                                                         host_tenant=HostTenant,
                                                                         user_tenant=UserTenant)

    def showplot(self):

        try:
            retrieveTimeseriesRequest = RetrieveTimeseriesRequest()
            retrieveTimeseriesRequest.entity = self.id
           
            retrieveTimeseriesRequest.property_set_name = self.property_set_name

            retrieveTimeseriesRequest._from = self._from
            # print("from date",retrieveTimeseriesRequest._from)
            retrieveTimeseriesRequest.to = self.to

            response2 = ReadOperationsClient.retrieve_timeseries(self=self.DataHandshakeConfig,
                                                                 request_object=retrieveTimeseriesRequest)
            # print(response2)
            records = serialization_filter.sanitize_for_serialization(response2)
            record = records.get("records")
            # print(records)
            jsondata = []
            xaxis = []
            xaxis1 = []
            newvalue = []
            xlist = []
            yaxis = []
            xlist1 = []
            yaxis1 = []
            yaxis2 = []
            yaxis3 = []
            yaxis4 = []
            yaxis5 = []
            yaxis6 = []
            yaxis7 = []
            yaxis8 = []
            ylistOperatingTime = []
            ylistPlannedStop = []
            ylistProductiveTime = []
            ylistUnproductiveTime = []
            ylistRunningState = []
            ylistUnplannedStop = []
            ylistBreakdownTime = []
            ylistActiveMode = []
            ylistBatchNo = []
            OperPlanBreakline = []
            OperPlanBreakNew = []
            TotalOperatingCount = 0
            TotalPlannedStopCount = 0
            TotalBreakdownCount = 0
            OperatingOnTime = 0
            OperatingOffTime = 0
            PlannedStopOnTime = 0
            PlannedStopOffTime = 0
            BreakdownOnTime = 0
            BreakdownOffTime = 0
            TotalProductiveTime = 0
            TotalUnproductiveTime = 0
            for i in record:
                for key, v in i.items():
                    xaxis = None
                    if key == '_time':
                        dt_obj = v
                        utc_date_str = datetime.strptime(v, '%Y-%m-%dT%H:%M:%S.%f%z')
                        xaxis = datetime.strftime(utc_date_str, '%d/%m/%Y %H:%M')
                        xaxis1 = datetime.strftime(utc_date_str, '%d/%m/%Y')
                        xlist.append(xaxis)
                        xlist1.append(xaxis1)
                        newvalue = xaxis
                        # print(newvalue)
                        i.update({'_time': newvalue})
                        jsondata.append(i)
                    if key == 'OperatingTime':
                        if v == True:
                            yaxis1 = 1
                        else:
                            yaxis1 = 0
                        ylistOperatingTime.append(yaxis1)
                    if key == 'PlannedStop':
                        if v == True:
                            yaxis2 = 1
                        else:
                            yaxis2 = 0
                        ylistPlannedStop.append(yaxis2)
                    if key == 'ProductiveTime':
                        if v == True:
                            yaxis4 = 1
                        else:
                            yaxis4 = 0
                        ylistProductiveTime.append(yaxis4)
                    if key == 'UnproductiveTime':
                        if v == True:
                            yaxis5 = 1
                        else:
                            yaxis5 = 0
                        ylistUnproductiveTime.append(yaxis5)
                    if key == 'RunningState':
                        if v == True:
                            yaxis6 = 1
                        else:
                            yaxis6 = 0
                        ylistRunningState.append(yaxis6)
                    if key == 'UnplannedStop':
                        if v == True:
                            yaxis = 1
                        else:
                            yaxis = 0
                        ylistUnplannedStop.append(yaxis)
                        # print("Unplanned Stop",ylistUnplannedStop)
                    if key == 'BreakdownTime':
                        if v == True:
                            yaxis3 = 1
                        else:
                            yaxis3 = 0
                        ylistBreakdownTime.append(yaxis3)
                    if key == 'ActiveMode':
                        if v != None:
                            yaxis7 = v
                        ylistActiveMode.append(yaxis7)
                    # if key == 'ActiveMode' and v == 1 and key == 'OperatingTime' and v == 1:
                    #     print("The VVVVV",v)
                    if key == 'BatchNo':
                        if v != None:
                            yaxis8 = v
                        ylistBatchNo.append(yaxis8)
            OperPlanBreaklinetemp = [newvalue, yaxis1, yaxis2, yaxis3, yaxis, yaxis4, yaxis5, yaxis6, yaxis7, yaxis8]
            OpenPlanBreak = [xaxis1, yaxis8]
            OperPlanBreakline.insert(-1, OperPlanBreaklinetemp)
            OperPlanBreakNew.insert(-1, OpenPlanBreak)
            # print("The OperPlan break", OperPlanBreakNew)
            TotalOperatingCount = len(ylistOperatingTime)
            OperatingOnTime = admin.countX(ylistOperatingTime, 1)
            # print("OperatingOnTime", OperatingOnTime)
            OperatingOffTime = admin.countX(ylistOperatingTime, 0)

            TotalProductiveTime = len(ylistProductiveTime)
            ProductiveOnTime = admin.countX(ylistProductiveTime, 1)
            ProductiveOffTime = admin.countX(ylistProductiveTime, 0)

            TotalUnproductiveTime = len(ylistUnproductiveTime)
            UnproductiveOnTime = admin.countX(ylistUnproductiveTime, 1)
            UnproductiveOffTime = admin.countX(ylistUnproductiveTime, 0)

            TotalPlannedStopCount = len(ylistPlannedStop)
            PlannedStopOnTime = admin.countX(ylistPlannedStop, 1)
            PlannedStopOffTime = admin.countX(ylistPlannedStop, 0)

            TotalUnplannedStopCount = len(ylistUnplannedStop)
            UnplannedStopOnTime = admin.countX(ylistUnplannedStop, 1)
            UnplannedStopOffTime = admin.countX(ylistUnplannedStop, 0)
            # print("The Unplanned Stop On Time", UnplannedStopOnTime)

            TotalBreakdownCount = len(ylistBreakdownTime)
            BreakdownOnTime = admin.countX(ylistBreakdownTime, 1)
            BreakdownOffTime = admin.countX(ylistBreakdownTime, 0)

            TotalActiveMode = len(ylistActiveMode)
            ActiveMode1 = admin.countX(ylistActiveMode, 0)
            ActiveMode2 = admin.countX(ylistActiveMode, 1)
            ActiveMode3 = admin.countX(ylistActiveMode, 2)
            ActiveMode4 = admin.countX(ylistActiveMode, 3)
            ActiveMode5 = admin.countX(ylistActiveMode, 4)
            ActiveMode6 = admin.countX(ylistActiveMode, 5)
            ActiveMode7 = admin.countX(ylistActiveMode, 6)
            # print("count of mode 1",ActiveMode2)
            # print("count of mode 2", ActiveMode3)
            # print("Count of mode 3",ActiveMode4)
            # print("Count of mode 5", ActiveMode6)
            # print("Count of mode 6", ActiveMode7)
            TotalUnplannedDownTime = len(ylistUnplannedStop)
            UnplannedOnTime = admin.countX(ylistUnplannedStop, 1)
            UnplannedOffTime = admin.countX(ylistUnplannedStop, 0)

            TotalforAvailability = OperatingOnTime + PlannedStopOnTime + BreakdownOnTime
            # print("Its i guess 0",TotalforAvailability)
            # Availability = OperatingOnTime / TotalforAvailability * 100

            cip = []
            pht = []
            sip = []
            trip = []
            maintenance = []
            dateBatchArr = []
            # dateBatchArray = []
            for i in OperPlanBreakline:
                # dateBatch = [i[0],i[9]]
                # if i[0] != None and i[9] != None:
                #     dateBatchArr.append(i)
                if i[8] == 1 and i[1] == 1:
                    cip.append(i)
                if i[8] == 2 and i[1] == 1:
                    pht.append(i)
                if i[8] == 3 and i[1] == 1:
                    sip.append(i)
                if i[8] == 5 and i[4] == 1:
                    trip.append(i)
                if i[8] == 6 and i[4] == 1:
                    maintenance.append(i)
            # dateBatchArray.append(dateBatch)
            # for i,j in OperPlanBreakNew:
            #     if i == ''
            # print("Date Batch Array",OperPlanBreakNew)
            cipCount = len(cip) - 1
            phtCount = len(pht)
            sipCount = len(sip)
            tripCount = len(trip)
            maintainCount = len(maintenance)
            print("cipCount", cipCount)
            print("PHT count", phtCount)
            print("SIP count", sipCount)
            print("trip count", tripCount)
            print("Maintenance count", maintainCount)

            # print("PlannedStopOn",PlannedStopOnTime)
            # print("Operating Time:",OperatingOnTime)
            # print("Availability in %:",Availability)

            AbatchNo = []
            AlarmNoArray = []
            ModeArray = []

            # print("The Batch Array",AbatchNo)
            #
            for i in jsondata:
                try:
                    BatachNo = i['BatchNo']
                    AlarmNo = i['AlarmNo']
                    Mode = i['ActiveMode']
                except KeyError:
                    print("Key Not taken here!")
                AlarmNoArray.append(AlarmNo)
                # print("AlarmNo",AlarmNoArray)
                AbatchNo.append(BatachNo)
                ModeArray.append(Mode)
            Array1 = []
            Array2 = []
            Array3 = []
            Array4 = []
            Array = []
            # array for value 0
            for i in ModeArray:
                if i == 0:
                    Array.append(i)
                    # array for value 1
                if i == 1:
                    Array1.append(i)
                    # array for value 2
                if i == 2:
                    Array2.append(i)
                    # array for value 3
                if i == 3:
                    Array3.append(i)
                    # array for value 4
                if i == 4:
                    Array4.append(i)

            UniqueBatchNo = []
            for i in AbatchNo:
                if i not in UniqueBatchNo:
                    UniqueBatchNo.append(i)
                    UniqueBatchNo.sort()
            UniqueBatchNo.pop(0)
            # print("UBatch",UniqueBatchNo)
            lastBatchNo = UniqueBatchNo[-1]
            print("Last No", lastBatchNo)
            lenOfTheBatch = len(UniqueBatchNo)

            QualityTot = lenOfTheBatch
            GoodBatch = lenOfTheBatch
            BadBatch = 0
            # QualityTot - GoodBatch
            QualityPer = round(GoodBatch / QualityTot * 100, 1)
            # print("quality",QualityTot)

            TotalforAvailability = OperatingOnTime + PlannedStopOnTime + BreakdownOnTime
            # print("The OperatingOnTime", TotalforAvailability)
            Availability = (OperatingOnTime / TotalforAvailability * 100)
            AvailabilityPer = round(Availability, 1)
            # print("Availability in %:", AvailabilityPer)
            #
            # # for i in myjson:
            # #     i['_time'] = datetime.strptime(i['_time'],'%Y-%m-%dT%H:%M:%S.%f%z')
            # #     i['_time'] = datetime.strftime(i['_time'],'%d/%m/%Y %H:%M')
            # #
            # # print("My Json",i['_time'])
            #
            idealBatch = 186
            ActualBatch = lenOfTheBatch
            MissedBatch = idealBatch - lenOfTheBatch
            Performance = round(ActualBatch / idealBatch * 100, 1)
            print("Performance", ActualBatch)

            OEETotal = TotalforAvailability + idealBatch + QualityTot
            actualOEE = ActualBatch + OperatingOnTime + GoodBatch
            print("OEE Total", OEETotal)
            OEEPercent = round(actualOEE / OEETotal * 100, 1)
            print("OEE Percent", OEEPercent)
            ######################################################### unique code from the view of downtime Analysis##################

            TotalPlannedDownTime = len(ylistPlannedStop)
            TotalUnplannedDownTime = len(ylistUnplannedStop)
            formattedProOnTime = str(timedelta(minutes=ProductiveOnTime))
            # print("Formatted Pro Time",formattedProOnTime)

            formattedCipTime = str(timedelta(minutes=cipCount))
            # print("Formatted Pro Time", dateBatchArray)

            formattedPhtTime = str(timedelta(minutes=phtCount))
            formattedSipTime = str(timedelta(minutes=sipCount))
            formattedPlStpOnTime = str(timedelta(minutes=PlannedStopOnTime))
            formattedTripTime = str(timedelta(minutes=tripCount))
            formattedMaintainTime = str(timedelta(minutes=maintainCount))
            ##############################################################################################################################

            ##################################code for the Production Yeild###############################################################
            # print("The date array",xlist)

            # OperPlanBreakNew = []
            dateDate = []
            dateDate1 = []
            DateArray = []

            for i in xlist:
                v = i
                utc_date_str = datetime.strptime(v, '%d/%m/%Y %H:%M')
                xaxis = datetime.strftime(utc_date_str, '%d/%m/%Y')
                DateArray.append(xaxis)
            countofDateArr = len(DateArray)
            # print("The Length of Date",countofDateArr)
            countOfBatchNo = len(ylistBatchNo)
            # print("count of batchno", countOfBatchNo)
            # OperPlaneBreak = [DateArray,ylistBatchNo]
            # OperPlanBreakNew.insert(-1,OperPlaneBreak)

            # print("The Operplanbreaknew", OperPlanBreakNew)

            UniqueOpenbreak = []
            for i in OperPlanBreakNew:
                if i not in UniqueOpenbreak:
                    UniqueOpenbreak.append(i)
            # print("This is the Unique", UniqueOpenbreak)
            # BahutUnique = { k[0]: k[1:] for k in UniqueOpenbreak}
            # print("Bahut Unique",BahutUnique)
            d = defaultdict(list)
            for k, v in UniqueOpenbreak:
                d[k].append(v)
            # i = iter(UniqueOpenbreak)
            # my_dict = dict((a[0], b) for a, b in zip(i, i))
            DBUniqueDict = dict(d)
            # print("Bahut Unique", DBUniqueDict)
            lenValue = (list(DBUniqueDict.values()))
            # for key,value in DBUniqueDict:
            #     if value != None:
            #         lenValue = len(value)
            MyValArray = []

            for i in lenValue:
                lenofValue = len(i) - 1
                MyValArray.append(lenofValue)

            lenofValueArray = len(MyValArray)

            # print("len Of Value", MyValArray)

            theIdealBatchArr = [15] * lenofValueArray
            theDollarArray = [item * 2 for item in MyValArray]
            # print("The ideal Batch Array", theIdealBatchArr)

            for i in OperPlanBreakNew:
                if i[0] != '08/06/2021' and i[0] != '09/06/2021':
                    dateDate.append(i)
                if i[0] != '07/06/2021' and i[0] != '09/06/2021':
                    dateDate1.append(i)
            # print("Nusti Date",dateDate)
            lendateDate = len(dateDate)
            lendateDate1 = len(dateDate1)
            # print("Nusti Date", lendateDate)
            # print("Nusti date 1",lendateDate1)

            # Merging two Array to form a dict of key value pair here the Group by is done with date
            someArray = []
            res = defaultdict(list)
            for i, j in zip(DateArray, ylistBatchNo):
                # if j not in someArray:
                #     someArray.append(j)
                res[i].append(j)
            theDict = dict(res)
            # print("The Merged Array",theDict)
            keysArray = (list(theDict.keys()))
            listArray = (list(theDict.values()))
            # for key in theDict:
            #     for value in theDict[key]:
            #         for i in str(value):
            #             if i not in someArray:
            #                 someArray.append(i)
            for i in listArray:
                if i not in someArray:
                    someArray.append(i)
            # print('some array',someArray)

            for key in theDict:
                print("Keys", key)
                print("Value Length", len(theDict[key]))

            for i in listArray:
                Unique_list = i
                Unique_list1 = list(dict.fromkeys(Unique_list))
            # print("The Unique Bhai",Unique_list1)

            print(sum([len(theDict[x]) for x in theDict if isinstance(theDict[x], list)]))
            result = list(sorted({ele for val in theDict.values() for ele in val}))
            print("The result", keysArray)
            print("Length", MyValArray)
            # print("The result", listArray)
            UniqueBatachNo = []
            # for i, j in theDict:
            #
            #     if j not in UniqueBatachNo:
            #         UniqueBatachNo.append(j)
            #         UniqueBatachNo.sort()
            # for key,val in theDict[key]:
            #     if val not in UniqueBatachNo:
            #         UniqueBatachNo.append(val)
            # for i in theDict.keys():
            #     key = i
            #     value = theDict[i]
            #     if value != None:
            #         UniqueBatachNo.append(value)
            #     # print("Key:", i, "\tData:", theDict[i])
            # # BtachNo = list(set(tpl[x] for tpl in UniqueBatachNo))
            # print("Kuch Gurantee nai",UniqueBatachNo)
            # someArray = []
            # for bacthArray in UniqueBatachNo:
            #     for bachNo in bacthArray:
            #         if bachNo not in someArray:
            #             someArray.append(bachNo)
            # print("Some Array",someArray)

            theMostUniqueBtchNo = []
            # for BatchArray in UniqueBatachNo:
            #     if BatchArray != None:
            #         lenofBatchArray = len(BatchArray)
            # for BachNo in BatchArray:
            #     if BachNo not in theMostUniqueBtchNo:
            #         theMostUniqueBtchNo.append(BachNo)
            print("The Unique batch Array", theMostUniqueBtchNo)

            # print("Unique Btached",lenofBatchArray)
            print("The result", keysArray)
            lenofUniqueBta = len(UniqueBatachNo)
            UniqueDate = []
            for i in DateArray:
                if i not in UniqueDate:
                    UniqueDate.append(i)
                    UniqueDate.sort()
            print("Unique Date", countofDateArr)
            print("Date Batch Array", countOfBatchNo)
            print('Date lenofUniqueBta', lenofUniqueBta)
            return {'Quality': QualityPer, 'Availability': AvailabilityPer, 'Performance': Performance,
                    'OEEPercent': OEEPercent, 'QualityTot': QualityTot,
                    'MissedBatchPer': MissedBatch, 'QualBadBatch': BadBatch, 'data': jsondata,
                    'QualGoodBatch': GoodBatch, 'ActualBatchPer': ActualBatch,
                    'lastBatchNo': lastBatchNo, 'GoodBatch': GoodBatch, 'BadBatch': BadBatch,
                    'AlarmNoArray': AlarmNoArray, 'xlist': xlist, 'ylistBreakdownTime': ylistBreakdownTime,
                    'ModeArray': ModeArray, 'ylistRunningState': ylistRunningState,
                    'BreakDownTime': ylistBreakdownTime, 'theDollarArray': theDollarArray,
                    'ylistOperatingTime': ylistOperatingTime,
                    'formattedProOnTime': formattedProOnTime, 'formattedCipTime': formattedCipTime,
                    'formattedPhtTime': formattedPhtTime, 'formattedSipTime': formattedSipTime,
                    'formattedPlStpOnTime': formattedPlStpOnTime, 'formattedTripTime': formattedTripTime,
                    'formattedMaintainTime': formattedMaintainTime,
                    'ylistPlannedStop': ylistPlannedStop, 'ProductiveOnTime': ProductiveOnTime,
                    'UnproductiveOnTime': UnproductiveOnTime, 'PlannedStopOnTime': PlannedStopOnTime,
                    'TotalUnplannedDownTime': TotalUnplannedDownTime, 'maintaincount': maintainCount,
                    'tripcount': tripCount, 'sipCount': sipCount, 'phtCount': phtCount, 'cipCount': cipCount,
                    'TotalPlannedDownTime': TotalPlannedDownTime,
                    'OperatingOnTime': OperatingOnTime,
                    'BreakdownOnTime': BreakdownOnTime, 'keysArray': keysArray, 'MyValArray': MyValArray,
                    'theIdealBatchArr': theIdealBatchArr, 'UniqueBatchNo': UniqueBatchNo,
                    }
        except MindsphereError as err:
            print("ERROR:", err)
            return err
            # Exception Handling
