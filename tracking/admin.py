from django.contrib import admin
from .models import DeviceLocation

@admin.register(DeviceLocation)
class DeviceLocationAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'latitude', 'longitude', 'timestamp')
    list_filter = ('device_id',)
