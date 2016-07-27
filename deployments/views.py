from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Deployment, Nvf, Channel
from .forms import DeploymentForm, AddForm
from django.contrib import messages
from django.core.urlresolvers import reverse
from vnfs.models import Vnf
from vnfs.forms import VnfForm
from operators.models import Operator
from scenarios.models import Bts, Area, OArea
from users.models import Client
import os, time
from django.shortcuts import render
from Vnfm.deployments import create, delete, create_virtual
from VIM.OpenStack.nova import nova
from VIM.OpenStack.ceilometer.ceilometer import statistics
from time import time
from .orchestration import planification_DL, planification_UL, rb_offer, price, list_bs


def deployment_list(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    queryset_list = Deployment.objects.filter(propietario__name=request.user.username).filter(start__isnull=False)
    areas = OArea.objects.filter(propietario__name=request.user.username)

    paginator = Paginator(queryset_list, 5)
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    context = {
        "user": request.user.username,
        "areas": areas,
        "object_list": queryset,
    }
    return render(request, "deployments/deployment_list.html", context)


def deployment_create(request, id=None):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    #########################################3
    tiempo_inicial = time()
    #########################################3

    form = DeploymentForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        deploy = form.save(commit=False)
        ##########no repetir deploy####
        search_depl = Deployment.objects.filter(name=form.cleaned_data.get("name"))

        if len(search_depl):
            messages.success(request, "Do not repeat the deployment name!", extra_tags="alert alert-success")
            context = {
                "user": request.user.username,
                "form": form,
            }
            return render(request, "deployments/add_catalog.html", context)

        deploy.propietario = get_object_or_404(Operator,name=request.user.username)
        oarea = get_object_or_404(OArea, pk=id)
        deploy.area = oarea
        deploy.save()

        bts_list = []
        channels = []
        communications = []

        lista = list_bs(form.cleaned_data.get("file"))
        for element in lista:
            bts = get_object_or_404(Bts, ip=element['ip'])
            nvf = Nvf(name=form.cleaned_data.get("name") + '-' + element['ip'],
                      vnf=Vnf.objects.filter(name=element['vnf']).filter(operador__name=request.user.username)[0],
                      BW_DL=int(element['rb']),
                      BW_UL=int(element['rb']),
                      bts=bts,
                      deploy=deploy,
                      operator=get_object_or_404(Operator, name=request.user.username),
                      Pt=element['pt'],
                      type=element['type'])

            planification_DL(nvf, deploy.propietario)
            planification_UL(nvf)
            nvf.radio = nvf.bts.max_dist(int(element['pt']), nvf.freC_DL)
            deploy.propietario.save()
            bts.save()
            nvf.save()
            deploy.rb += nvf.rb
            deploy.price = deploy.price + price(nvf, nvf.BW_DL, deploy)

            if str(element['type']) == "real":
                bts_list.append(nvf)
            if str(element['type']) == "virtual":
                bts_list.append(nvf)
                print element['channel']
                channel = get_object_or_404(Vnf, name=element['channel'])
                print channel
                channels.append(channel)
                subs = get_object_or_404(Vnf, name=element['subs'])
                communications.append(subs)
                print subs
                print channel
            if str(element['type']) == "simulation":
                print "simulat"

        oarea.price += deploy.price
        oarea.rb_offer = rb_offer(str(deploy.rb), oarea.rb_offer, int(str(deploy.start).split(':')[0]),
                                  int(str(deploy.stop).split(':')[0]), "suma")
        oarea.save()
        deploy.save()

        if form.cleaned_data.get("name") is "virtual":
            create_virtual(get_object_or_404(Operator, name=request.user.username),
                   form.cleaned_data.get("name"),
                   form.cleaned_data.get("description"),
                   bts_list, channels, communications)
        else:
            create(get_object_or_404(Operator, name=request.user.username),
                   form.cleaned_data.get("name"),
                   form.cleaned_data.get("description"),
                   bts_list, channels, communications)

        ########################################3
        tiempo_final = time()
        tiempo_ejecucion = tiempo_final - tiempo_inicial
        print 'El tiempo de ejecucion fue:',tiempo_ejecucion
        #########################################3

        messages.success(request, "Deployment successfully created!", extra_tags="alert alert-success")
        return redirect("deployments:list")
    context = {
        "user": request.user.username,
        "form": form,
    }
    return render(request, "deployments/deployment_form.html", context)


def deployment_edit(request, id=None):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    instance = get_object_or_404(Deployment, id=id)
    form = DeploymentForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Successfully update!", extra_tags="some-tag")
        return redirect("deployments:list")
    context = {
        "user": request.user.username,
        "instance": instance,
        "form": form,
    }
    return render(request, "deployments/deployment_form.html", context)


def deployment_delete(request, id=None):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    deploy = get_object_or_404(Deployment, pk=id)
    area = OArea.objects.filter(name=deploy.area).filter(propietario__name=request.user.username)[0]
    area.price -= deploy.price

    if deploy.name == area.name:
        t = int(str(time.strftime("%H")).split(':')[0])
        area.rb_offer = [0 for x in area.forecast[1:-1].split(',')]

        area.save()
        deploy.delete()

    elif deploy.name != area.name:
        area.rb_offer = rb_offer(str(deploy.rb), area.rb_offer, int(str(deploy.start).split(':')[0]),
                                 int(str(deploy.stop).split(':')[0]), "resta")
        area.save()
        nvfs = Nvf.objects.filter(deploy__name=deploy.name).filter(operator__name=request.user.username)
        for nvf in nvfs:
            bts = get_object_or_404(Bts, ip=nvf.bts.ip)
            lista = bts.freCs.split('/')
            lista.remove(str(nvf.freC_DL - nvf.BW_DL / 2) + "-" + str(nvf.freC_DL + nvf.BW_DL / 2))
            lista.remove(str(nvf.freC_UL - nvf.BW_UL / 2) + "-" + str(nvf.freC_UL + nvf.BW_UL / 2))
            bts.freCs = '/'.join(lista)
            bts.save()

        delete(deploy.name, deploy.propietario)
        deploy.delete()
    messages.success(request, "Deployment successfully deleted!", extra_tags="alert alert-success")
    return redirect("deployments:list")


def deployment_detail(request, id=None):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    instance = get_object_or_404(Deployment, id=id)
    scenario = get_object_or_404(Area, name=instance.area)
    clients = Client.objects.filter(deploy__name=instance.name)
    operator = get_object_or_404(Operator, name=request.user.username)

    frecs = ["#5ED3F8","#E325B9","#FFFF00"]

    context = {
        "user": operator,
        "deployment": instance,
        "scenario": scenario,
        "btss": Bts.objects.filter(area=scenario),
        "nvfs": Nvf.objects.filter(deploy=instance),
        "frecs":frecs,
        "clients": clients,
    }
    return render(request, "deployments/deployment_detail.html", context)


def nvf_list(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    queryset_list = Nvf.objects.filter(operator__name=request.user.username)

    paginator = Paginator(queryset_list, 5)
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    context = {
        "user": request.user.username,
        "object_list": queryset,
    }
    return render(request, "nvfs/nvf_list.html", context)


def nvf_detail(request, id=None):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    instance = get_object_or_404(Nvf, id=id)
    clients = Client.objects.filter(nvf__name=instance.name)
    name = nova.find_vm(instance.name)

    (cpu, ram) = statistics(name.id,instance.name)

    # instance.static_labels += str(time.strftime("%H:%M:%S")) + '/'
    # instance.static_cpu += str(cpu) + '/'
    # instance.static_ram += str(ram) + '/'

    instance.save()
    context = {
        "user": request.user.username,
        "nvf": instance,
        "clients": clients,
        "labels": str(instance.static_labels).split('/')[1:-1],
        "cpu": map(int, str(instance.static_cpu).split('/')[1:-1]),
        "ram": str(instance.static_ram).split('/')[1:-1],
    }
    return render(request, "nvfs/nvf_detail.html", context)


def canals_list(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    queryset_list = Vnf.objects.filter(operador__name=request.user.username).filter(type="channel")
    #queryset_list = Channel.objects.filter(propietario__name=request.user.username)

    paginator = Paginator(queryset_list, 5)
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    context = {
        "user": request.user.username,
        "object_list": queryset,
    }

    return render(request, "canals/canals_list.html", context)


def channel_create(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    form = VnfForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.operador = get_object_or_404(Operator, name=request.user.username)
        instance.type="channel"
        messages.success(request, "Channel successfully created!", extra_tags="alert alert-success")
        instance.save()

        '''create_channel(get_object_or_404(Operator, name=request.user.username),
               form.cleaned_data.get("name"),
               form.cleaned_data.get("description"),
               instance)'''

        return redirect("deployments:canals")
    context = {
        "user": request.user.username,
        "form": form,
    }
    return render(request, "canals/channel_form.html", context)


def channel_detail(request, id=None):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    instance = get_object_or_404(Channel, id=id)
    context = {
        "user": request.user.username,
        "vnf": instance,
    }
    return render(request, "canals/channel_detail.html", context)


def channel_delete(request, id=None):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    instance = get_object_or_404(Vnf, id=id)
    instance.delete()
    messages.success(request, "Channel successfully deleted!", extra_tags="alert alert-success")
    return redirect("deployments:canals")


def autodeploy(request, id=None):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    area = get_object_or_404(OArea, pk=id)
    auto_deploy = Deployment(area=area, name=area.name, start="00:00", stop="23:59",
                             propietario=get_object_or_404(Operator, name=request.user.username))
    catalog = Deployment.objects.filter(propietario__name=request.user.username).filter(auto=True)
    rbs = [int(x) for x in area.forecast[1:-1].split(',')]
    catalog = [int(x.name) for x in catalog]

    cont = 0
    for deploy in rbs:
        select = 200000000
        for i in catalog:
            if i == deploy:
                select = i
                continue
            if i > deploy and i < select:
                select = i
                continue
        rbs[cont] = select
        cat_selected = get_object_or_404(Deployment, name=str(select))
        auto_deploy.price = auto_deploy.price + int(cat_selected.price)
        cont += 1

    rbs = [str(x) for x in rbs]
    rbs = ','.join(rbs)
    area.rb_offer = "[" + rbs + "]"
    area.price += auto_deploy.price
    area.save()

    auto_deploy.save()
    messages.success(request, "Auto-deployment launched!", extra_tags="alert alert-success")
    return redirect("deployments:list")


def catalog(request, id=None):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    queryset_list = Deployment.objects.filter(propietario__name=request.user.username).filter(start=None)
    areas = Area.objects.all()

    paginator = Paginator(queryset_list, 5)
    page = request.GET.get('page')
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    context = {
        "user": request.user.username,
        "areas": areas,
        "object_list": queryset,
    }
    return render(request, "deployments/catalog.html", context)


def add_catalog(request, id=None):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    form = AddForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        deploy = form.save(commit=False)
        deploy.auto = True
        deploy.propietario = get_object_or_404(Operator, name=request.user.username)
        area = get_object_or_404(OArea, pk=id)
        search_depl = Deployment.objects.filter(name=form.cleaned_data.get("name"))

        if len(search_depl):
            messages.success(request, "Do not repeate the deployment name!", extra_tags="alert alert-danger")
            context = {
                "user": request.user.username,
                "form": form,
            }
            return render(request, "deployments/add_catalog.html", context)

        deploy.area = area
        deploy.save()

        lista = list_bs(form.cleaned_data.get("file"))
        for element in lista:
            nvf = Nvf(name=form.cleaned_data.get("name") + '-' + element['ip'],
                      vnf=get_object_or_404(Vnf, name=element['vnf']),
                      BW_DL=int(element['rb']),
                      BW_UL=int(element['rb']),
                      bts=get_object_or_404(Bts, ip=element['ip']),
                      deploy=deploy,
                      static_labels='/',
                      static_cpu='/',
                      static_ram='/',
                      operator=get_object_or_404(Operator, name=request.user.username),
                      Pt=element['pt'])

            #deploy.price = deploy.price + price(nvf, nvf.BW_DL, deploy)

            nvf.radio = nvf.bts.max_dist(int(element['pt']), 2400700000)
            nvf.save()

        area.save()
        deploy.save()
        messages.success(request, "Deployment added to the catalog!", extra_tags="alert alert-success")
        return redirect("deployments:list")
    context = {
        "user": request.user.username,
        "form": form,
    }
    return render(request, "deployments/add_catalog.html", context)


def del_catalog(request, id=None, id_deploy=None):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    deploy = get_object_or_404(Deployment, pk=id_deploy)
    nvfs = Nvf.objects.filter(deploy__name=deploy.name)
    for nvf in nvfs:
        nvf.delete()

    deploy.delete()

    messages.success(request, "Deployment deleted!", extra_tags="alert alert-success")
    return redirect("deployments:list")
