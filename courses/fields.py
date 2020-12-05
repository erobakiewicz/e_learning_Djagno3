from django.core.exceptions import ObjectDoesNotExist
from django.db import models

"""
custom django model field OrederField. it has optional for_fields param which is ordering
by overriding pre_save method:
1. checking if value already exist
2. Build queryset to retrive all obj of model 
3. if there are any names in for_fields attr and filter the queryset by the current value of
model fields in for_fields
4. retrive obj with the highest (latest) order, if there is none order att is set to 0
5. else if there is an obj +1 is added to order attr
6. in setattr() order is calculated and set
"""


class OrderField(models.PositiveIntegerField):
    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if getattr(model_instance, self.attname) is None:
            # no current value
            try:
                qs = self.model.objects.all()
                if self.for_fields:
                    # filter by objects with the same field values
                    # for the fields in "for_fields"
                    query = {field: getattr(model_instance, field) for field in self.for_fields}
                    qs = qs.filter(**query)
                # get the order of the last item
                last_item = qs.latest(self.attname)
                value = last_item.order + 1
            except ObjectDoesNotExist:
                value = 0
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super().pre_save(model_instance, add)
