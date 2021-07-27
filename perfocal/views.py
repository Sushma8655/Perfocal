from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from .decorators import allowed_users
from datetime import datetime, timedelta
from . import timeseriesshow, bulktimeseriesshow, processor
from .models import *
from django.views import View
from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa
# Create your views here.
x = datetime.now()




@login_required(login_url='login/')
def production(request):
    results = AddMachine.objects.all()
    if request.method == 'POST':
        fromdate = request.POST.get('dateStart')
        print('type of fdate', fromdate)
        todate = request.POST.get('dateEnd')
        print('type of tdate', todate)
        MachineID = request.POST.get('MachineID')
        print('type of id', MachineID)
        assetidtemp = AddMachine.objects.get(pk=MachineID)
        print('type of asset', assetidtemp)
        AssetID = assetidtemp.AssetID
        print('The Type of fromdate', AssetID)
        context1 = processor.processvalue()
        context1.id = AssetID
    else:
        tempto = datetime.now()
        tempfrom = tempto - timedelta(hours=360)
        temptoString = datetime.strftime(tempto, '%Y-%m-%dT%H:%M:%SZ')
        tempfromString = datetime.strftime(tempfrom, '%Y-%m-%dT%H:%M:%SZ')
        fromdate = tempfromString
        todate = temptoString
        print("Normal From", fromdate)
        context1 = processor.processvalue()
        context1.id = 'ce5ad34e00ff46c48c7bb2e27fec7c49'

    context1.property_set_name = 'CJV600'
    context1._from = fromdate
    context1.to = todate
    context = processor.processvalue.showplot(self=context1)

    data = context['data']
    # print(type(data))
    GoodBatch = context['GoodBatch']
    BadBatch = context['BadBatch']
    Availability = context['Availability']
    Quality = context['Quality']
    Performance = context['Performance']
    OEEPercent = context['OEEPercent']
    QualityTot = context['QualityTot']
    lastBatchNo = context['lastBatchNo']
    keysArray = context['keysArray']
    MyValArray = context['MyValArray']
    theIdealBatchArr = context['theIdealBatchArr']
    ActualBatchPer = context['ActualBatchPer']
    MissedBatchPer = context['MissedBatchPer']
    QualGoodBatch = context['QualGoodBatch']
    QualBadBatch = context['QualBadBatch']
    OperatingOnTime = context['OperatingOnTime']
    PlannedStopOnTime = context['PlannedStopOnTime']
    BreakdownOnTime = context['BreakdownOnTime']
    ProductiveOnTime = context['ProductiveOnTime']
    UnproductiveOnTime = context['UnproductiveOnTime']
    xlist = context['xlist']
    theDollarArray = context['theDollarArray']
    # print(Availability)
    return render(request, 'production.html',
                  {'data': data, 'GoodBatch': GoodBatch, 'BadBatch': BadBatch, 'Availability': Availability, 'time': x,
                   'Quality': Quality, 'Performance': Performance, 'OEEPercent': OEEPercent, 'QualityTot': QualityTot,
                   'lastBatchNo': lastBatchNo, 'keysArray': keysArray, 'MyValArray': MyValArray, 'data1': results,
                   'theIdealBatchArr': theIdealBatchArr, 'ProductiveOnTime': ProductiveOnTime,
                   'UnproductiveOnTime': UnproductiveOnTime,
                   'ActualBatchPer': ActualBatchPer, 'xlist': xlist, 'theDollarArray': theDollarArray,
                   'MissedBatchPer': MissedBatchPer, 'QualGoodBatch': QualGoodBatch, 'QualBadBatch': QualBadBatch,
                   'OperatingOnTime': OperatingOnTime, 'PlannedStopOnTime': PlannedStopOnTime,
                   'BreakdownOnTime': BreakdownOnTime})

@login_required(login_url='login/')
# @allowed_users(allowed_roles=['admin'])
def registerPage(request):
    x = datetime.now()
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('/login')
    context = {'form': form, 'time': x, }
    return render(request, 'signup.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Username OR password is incorrect')
    context = {}
    return render(request, 'login.html', context)
    # return render(reverse('login'))


def logoutUser(request):
    logout(request)
    return redirect('/login')
def machines(request):
    results = AddMachine.objects.all()
    return render(request, 'device.html', {'data': results, 'time': x})

@login_required(login_url='login/')
def home(request):
        results = AddMachine.objects.all()
        data = []
        if request.method == 'POST':
            fromdate = request.POST.get('dateStart')
            print('type of fdate', fromdate)
            todate = request.POST.get('dateEnd')
            print('type of tdate', todate)
            MachineID = request.POST.get('MachineID')
            print('type of id', MachineID)
            assetidtemp = AddMachine.objects.get(pk=MachineID)
            # print('type of asset', assetidtemp)
            AssetID = assetidtemp.AssetID
            # print('The Type of fromdate', AssetID)
            context1 = processor.processvalue()
            context1.id = AssetID
            context1.property_set_name = 'CJV600iot'
            context1._from = fromdate
            context1.to = todate
            context = processor.processvalue.showplot(self=context1)
        else:
            tempto = datetime.now()
            tempfrom = tempto - timedelta(hours=360)
            temptoString = datetime.strftime(tempto, '%Y-%m-%dT%H:%M:%SZ')
            tempfromString = datetime.strftime(tempfrom, '%Y-%m-%dT%H:%M:%SZ')
            fromdate = tempfromString
            todate = temptoString
            # print("Normal From", fromdate)
            context1 = processor.processvalue()
            context1.id = 'ce5ad34e00ff46c48c7bb2e27fec7c49'
            context1.property_set_name = 'CJV600'
            context1._from = fromdate
            context1.to = todate
            context = processor.processvalue.showplot(self=context1)
        print(context)
        data = context['data']
        # print(type(data))
        GoodBatch = context['GoodBatch']
        BadBatch = context['BadBatch']
        Availability = context['Availability']
        Quality = context['Quality']
        Performance = context['Performance']
        OEEPercent = context['OEEPercent']
        QualityTot = context['QualityTot']
        lastBatchNo = context['lastBatchNo']
        keysArray = context['keysArray']
        MyValArray = context['MyValArray']
        theIdealBatchArr = context['theIdealBatchArr']
        ActualBatchPer = context['ActualBatchPer']
        MissedBatchPer = context['MissedBatchPer']
        QualGoodBatch = context['QualGoodBatch']
        QualBadBatch = context['QualBadBatch']
        OperatingOnTime = context['OperatingOnTime']
        PlannedStopOnTime = context['PlannedStopOnTime']
        BreakdownOnTime = context['BreakdownOnTime']
        ProductiveOnTime = context['ProductiveOnTime']
        UnproductiveOnTime = context['UnproductiveOnTime']
        xlist = context['xlist']
        theDollarArray = context['theDollarArray']
        # print(Availability)
        return render(request, 'dashboard.html',
                      {'data': data, 'GoodBatch': GoodBatch, 'BadBatch': BadBatch, 'Availability': Availability, 'time': x,
                       'Quality': Quality, 'Performance': Performance, 'OEEPercent': OEEPercent, 'QualityTot': QualityTot,
                       'lastBatchNo': lastBatchNo, 'keysArray': keysArray, 'MyValArray': MyValArray,'data1': results,
                       'theIdealBatchArr': theIdealBatchArr,'ProductiveOnTime':ProductiveOnTime,'UnproductiveOnTime':UnproductiveOnTime,
                       'ActualBatchPer': ActualBatchPer,'xlist': xlist,'theDollarArray':theDollarArray,
                       'MissedBatchPer': MissedBatchPer, 'QualGoodBatch': QualGoodBatch, 'QualBadBatch': QualBadBatch,
                       'OperatingOnTime': OperatingOnTime, 'PlannedStopOnTime': PlannedStopOnTime,
                       'BreakdownOnTime': BreakdownOnTime})


@login_required(login_url='login')
def MachineInstance(request):
    if request.method == 'POST':
        MachineID = request.POST['MachineID']
        AssetID = request.POST['AssetID']
        MachineName = request.POST['MachineName']
        Capacity = request.POST['Capacity']
        if AddMachine.objects.filter(MachineID=MachineID).exists():
            results = AddMachine.objects.all()
            return render(request, 'device.html', {'data': results, 'date': x})
        else:
            machine = AddMachine(MachineID=MachineID, MachineName=MachineName, Capacity=Capacity, AssetID=AssetID)
            machine.save()
            results = AddMachine.objects.all()
            return render(request, 'dashboard.html', {'data': results, 'date': x})
    else:
        results = AddMachine.objects.all()
        return render(request, 'device.html', {'data': results, 'date': x})


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


class ViewPDF(View):
    def get(self, request, *args, **kwargs):
        fromdate1 = request.POST.get('dateStart')
        todate1 = request.POST.get('dateEnd')
        MachineID = request.POST.get('MachineID')
        AssetID = request.POST.get('AssetID')
        if request.method == 'POST':
            fromdate = request.POST.get('dateStart')
            print('type of fdate', fromdate)
            todate = request.POST.get('dateEnd')
            print('type of tdate', todate)
            # MachineID = request.POST.get('MachineID')
            print('type of id', MachineID)
            # assetidtemp = AddMachine.objects.get(pk=MachineID)
            # print('type of asset', assetidtemp)
            # AssetID = assetidtemp.assetid
            # filter(machineID=machineID)
            # print('The Type of fromdate', AssetID)
            context1 = timeseriesshow.ShowTimeValueSeries()
            context1.newentityid = 'ce5ad34e00ff46c48c7bb2e27fec7c49'
        else:
            tempto = datetime.now()
            tempfrom = tempto - timedelta(hours=360)
            temptoString = datetime.strftime(tempto, '%Y-%m-%dT%H:%M:%SZ')
            tempfromString = datetime.strftime(tempfrom, '%Y-%m-%dT%H:%M:%SZ')
            fromdate = tempfromString
            todate = temptoString
            print("Normal From", fromdate)
            context1 = timeseriesshow.ShowTimeValueSeries()
            context1.newentityid = 'ce5ad34e00ff46c48c7bb2e27fec7c49'

        context1.property_set_name = 'CJV600'
        context1._from = fromdate
        context1.to = todate
        context = timeseriesshow.ShowTimeValueSeries.showplot(self=context1)
        Availability = context['Availability']
        Quality = context['Quality']
        Performance = context['Performance']
        OperatingOnTime = context['OperatingOnTime']
        BreakdownOnTime = context['BreakdownOnTime']
        theIdealBatchArr = context['theIdealBatchArr']
        ActualBatchPer = context['ActualBatchPer']
        QualGoodBatch = context['QualGoodBatch']
        QualBadBatch = context['QualBadBatch']
        content ={'Availability':Availability,'Quality':Quality,'Performance':Performance,
                  'OperatingOnTime':OperatingOnTime,'BreakdownOnTime':BreakdownOnTime,
                  'theIdealBatchArr':theIdealBatchArr,'ActualBatchPer':ActualBatchPer,'MachineID':MachineID,'AssetID':AssetID,
                  'QualGoodBatch': QualGoodBatch, 'QualBadBatch': QualBadBatch,'fromdate1':fromdate,'todate1':todate}
        pdf = render_to_pdf('pdf.html',content)
        return HttpResponse(pdf, content_type='application/pdf')


# Automaticly downloads to PDF file
class DownloadPDF(View):
    def get(self, request, *args, **kwargs):
        if request.method == 'POST':
            fromdate = request.POST.get('dateStart')
            print('type of fdate', fromdate)
            todate = request.POST.get('dateEnd')
            print('type of tdate', todate)
            MachineID = request.POST.get('MachineID')
            print('type of id', MachineID)
            assetidtemp = AddMachine.objects.get(pk=MachineID)
            print('type of asset', assetidtemp)
            AssetID = assetidtemp.AssetID
            # filter(machineID=machineID)
            print('The Type of fromdate', AssetID)
            context1 = timeseriesshow.ShowTimeValueSeries()
            context1.newentityid = AssetID

        else:
            tempto = datetime.now()
            tempfrom = tempto - timedelta(hours=360)
            temptoString = datetime.strftime(tempto, '%Y-%m-%dT%H:%M:%SZ')
            tempfromString = datetime.strftime(tempfrom, '%Y-%m-%dT%H:%M:%SZ')
            fromdate = tempfromString
            todate = temptoString
            print("Normal From", fromdate)
            context1 = timeseriesshow.ShowTimeValueSeries()
            context1.newentityid = 'ce5ad34e00ff46c48c7bb2e27fec7c49'
        context1.property_set_name = 'CJV600'
        context1._from = fromdate
        context1.to = todate
        context = timeseriesshow.ShowTimeValueSeries.showplot(self=context1)
        Availability = context['Availability']
        Quality = context['Quality']
        Performance = context['Performance']
        OperatingOnTime = context['OperatingOnTime']
        BreakdownOnTime = context['BreakdownOnTime']
        theIdealBatchArr = context['theIdealBatchArr']
        ActualBatchPer = context['ActualBatchPer']
        QualGoodBatch = context['QualGoodBatch']
        QualBadBatch = context['QualBadBatch']
        content ={'Availability':Availability,'Quality':Quality,'Performance':Performance,
                  'OperatingOnTime':OperatingOnTime,'BreakdownOnTime':BreakdownOnTime,
                  'theIdealBatchArr':theIdealBatchArr,'ActualBatchPer':ActualBatchPer,
                  'QualGoodBatch': QualGoodBatch, 'QualBadBatch': QualBadBatch,}
        pdf = render_to_pdf('pdf.html',content)
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = 'Invoice_%s.pdf' % ("12341231")
        content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response

@login_required(login_url='login')
def edit(request, MachineID):
    editMachineID = AddMachine.objects.get(MachineID=MachineID)
    return render(request,'edit.html',{'editdata':editMachineID,'date':x})

def update(request, MachineID):
    updateMachineID = AddMachine.objects.get(MachineID = MachineID)
    form = AddMachine(request.POST,instance=updateMachineID)
    if form.is_valid():
        form.save(commit=True)
        return redirect('/machines')
    return render (request, 'edit.html',{'updatedata':updateMachineID,'date':x})

def destroy(request,MachineID):
    MachineID = AddMachine.objects.get(MachineID=MachineID)
    MachineID.delete()
    results = AddMachine.objects.all()
    return redirect('/machines', {'data':results,'date':x})