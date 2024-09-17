from django import forms
from dal import autocomplete
from mentoring_management.models import MentorshipAssignment
from main.models import CustomUser
from unfold.widgets import UnfoldForeignKeyRawIdWidget
from django.utils.translation import gettext_lazy as _


class MentorshipAssignmentForm(forms.ModelForm):
    class Meta:
        model = MentorshipAssignment
        fields = ['employee', 'mentor', 'manager']
        widgets = {
            'employee': autocomplete.ModelSelect2(
                url='employee-autocomplete',
                attrs={

                    'data-placeholder': _('Select employee'),
                    'aria-hidden': 'true'
                }
            ),
            'mentor': autocomplete.ModelSelect2(
                url='mentor-autocomplete',
                attrs={

                    'data-placeholder': _('Select mentor'),
                    'aria-hidden': 'true'
                }
            ),
            'manager': autocomplete.ModelSelect2(
                url='manager-autocomplete',
                attrs={

                    'data-placeholder': _('Select manager'),
                    'aria-hidden': 'true'
                }
            ),
        }
