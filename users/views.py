from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .forms import VnfForm
from .models import Client
from vnfs.models import Vnf
from deployments.models import Nvf
from django.contrib import messages
from operators.models import Operator
from .orchestration import optim, distance, mcs


def users_list(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    queryset_list = Vnf.objects.filter(operador__name=request.user.username).filter(type="subscriber")
    #queryset_list = Client.objects.filter(operator__name=request.user.username).

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
    return render(request, "users/users_list.html", context)


'''def users_create(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    form = UserForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        lista = optim(form.cleaned_data.get("file"))
        for element in lista:
            nvf = get_object_or_404(Nvf, name=form.cleaned_data.get("name") + '-' + element['bts'])
            nvf.users += 1
            nvf.load = nvf.load+','+element['rb']
            cli = Client(name=form.cleaned_data.get("name") + '-' + element['name'],
                         rb=element['rb'],
                         lat=element['lat'],
                         mcs=mcs(element['mcs'], get_object_or_404(Operator, name=request.user.username)),
                         longi=element['long'],
                         deploy=get_object_or_404(Deployment, name=form.cleaned_data.get("name")),
                         operator=get_object_or_404(Operator, name=request.user.username),
                         nvf=nvf,
                         dist=distance(float(element['lat']), float(element['long']), float(nvf.bts.get_lat()),
                                       float(nvf.bts.get_longi())))

            if distance(float(element['lat']), float(element['long']), float(nvf.bts.get_lat()),
                        float(nvf.bts.get_longi())) > float(nvf.radio):
                nvf.radio = str(distance(float(element['lat']), float(element['long']), float(nvf.bts.get_lat()),
                                         float(nvf.bts.get_longi())))

            cli.pt_dl = nvf.bts.propagation(cli.dist, nvf.freC_DL, 'dl')
            cli.pt_ul = nvf.bts.propagation(cli.dist, nvf.freC_UL, 'ul')
            nvf.save()
            cli.save()

        messages.success(request, "Subscribers launched!", extra_tags="alert alert-success")
        return redirect("users:list")
    context = {
        "user": request.user.username,
        "form": form,
        "deploys": Deployment.objects.filter(propietario__name=request.user.username),
    }
    return render(request, "users/users_form.html", context)
'''
def users_create(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    form = VnfForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.operador = get_object_or_404(Operator, name=request.user.username)
        instance.type = "subscriber"
        messages.success(request, "Successfully created!", extra_tags="alert alert-success")
        instance.save()
        return redirect("users:list")
    context = {
        "user": request.user.username,
        "form": form,
    }
    return render(request, "users/vnf_form.html", context)

def users_delete(request, id=None):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    instance = get_object_or_404(Vnf, id=id)
    instance.delete()
    messages.success(request, "Subscriber successfully deleted!", extra_tags="alert alert-success")
    return redirect("users:list")
