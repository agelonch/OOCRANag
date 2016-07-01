from django.contrib import admin
from .models import Nvf
from .models import Deployment

class DeploymentModelAdmin(admin.ModelAdmin):
	list_display = ["name","update","timestamp"]
	list_display_links = ["update"]
	list_filter = ["update","timestamp"]
	list_editable = ["name"]
	search_fields = ["name"]
	class Meta:
		model = Deployment

admin.site.register(Deployment, DeploymentModelAdmin)

class NvfModelAdmin(admin.ModelAdmin):
	list_display = ["name","update","timestamp"]
	list_display_links = ["update"]
	list_filter = ["update","timestamp"]
	list_editable = ["name"]
	search_fields = ["name"]
	class Meta:
		model = Nvf

admin.site.register(Nvf, NvfModelAdmin)

