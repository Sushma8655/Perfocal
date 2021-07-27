from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from maintenance.models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from maintenance.models import maintenanceClose as mainclose
from .forms import *
from django.urls import reverse
from dateutil.relativedelta import relativedelta
# val = None
# Create your views here.
@login_required(login_url='login/')
def home(request):
    x1 = datetime.now()
    form = registryForm(request.POST)
    if request.method == 'POST' and form.is_valid:
        form.save()
        # n = request.POST.get("servicePeriod")
        # DMY = request.POST.get("servicePeriodDMY")
        # print("The value of N", n)
        # print("The Value of DMY", DMY)
        # global val
        # def val():
        #     return n
        return render(request, 'index.html')
    else:
        form = registryForm()
    return render(request, 'maintenance/home.html', {"form": form, 'time': x1, })





@login_required(login_url='login/')
def registryrecords(request):
    x1 = datetime.now()
    form = maintenanceInitiate(request.POST or None)
    # ok = val()
    if request.POST:
        if form.is_valid():

            elementID = request.POST.get("elementID")
            initmaintainDate = request.POST.get("installationMaintenanceDate")

            status = "Initiated"
            initiateTimestamp = datetime.now()
            ackStatus = "Not Acknowledged"
            closeStatus = "Not Closed"
            print("Date", initmaintainDate)
            countServicePeriod = partRegistry.objects.values_list('servicePeriod', flat=True).get(partsID =elementID)
            DMYServicePeriod = partRegistry.objects.values_list('servicePeriodDMY', flat=True).get(partsID =elementID)
            if countServicePeriod is not None:
                if DMYServicePeriod == "Days":
                    dayservicePeriod = datetime.strptime(initmaintainDate, "%Y-%m-%dT%H:%M") + timedelta(
                        days=countServicePeriod)
                    actualserviceDate = datetime.strftime(dayservicePeriod, "%Y-%m-%dT%H:%M")
                    print("The date after the initiation time", dayservicePeriod)
                if DMYServicePeriod == "Weeks":
                    dayservicePeriod = datetime.strptime(initmaintainDate, "%Y-%m-%dT%H:%M") + timedelta(
                        weeks=countServicePeriod)
                    actualserviceDate = datetime.strftime(dayservicePeriod, "%Y-%m-%dT%H:%M")
                    # print("The date after the initiation time", actualserviceDate)
                if DMYServicePeriod == "Months":
                    dayservicePeriod = datetime.strptime(initmaintainDate, "%Y-%m-%dT%H:%M") + relativedelta(
                        months=countServicePeriod)
                    actualserviceDate = datetime.strftime(dayservicePeriod, "%Y-%m-%dT%H:%M")
                    # print("The date after the initiation time", actualserviceDate)
            ###################Directly Inserting Data from Form to the Database Directly########################
                theelementID = initiateMaintenance.objects.create(elementID=elementID,
                                                                  installationMaintenanceDate=initmaintainDate,
                                                                  nextDueDate=actualserviceDate,
                                                                  initiateStatus=status,initiateTimestamp=initiateTimestamp,
                                                                  ackStatus=ackStatus,closeStatus=closeStatus
                                                                  )
            return render(request, 'index.html')


    else:
        form = maintenanceInitiate(request.POST or None)
    initObj = initiateMaintenance.objects.all()
    return render(request, 'maintenance/registryrecords.html', {'time': x1, 'form1':form,'initObj':initObj})

def acknowledge(request):
    x1 = datetime.now()
    form = maintenanceAcknowledge(request.POST or None)
    initObj = initiateMaintenance.objects.all()
    if request.POST:
        if form.is_valid():
            elementID = request.POST.get("elementID")
            initiateStatus = "Done"
            AcknowlegedStatus = "Acknowledged"
            AckTimestamp = datetime.now()
            ID = initiateMaintenance.objects.values_list('id', flat=True).filter(elementID=elementID).latest('id')
            # print("The Unique ID Passed",ID)

            updateTable = initiateMaintenance.objects.filter(id=ID).update(initiateStatus=initiateStatus,
                                                                                         ackStatus=AcknowlegedStatus,
                                                                                         ackTimestamp=AckTimestamp)
            return render(request, 'index.html')

    # initObjects = initiateMaintenance.objects.all()
    # return HttpResponseRedirect('/maintenance/acknowledge',{'x1': x1, 'initiateObj': initObjects})
    else:
        form = maintenanceAcknowledge(request.POST or None)
    initObj = initiateMaintenance.objects.all().filter(initiateStatus="Initiated")
    return HttpResponseRedirect('/maintenance/acknowledge', {'time': x1, 'form': form,'initObj':initObj})

def ackApproved(request,elementID):
    x1 = datetime.now()
    initObjects = initiateMaintenance.objects.all()
    approvedID = initiateMaintenance.objects.get(elementID=elementID)
    status = "Acknowledged"
    theID = initiateMaintenance.objects.values_list('id',flat=True).get(elementID=elementID)
    initialDate = initiateMaintenance.objects.values_list('installationMaintenanceDate', flat=True).get(elementID=elementID)
    nextDueDate = initiateMaintenance.objects.values_list('nextDueDate', flat=True).get(elementID=elementID)
    saveAck = maintenanceAcknowledge.objects.create(elementAID=elementID,
                                                    initialisedDate=initialDate,
                                                    nextDueDate=nextDueDate,
                                                    status=status,
                                                    initID_id=theID)
    return HttpResponseRedirect('/maintenance/acknowledge',{'time': x1, 'initiateObj': initObjects})
    # return render(request,'maintenance/acknowledge.html',{'x1': x1, 'initiateObj': initObjects})

def maintainClose(request):
    x1 = datetime.now()
    form = maintenanceClose(request.POST or None)
    initObjR = initiateMaintenance.objects.all().filter(initiateStatus="Repair")
    if request.POST:
        if form.is_valid():
            elementID = request.POST.get("elementID")
            closeTimestamp = request.POST.get("closeTimestamp")
            AcknowlegedStatus = "Done"
            closedStatus = "Done"
            repairID = request.POST.get("repairID")
            print(repairID)
            istatus = "Initiated"
            ackStatus = "Not Acknowledged"
            closeStatus = "Not Closed"
            if repairID is None:
                updateTable = initiateMaintenance.objects.filter(elementID=elementID).update(ackStatus=AcknowlegedStatus,
                                                                                             closeStatus=closedStatus,
                                                                                             closeTimestamp=closeTimestamp)


                countServicePeriod = partRegistry.objects.values_list('servicePeriod', flat=True).get(partsID=elementID)
                DMYServicePeriod = partRegistry.objects.values_list('servicePeriodDMY', flat=True).get(partsID=elementID)
                if countServicePeriod is not None:
                    if DMYServicePeriod == "Days":
                        dayservicePeriod = datetime.strptime(closeTimestamp, "%Y-%m-%dT%H:%M") + timedelta(
                            days=countServicePeriod)
                        actualserviceDate = datetime.strftime(dayservicePeriod, "%Y-%m-%dT%H:%M")
                        print("The date after the initiation time", dayservicePeriod)
                    if DMYServicePeriod == "Weeks":
                        dayservicePeriod = datetime.strptime(closeTimestamp, "%Y-%m-%dT%H:%M") + timedelta(
                            weeks=countServicePeriod)
                        actualserviceDate = datetime.strftime(dayservicePeriod, "%Y-%m-%dT%H:%M")
                        # print("The date after the initiation time", actualserviceDate)
                    if DMYServicePeriod == "Months":
                        dayservicePeriod = datetime.strptime(closeTimestamp, "%Y-%m-%dT%H:%M") + relativedelta(
                            months=countServicePeriod)
                        actualserviceDate = datetime.strftime(dayservicePeriod, "%Y-%m-%dT%H:%M")



                reinitiate = initiateMaintenance.objects.create(elementID=elementID,
                                                                      installationMaintenanceDate=closeTimestamp,
                                                                      nextDueDate=actualserviceDate,
                                                                      initiateStatus=istatus, initiateTimestamp=closeTimestamp,
                                                                      ackStatus=ackStatus, closeStatus=closeStatus)
                # return render(request, 'index.html')
            if repairID is not None:
                updateState = initiateMaintenance.objects.values_list('repairUpdateCycle', flat=True).filter(
                            elementID=repairID).latest('repairUpdateCycle')
                print("The Repair ID", updateState)
                if updateState == "Yes":
                    print("updateState = yes")
                    updateTable = initiateMaintenance.objects.filter(elementID=repairID).update(
                        initiateStatus="Done",
                        closeStatus=closedStatus,
                        closeTimestamp=closeTimestamp)

                    countServicePeriod = partRegistry.objects.values_list('servicePeriod', flat=True).get(
                        partsID=repairID)
                    DMYServicePeriod = partRegistry.objects.values_list('servicePeriodDMY', flat=True).get(
                        partsID=repairID)
                    if countServicePeriod is not None:
                        if DMYServicePeriod == "Days":
                            dayservicePeriod = datetime.strptime(closeTimestamp, "%Y-%m-%dT%H:%M") + timedelta(
                                days=countServicePeriod)
                            actualserviceDate = datetime.strftime(dayservicePeriod, "%Y-%m-%dT%H:%M")
                            print("The date after the initiation time", dayservicePeriod)
                        if DMYServicePeriod == "Weeks":
                            dayservicePeriod = datetime.strptime(closeTimestamp, "%Y-%m-%dT%H:%M") + timedelta(
                                weeks=countServicePeriod)
                            actualserviceDate = datetime.strftime(dayservicePeriod, "%Y-%m-%dT%H:%M")
                            # print("The date after the initiation time", actualserviceDate)
                        if DMYServicePeriod == "Months":
                            dayservicePeriod = datetime.strptime(closeTimestamp, "%Y-%m-%dT%H:%M") + relativedelta(
                                months=countServicePeriod)
                            actualserviceDate = datetime.strftime(dayservicePeriod, "%Y-%m-%dT%H:%M")

                    reinitiate = initiateMaintenance.objects.create(elementID=repairID,
                                                                    installationMaintenanceDate=closeTimestamp,
                                                                    nextDueDate=actualserviceDate,
                                                                    initiateStatus=istatus,
                                                                    initiateTimestamp=closeTimestamp,
                                                                    ackStatus=ackStatus, closeStatus=closeStatus)
                    return render(request, 'index.html', {'initObj':initObjR})

                if updateState == "No":
                    updateTable = initiateMaintenance.objects.filter(elementID=elementID).update(
                        ackStatus="NA",
                        closeStatus=closedStatus,
                        closeTimestamp=closeTimestamp)



                return render(request, 'index.html')

            # initObjects = initiateMaintenance.objects.all()
            # return HttpResponseRedirect('/maintenance/acknowledge',{'x1': x1, 'initiateObj': initObjects})

        else:
            form = maintenanceClose(request.POST or None)
    initObj = initiateMaintenance.objects.all()
    return render(request, 'maintenance/maintainClose.html', {'time': x1, 'form': form, 'initObj': initObj})

def repairmaintenance(request):
    x1 = datetime.now()
    form = reparirForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            elementID = request.POST.get("elementID")
            repairDate = request.POST.get("installationMaintenanceDate")
            updateCycle = request.POST.get("repairUpdateCycle")
            if updateCycle == "Yes":
                try:
                    initstatus = initiateMaintenance.objects.values_list('initiateStatus', flat=True).filter(elementID=elementID).latest('initiateStatus')
                    if initstatus == "Initiated":
                        ID = initiateMaintenance.objects.values_list('id', flat=True).filter(
                            elementID=elementID).latest('id')
                        countServicePeriod = partRegistry.objects.values_list('servicePeriod', flat=True).get(
                            partsID=elementID)
                        DMYServicePeriod = partRegistry.objects.values_list('servicePeriodDMY', flat=True).get(
                            partsID=elementID)
                        if countServicePeriod is not None:
                            if DMYServicePeriod == "Days":
                                dayservicePeriod = datetime.strptime(repairDate, "%Y-%m-%dT%H:%M") + timedelta(
                                    days=countServicePeriod)
                                actualserviceDate = datetime.strftime(dayservicePeriod, "%Y-%m-%dT%H:%M")
                                print("The date after the initiation time", dayservicePeriod)
                            if DMYServicePeriod == "Weeks":
                                dayservicePeriod = datetime.strptime(repairDate, "%Y-%m-%dT%H:%M") + timedelta(
                                    weeks=countServicePeriod)
                                actualserviceDate = datetime.strftime(dayservicePeriod, "%Y-%m-%dT%H:%M")
                                # print("The date after the initiation time", actualserviceDate)
                            if DMYServicePeriod == "Months":
                                dayservicePeriod = datetime.strptime(repairDate,"%Y-%m-%dT%H:%M") + relativedelta(
                                    months=countServicePeriod)
                                actualserviceDate = datetime.strftime(dayservicePeriod, "%Y-%m-%dT%H:%M")
                        reinitiateStatus = "Repair"
                        reinitiatetimestamp = datetime.now()
                        ackStatus = "NA"
                        closeStatus = "Not Closed"
                        updateDB = initiateMaintenance.objects.filter(id=ID).update(installationMaintenanceDate=repairDate,
                                                                         nextDueDate=actualserviceDate,initiateStatus=reinitiateStatus,
                                                                                     initiateTimestamp=reinitiatetimestamp,
                                                                                     ackStatus=ackStatus, closeStatus=closeStatus,
                                                                                    repairUpdateCycle=updateCycle)

                        print("Initiated")
                except:
                    msg = "No Record to Update for the above mentioned element ID please ask to initiate"
                try:

                    initstatus = initiateMaintenance.objects.values_list('initiateStatus', flat=True).filter(
                        elementID=elementID).latest('initiateStatus')

                    ackStatus = initiateMaintenance.objects.values_list('ackStatus', flat=True).filter(elementID=elementID).last()

                    if initstatus == "Done" and ackStatus == "Acknowledged":
                        ID = initiateMaintenance.objects.values_list('id', flat=True).filter(elementID=elementID).latest('id')
                        countServicePeriod = partRegistry.objects.values_list('servicePeriod', flat=True).get(partsID=elementID)
                        DMYServicePeriod = partRegistry.objects.values_list('servicePeriodDMY', flat=True).get(partsID=elementID)
                        if countServicePeriod is not None:
                            if DMYServicePeriod == "Days":
                                dayservicePeriod = datetime.strptime(repairDate, "%Y-%m-%dT%H:%M") + timedelta(
                                    days=countServicePeriod)
                                actualserviceDate = datetime.strftime(dayservicePeriod, "%Y-%m-%dT%H:%M")
                                print("The date after the initiation time", dayservicePeriod)
                            if DMYServicePeriod == "Weeks":
                                dayservicePeriod = datetime.strptime(repairDate, "%Y-%m-%dT%H:%M") + timedelta(
                                    weeks=countServicePeriod)
                                actualserviceDate = datetime.strftime(dayservicePeriod, "%Y-%m-%dT%H:%M")
                                # print("The date after the initiation time", actualserviceDate)
                            if DMYServicePeriod == "Months":
                                dayservicePeriod = datetime.strptime(repairDate, "%Y-%m-%dT%H:%M") + relativedelta(
                                    months=countServicePeriod)
                                actualserviceDate = datetime.strftime(dayservicePeriod, "%Y-%m-%dT%H:%M")
                        reinitiateStatus = "Repair"
                        reinitiatetimestamp = datetime.now()
                        ackStatus = "NA"
                        closeStatus = "Not Closed"
                        updateDB = initiateMaintenance.objects.filter(id=ID).update(installationMaintenanceDate=repairDate,
                                                                                    nextDueDate=actualserviceDate,
                                                                                    initiateStatus=reinitiateStatus,
                                                                                    initiateTimestamp=reinitiatetimestamp,
                                                                                    ackStatus=ackStatus, closeStatus=closeStatus,
                                                                                    repairUpdateCycle=updateCycle)

                except:
                    msg = "No Record to Update for the above mentioned element ID please ask to initiate"
                    if msg is not None:
                        return render(request, 'maintenance/repair.html', {'time': x1, 'form1': form, 'msg':msg})
                initObj = initiateMaintenance.objects.all()
                return render(request, 'maintenance/repair.html', {'time': x1, 'form1': form,'initObj':initObj})
            if updateCycle == "No":
                initiateDateRepair = datetime.now()
                createDBRecord = initiateMaintenance.objects.create(elementID=elementID,
                                                                    installationMaintenanceDate=repairDate,
                                                                    initiateStatus="Repair", initiateTimestamp=initiateDateRepair,
                                                                    ackStatus="NA", closeStatus="Not Closed",
                                                                    repairUpdateCycle=updateCycle)
            else:
                print("No value")

    initObj = initiateMaintenance.objects.all()
    return render(request, 'maintenance/repair.html', {'time': x1, 'form1': form, 'initObj': initObj})


def recordHistory(request):
    x1 = datetime.now()
    tableContent = initiateMaintenance.objects.all()
    countofRepair = initiateMaintenance.objects.all().filter(initiateStatus="Repair").count()
    countInitiated = initiateMaintenance.objects.all().filter(initiateStatus="Initiated").count()
    repairstateD = initiateMaintenance.objects.all().filter(initiateStatus="Done", ackStatus="NA", closeStatus="Done").count()
    ackCount = initiateMaintenance.objects.all().filter(initiateStatus="Done", ackStatus="Acknowledged").count()
    notackCount = initiateMaintenance.objects.all().filter(initiateStatus="Done", ackStatus="Not Acknowledged").count()
    closedCount = initiateMaintenance.objects.all().filter(initiateStatus="Done", closeStatus="Done").count()
    notClosedCount = initiateMaintenance.objects.all().filter(initiateStatus="Done", closeStatus="Not Closed").count()
    return render(request, 'maintenance/recordHistory.html', {'time':x1, 'tableContent': tableContent, 'countInitiated':countInitiated,
                                                              'repairstateD': repairstateD, 'ackCount': ackCount,
                                                              'notackCount': notackCount, 'closedCount':closedCount,
                                                              'countofRepair':countofRepair, 'notClosedCount':notClosedCount})