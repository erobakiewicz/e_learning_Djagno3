from django import forms

from courses.models import Course

"""
This form is not to be displayed, it's function for "enroll" button in 
course detail view.
"""


class CourseEnrollForm(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(),
                                    widget=forms.HiddenInput)
