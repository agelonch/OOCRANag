from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Bts, Area, OArea
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import AreaForm
from operators.models import Operator
from django.contrib import messages
from django.core.urlresolvers import reverse
import sys, os

from .orchestration import scenarioCreate
from Vnfm.structura import infrastructure

from django.contrib.auth.decorators import login_required


def scenarios_list(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    areas = Area.objects.all()
    paginator = Paginator(areas, 5)
    page = request.GET.get('page')
    print os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    try:
        areas = paginator.page(page)
    except PageNotAnInteger:
        areas = paginator.page(1)
    except EmptyPage:
        areas = paginator.page(paginator.num_pages)
    context = {
        "user": request.user.username,
        "admin": request.user,
        "areas": areas,
    }
    return render(request, "scenarios/scenarios_list.html", context)


def area_detail(request, id=None):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    area = get_object_or_404(Area, id=id)
    context = {
        "scenario": area,
        "btss": Bts.objects.filter(area__name=area.name)
    }
    return render(request, "scenarios/scenario_detail.html", context)


def area_create(request):
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse('login'))

    form = AreaForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        area = form.save(commit=False)
        area.save()
        btss = scenarioCreate(form.cleaned_data.get("file"))

        for vm in btss:
            bts = Bts(ip=vm['ip'], lat=vm['lat'], longi=vm['long'], radio=vm['r_max'], name=vm['name'],
                      neighbor=vm['neighbor'], BW=vm['bw'], area=area)
            bts.save()

        operators = Operator.objects.filter()
        for operator in operators:
            infrastructure(operator, form.cleaned_data.get("name"),form.cleaned_data.get("description"))
            oarea= OArea(name=form.cleaned_data.get("name"),
                         propietario=operator,
                         area=area)
            oarea.save()

        messages.success(request, "Area successfully created!", extra_tags="alert alert-success")
        return redirect("scenarios:list")
    context = {
        "user": request.user.username,
        "form": form,
    }
    return render(request, "scenarios/scenario_form.html", context)


def scenario_delete(request, id=None):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    instance = get_object_or_404(OArea, id=id)
    instance.delete()
    return redirect("scenarios:list")
