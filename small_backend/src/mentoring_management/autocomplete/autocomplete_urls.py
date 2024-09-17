from django.urls import path
from . import autocomplete

urlpatterns = [
    path('employee-autocomplete/', autocomplete.EmployeeAutocomplete.as_view(), name='employee-autocomplete'),
    path('mentor-autocomplete/', autocomplete.MentorAutocomplete.as_view(), name='mentor-autocomplete'),
    path('manager-autocomplete/', autocomplete.ManagerAutocomplete.as_view(), name='manager-autocomplete'),
]
