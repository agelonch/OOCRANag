from django.contrib import admin
from .models import Bts, Area, OArea

class BtsModelAdmin(admin.ModelAdmin):
	list_display = ["ip","update","timestamp"]
	list_display_links = ["update"]
	list_filter = ["update","timestamp"]
	list_editable = ["ip"]
	search_fields = ["ip"]
	class Meta:
		model = Bts

admin.site.register(Bts, BtsModelAdmin)

class AreaModelAdmin(admin.ModelAdmin):
	list_display = ["name","update","timestamp"]
	list_display_links = ["update"]
	list_filter = ["update","timestamp"]
	list_editable = ["name"]
	search_fields = ["name"]
	class Meta:
		model = Area

admin.site.register(Area, AreaModelAdmin)

class OAreaModelAdmin(admin.ModelAdmin):
	list_display = ["name","update","timestamp"]
	list_display_links = ["update"]
	list_filter = ["update","timestamp"]
	list_editable = ["name"]
	search_fields = ["name"]
	class Meta:
		model = OArea

admin.site.register(OArea, OAreaModelAdmin)