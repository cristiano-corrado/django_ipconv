from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from .forms import InputForm
from .utils import sortcidr
from .models import IPChaos, IPUnpacked
import random,string
from django.conf import settings as djangoSettings

def home(request):

    ipsave = IPChaos()

    if request.method == 'POST':
        form = InputForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data.get("ipinsert")
            cleandata = data.replace("\n"," ").replace("\r"," ")
            validated = sortcidr.evaluateBadStrings(cleandata)

            for elem in validated:
                model = sortcidr.getmodel(elem)
                if model == 'netmask':
                    ipbloc = elem.split("-")
                    if ( sortcidr.validateIP(ipbloc[0]) and sortcidr.validateIP(ipbloc[1]) ):
                        ipsave.pk = None
                        ipsave.string=elem
                        ipsave.type=sortcidr.getmodel(elem)
                        ipsave.save()
                elif model == 'cidr':
                    if sortcidr.validateIP(elem):
                        ipsave.pk = None
                        ipsave.string=elem
                        ipsave.type=sortcidr.getmodel(elem)
                        ipsave.save()
                elif model == 'ip':
                        ipsave.pk = None
                        ipsave.string=elem
                        ipsave.type=sortcidr.getmodel(elem)
                        ipsave.save()
                else:
                    ipsave.pk = None
                    ipsave.string=elem
                    ipsave.type = "Not Valid"
                    ipsave.save()

        ipunpacked = set()

        for elements in IPChaos.objects.all():
            if elements.type != 'Not Valid':
                if elements.type == 'cidr':
                    for ip in sortcidr.iscidr(elements.string):
                        ipunpacked.add(str(ip))
                if elements.type == 'netmask':
                    getnet = sortcidr.getcidrfromblock(elements.string)
                    for net in getnet:
                        for ip in sortcidr.iscidr(net):
                            ipunpacked.add(str(ip))
                if elements.type == 'ip':
                    ipunpacked.add(str(elements.string))

        filterQuery = IPChaos.objects.filter(type='Not Valid').all()
        invalid = [ x for x in filterQuery ]
        for row in IPChaos.objects.all():
            row.delete()

        filename=''.join(random.choice(string.ascii_letters) for i in range(10))
        with open(djangoSettings.STATICFILES_DIRS[0]+'/downloads/{}.txt'.format(filename),'w') as ipwriter:
            print(str())
            ipwriter.write("{}".format(",".join([x for x in sortcidr.sort_ip_list(ipunpacked)])))

        return render(request,'results.html',{'downloadFile':filename+'.txt','results': [ x for x in sortcidr.sort_ip_list(ipunpacked) ],'invalid':invalid})

    else:
        form = InputForm()

    return render(request,'home.html',{'form' : form})
