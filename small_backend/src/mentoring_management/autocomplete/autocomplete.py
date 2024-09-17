from dal import autocomplete
from main.models import CustomUser, ModerationForCity, Role
from mentoring_management.models import MentorshipAssignment


class EmployeeAutocomplete(autocomplete.Select2QuerySetView):
    paginate_by = 10
    def get_queryset(self):
        # Убедитесь, что пользователь аутентифицирован
        if not self.request.user.is_authenticated:
            return CustomUser.objects.none()

        # Получаем города, которыми управляет текущий администратор
        moderation_for_city = ModerationForCity.objects.filter(admin=self.request.user).values_list('city', flat=True)

        # Получаем сотрудников, которые уже выбраны в других записях MentorshipAssignment
        used_employees = MentorshipAssignment.objects.values_list('employee', flat=True)

        # Фильтруем сотрудников по роли, городам и исключаем уже выбранных сотрудников
        qs = CustomUser.objects.filter(role=Role.EMPLOYEE, city__in=moderation_for_city).exclude(id__in=used_employees)

        if self.q:
            qs = qs.filter(first_name__icontains=self.q)

        return qs


class MentorAutocomplete(autocomplete.Select2QuerySetView):
    paginate_by = 10

    def get_queryset(self):
        # Убедитесь, что пользователь аутентифицирован
        if not self.request.user.is_authenticated:
            return CustomUser.objects.none()

        # Получаем города, которыми управляет текущий администратор
        moderation_for_city = ModerationForCity.objects.filter(admin=self.request.user).values_list('city', flat=True)

        # Фильтруем менторов по роли и городам
        qs = CustomUser.objects.filter(role__in=[Role.MENTOR, Role.MANAGER], city__in=moderation_for_city)

        if self.q:
            qs = qs.filter(first_name__icontains=self.q)

        return qs


class ManagerAutocomplete(autocomplete.Select2QuerySetView):
    paginate_by = 10
    def get_queryset(self):
        # Убедитесь, что пользователь аутентифицирован
        if not self.request.user.is_authenticated:
            return CustomUser.objects.none()

        # Получаем города, которыми управляет текущий администратор
        moderation_for_city = ModerationForCity.objects.filter(admin=self.request.user).values_list('city', flat=True)

        # Фильтруем менеджеров по роли и городам
        qs = CustomUser.objects.filter(role=Role.MANAGER, city__in=moderation_for_city)

        if self.q:
            qs = qs.filter(first_name__icontains=self.q)

        return qs
