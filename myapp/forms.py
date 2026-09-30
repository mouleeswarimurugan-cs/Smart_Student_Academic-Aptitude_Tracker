from django import forms
from .models import Assignment


class AssignmentForm(forms.ModelForm):

    class Meta:

        model = Assignment

        fields = [
            'title',
            'subject',
            'description',
            'due_date',
            'priority',
            'status',
        ]

        widgets = {'due_date': forms.DateInput(attrs={'type': 'date'
                }),
        }