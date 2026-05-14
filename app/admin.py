from django.contrib import admin
from .models import DailyAttendance

@admin.register(DailyAttendance)
class DailyAttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'punch_in', 'punch_out')
    list_filter = ('user', 'date')
