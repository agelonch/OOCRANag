from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import SettingsForm
from .models import Operator


# Create your views here.
def settings(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    operator = get_object_or_404(Operator, name=request.user.username)
    mcs = operator.mcs
    table = []
    if mcs != "":
        i = 0
        for row in mcs:
            row = row.split('\n')[0]
            value = [row.split(',')[0], row.split(',')[1], row.split(',')[2]]
            table.append(value)
            i += 1

    context = {
        "user": request.user.username,
        "operator": operator,
        "mcs": table,
    }
    return render(request, "operators/settings.html", context)


def mcs(request, id=id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))

    form = SettingsForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        mcs = form.save(commit=False)
        mcs.save()

    context = {
        "user": request.user.username,
        "form": form,
    }
    return render(request, "operators/mcs_form.html", context)
