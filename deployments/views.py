from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Deployment, Nvf
from .forms import DeploymentForm, AddForm
from django.contrib import messages
from django.core.urlresolvers import reverse
from vnfs.models import Vnf
from operators.models import Operator
from scenarios.models import Bts, Area, OArea
from users.models import Client
import os, time
from django.shortcuts import render
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

    form = DeploymentForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        deploy = form.save(commit=False)
        deploy.propietario = get_object_or_404(Operator, name=request.user.username)
        deploy.start = time.strftime("%H:00")
        oarea = get_object_or_404(OArea, pk=id)
        deploy.area = oarea
        deploy.save()

        nvfs = []
        enod_conf = {}

        lista = list_bs(form.cleaned_data.get("file"))
        for element in lista:
            bts = get_object_or_404(Bts, ip=element['ip'])
            nvf = Nvf(name=form.cleaned_data.get("name") + '-' + element['ip'],
                      vnf=Vnf.objects.filter(name=element['vnf']).filter(operador__name=request.user.username)[0],
                      BW_DL=int(element['rb']),
                      BW_UL=int(element['rb']),
                      bts=bts,
                      deploy=deploy,
                      static_labels='/',
                      static_cpu='/',
                      static_ram='/',
                      operator=get_object_or_404(Operator, name=request.user.username),
                      Pt=element['pt'])

            planification_DL(nvf, Bts.objects.all())
            planification_UL(nvf, Bts.objects.all())
            nvf.radio = nvf.bts.max_dist(int(element['pt']), nvf.freC_DL)
            bts.save()
            nvf.save()
            deploy.rb += nvf.rb_offer
            # deploy.price = deploy.price + price(nvf, nvf.BW_DL, deploy)

            enod_conf[element['ip']] = {"BW_DL": nvf.BW_UL, "BW_UL": nvf.BW_UL, "Pt": element['pt']}
            nvfs.append(nvf)

        oarea.price += deploy.price
        oarea.rb_offer = rb_offer(str(deploy.rb), oarea.rb_offer, int(str(deploy.start).split(':')[0]),
                                  int(str(deploy.stop).split(':')[0]), "suma")
        oarea.save()
        deploy.save()

        # create(auth(request.user.username), request.user.username, form.cleaned_data.get("name"), form.cleaned_data.get("description"), nvfs)

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
            print lista
            lista.remove(str(nvf.freC_DL - nvf.BW_DL / 2) + "-" + str(nvf.freC_DL + nvf.BW_DL / 2))
            lista.remove(str(nvf.freC_UL - nvf.BW_UL / 2) + "-" + str(nvf.freC_UL + nvf.BW_UL / 2))
            print lista
            bts.freCs = '/'.join(lista)
            bts.save()

        # delete(auth(request.user.username), request.user.username, deploy.name)
        deploy.delete()
    messages.success(request, "Successfully deleted!")
    return redirect("deployments:list")


def deployment_detail(request, id=None):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    instance = get_object_or_404(Deployment, id=id)
    scenario = get_object_or_404(Area, name=instance.area)
    clients = Client.objects.filter(deploy__name=instance.name)
    operator = get_object_or_404(Operator, name=request.user.username)

    context = {
        "user": operator,
        "deployment": instance,
        "scenario": scenario,
        "btss": Bts.objects.filter(area=scenario),
        "nvfs": Nvf.objects.filter(deploy=instance),
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
    # name = nova.find_vm(instance.name)

    # (cpu, ram) = statistics(name.id,instance.name)

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

    return render(request, "canals/canals_list.html")


def autodeploy(request, id=None):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    area = get_object_or_404(Area, pk=id)
    auto_deploy = Deployment(area=area, name=area.name, start="00:00", stop="23:59",
                             propietario=get_object_or_404(Operator, name=request.user.username))
    catalog = Deployment.objects.filter(propietario__name=request.user.username).filter(start=None)
    rbs = [int(x) for x in area.forecast[1:-1].split(',')]
    catalog = [int(x.name) for x in catalog]

    cont = 0
    for deploy in rbs:
        select = 9999999999999999
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
        deploy.propietario = get_object_or_404(Operator, name=request.user.username)
        area = get_object_or_404(OArea, pk=id)
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

            deploy.price = deploy.price + price(nvf, nvf.BW_DL, deploy)
            nvf.save()

        area.save()
        deploy.save()
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

    messages.success(request, "Successfully deleted!")
    return redirect("deployments:list")
