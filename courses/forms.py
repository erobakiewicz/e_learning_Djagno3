from django.forms import inlineformset_factory

from courses.models import Course, Module

"""
Formset to validate all forms
fields: fields included in all forms
extra: number of extra empty forms to display
can_delete: if True Django will display checkbox input to mark objects to delete
"""
ModuleFormSet = inlineformset_factory(Course,
                                      Module,
                                      fields=['title', 'description'],
                                      extra=2,
                                      can_delete=True)
