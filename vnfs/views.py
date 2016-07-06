from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Vnf
from operators.models import Operator
from .forms import VnfForm
from django.contrib import messages
from django.core.urlresolvers import reverse
from .authentication import auth

#from aloeoCLI.VNFM.vnfs.vnfs import create

from django.contrib.auth.decorators import login_required


def vnf_list(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    queryset_list = Vnf.objects.filter(operador__name=request.user.username)

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
    return render(request, "vnfs/vnf_list.html", context)


def vnf_create(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    form = VnfForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.operador = get_object_or_404(Operator, name=request.user.username)
        # results = create(auth(request.user.username),request.user.username,form.cleaned_data.get("name"), form.cleaned_data.get("description"))
        messages.success(request, "Successfully created!", extra_tags="alert alert-success")
        # instance.cpu = results[0][0]
        # instance.ram = results[0][1]
        instance.save()
        return redirect("vnfs:list")
    context = {
        "user": request.user.username,
        "form": form,
    }
    return render(request, "vnfs/vnf_form.html", context)


def vnf_delete(request, id=None):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    instance = get_object_or_404(Vnf, id=id)
    instance.delete()
    messages.success(request, "VNF successfully deleted!", extra_tags="alert alert-success")
    return redirect("vnfs:list")


def vnf_detail(request, id=None):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    instance = get_object_or_404(Vnf, id=id)
    context = {
        "user": request.user.username,
        "vnf": instance,

    }
    return render(request, "vnfs/vnf_detail.html", context)


def vnf_edit(request, id=None):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    instance = get_object_or_404(Vnf, id=id)
    form = VnfForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Successfully update!", extra_tags="some-tag")
        return redirect("vnfs:list")
    context = {
        "user": request.user.username,
        "instance": instance,
        "form": form,
    }
    return render(request, "vnfs/vnf_form.html", context)
