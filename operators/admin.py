from django.contrib import admin

from .models import Operator

class OperatorModelAdmin(admin.ModelAdmin):
	list_display = ["name"]
	#list_filter = ["update"]
	list_editable = ["name"]
	search_fields = ["name"]
	class Meta:
		model = Operator

admin.site.register(Operator, OperatorModelAdmin)
