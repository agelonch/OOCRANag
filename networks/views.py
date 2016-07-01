from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from .models import Controller
import keystoneclient.v2_0.client as k_client
from .forms import ControllerForm
from operators.models import Operator
from .authentication import auth
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#import aloeoCLI.tasks.configuration as conf
#from aloeoCLI.functions.creations import launchController

# Create your views here.
def network_list(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('login'))
		
	queryset_list = Controller.objects.filter(operator__name=request.user.username)

	'''keystone = k_client.Client(auth_url=conf.get_endpoint_keystone(), 
                              username='operator1',
                              password='odissey09', 
                              tenant_name='operator1')

   	auth_token = keystone.auth_token
   	print auth_token'''

	paginator = Paginator(queryset_list,5)
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
	return render(request, "networks/network_list.html", context)

def network_create(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('login'))
		
	form = ControllerForm(request.POST or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.operator = get_object_or_404(Operator, name = request.user.username)
		instance.save()
		launchController(auth(request.user.username), instance.name, request.user.username)
		#messages.success(request,"Successfully created!")
		return redirect("networks:list")
	context = {
		"user": request.user.username,
		"form": form,
	}
	return render(request, "networks/network_form.html", context)

def network_delete(request,id=None):
	if not request.user.is_authenticated():
		return HttpResponseRedirect(reverse('login'))

	instance = get_object_or_404(Controller, id=id)
	instance.delete()
	#messages.success(request,"Successfully deleted!")
	return redirect("networks:list")