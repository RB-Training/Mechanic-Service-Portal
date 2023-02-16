from django.contrib import admin
from portal.models import NewVehicle,rule_engine,Bikename
# Register your models here.

admin.site.register(Bikename)

admin.site.register(NewVehicle)

admin.site.register(rule_engine)
