from django.db import models
from main.models import *
from django.utils.translation import gettext_lazy as _

class MentorshipAssignment(models.Model):
    employee = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='employee_assignments',
        limit_choices_to={'role': Role.EMPLOYEE},
        verbose_name=_("Employee")
    )
    mentor = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='mentor_assignments',
        limit_choices_to={'role__in': [Role.MENTOR, Role.MANAGER]},
        verbose_name=_("Mentor")
    )
    manager = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='manager_assignments',
        limit_choices_to={'role': Role.MANAGER},
        verbose_name=_("Manager")
    )
    assigned_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Assigned At"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    def __str__(self):
        return f"{self.employee.first_name} {self.employee.last_name} -> Mentor: {self.mentor.first_name if self.mentor else 'None'} -> Manager: {self.manager.first_name if self.manager else 'None'}"

    class Meta:
        verbose_name = _("Mentorship Assignment")
        verbose_name_plural = _("Mentorship Assignments")
        unique_together = ('employee', 'mentor', 'manager')
        ordering = ['-assigned_at']

    @staticmethod
    def get_assignments_by_city(city_id):
        """
        Метод для получения сотрудников, наставников и руководителей для указанного города.
        """
        employees = CustomUser.objects.filter(role=Role.EMPLOYEE, city_id=city_id)
        mentors = CustomUser.objects.filter(role=Role.MENTOR, city_id=city_id)
        managers = CustomUser.objects.filter(role=Role.MANAGER, city_id=city_id)

        return {
            "employees": employees,
            "mentors": mentors,
            "managers": managers
        }