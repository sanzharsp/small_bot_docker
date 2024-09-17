from django.contrib import admin, messages
from unfold.admin import ModelAdmin, StackedInline
from unfold.widgets import UnfoldAdminSelectWidget, UnfoldAdminTextInputWidget

from .models import *
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm
from simple_history.admin import SimpleHistoryAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from unfold.decorators import display
from django_celery_beat.models import (
    ClockedSchedule,
    CrontabSchedule,
    IntervalSchedule,
    PeriodicTask,
    SolarSchedule,
)
from django.contrib.auth.models import Group
from django_celery_beat.admin import PeriodicTaskAdmin as BasePeriodicTaskAdmin
from django_celery_beat.admin import PeriodicTaskForm, TaskSelectWidget
from django_celery_beat.admin import ClockedScheduleAdmin as BaseClockedScheduleAdmin
from django_celery_beat.admin import CrontabScheduleAdmin as BaseCrontabScheduleAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from .models import Role
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# unregister celery models
admin.site.unregister(PeriodicTask)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)
admin.site.unregister(User)

# unregister django models
admin.site.unregister(Group)



class ModerationForCityInlines(StackedInline):
    model = ModerationForCity
    extra = 1
    autocomplete_fields = ('city',)


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin, ModelAdmin):
    inlines = (ModerationForCityInlines, )
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm


class UnfoldTaskSelectWidget(UnfoldAdminSelectWidget, TaskSelectWidget):
    pass


class UnfoldPeriodicTaskForm(PeriodicTaskForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["task"].widget = UnfoldAdminTextInputWidget()
        self.fields["regtask"].widget = UnfoldTaskSelectWidget()


@admin.register(PeriodicTask)
class PeriodicTaskAdmin(BasePeriodicTaskAdmin, ModelAdmin):
    form = UnfoldPeriodicTaskForm


@admin.register(IntervalSchedule)
class IntervalScheduleAdmin(ModelAdmin):
    pass


@admin.register(CrontabSchedule)
class CrontabScheduleAdmin(BaseCrontabScheduleAdmin, ModelAdmin):
    pass


@admin.register(SolarSchedule)
class SolarScheduleAdmin(ModelAdmin):
    pass


@admin.register(ClockedSchedule)
class ClockedScheduleAdmin(BaseClockedScheduleAdmin, ModelAdmin):
    pass


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        messages.warning(
            request,
            _(
                "This model for administering user rights"
            ),
        )

        return super().changelist_view(request, extra_context=extra_context)


@admin.register(CustomUser)
class CustomUserAdmin(SimpleHistoryAdmin, ModelAdmin, ImportExportModelAdmin):
    autocomplete_fields = [
        "city",
    ]
    model = CustomUser
    import_form_class = ImportForm
    export_form_class = ExportForm
    readonly_fields = ('updated_at', 'created_at')
    list_display = (
        'phone_number', 'telegram_id_field', 'first_name', 'last_name',
        'role_status', 'city'
    )
    list_filter = ('job_day', 'created_at', 'updated_at', 'role', 'department')
    list_filter_submit = True
    list_per_page = 25
    list_max_show_all = 1000

    @display(
        description=_("Role"),
        ordering="role",
        label={
            Role.EMPLOYEE: "success",  # green
            Role.MENTOR: "info",  # blue
            Role.MANAGER: "warning",  # orange

        },
    )
    def role_status(self, obj):
        return obj.role

    @display(
        description=_("telegram_id"),
        ordering="telegram_id_field",
        label={

            CustomUser.telegram_id: "info",  # blue

        },
    )
    def telegram_id_field(self, obj):
        return obj.telegram_id

    fieldsets = (
        (None, {'fields': ('phone_number', ('first_name', 'last_name'), 'telegram_id',)}),
        (_('Access rights and confirmation'), {'fields': ('role',)}),
        (_('Department'), {'fields': ('department', 'city')}),
        (_('Dates of creation, update and start of work'), {'fields': (('created_at', 'updated_at'), 'job_day')}),
    )

    search_fields = ('telegram_id', 'first_name', 'last_name', 'phone_number',)
    ordering = ('-created_at', '-updated_at')


@admin.register(City)
class CityAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ('name', 'slug', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at',)
    search_fields = ('name', 'slug')
    readonly_fields = ('slug', 'updated_at', 'created_at')
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_filter_submit = True
    list_per_page = 25
    list_max_show_all = 1000


@admin.register(ModerationForCity)
class ModerationForCityAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ('admin', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at',)
    search_fields = ('admin', 'city_name')
    readonly_fields = ('updated_at', 'created_at')
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_filter_submit = True
    list_per_page = 25
    list_max_show_all = 1000
