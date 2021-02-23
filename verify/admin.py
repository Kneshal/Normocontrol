from django.contrib import admin

from .models import CheckOut


class CheckAdmin(admin.ModelAdmin):
    list_display = ('pk', 'student', 'docx_file', 'check_date',)
    search_fields = ('student',)
    list_filter = ('student',)
    empty_value_display = "-пусто-"


admin.site.register(CheckOut, CheckAdmin)
