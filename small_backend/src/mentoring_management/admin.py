from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm
from unfold.admin import ModelAdmin
from simple_history.admin import SimpleHistoryAdmin
from .autocomplete.forms import MentorshipAssignmentForm


@admin.register(MentorshipAssignment)
class MentorshipAssignmentAdmin(ModelAdmin, SimpleHistoryAdmin, ImportExportModelAdmin):
    form = MentorshipAssignmentForm
    list_display = ('employee', 'mentor', 'manager', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'mentor', 'manager', 'employee')
    search_fields = ('employee', 'mentor', 'manager')
    readonly_fields = ('updated_at', 'created_at')
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_filter_submit = True
    list_per_page = 25
    list_max_show_all = 1000
