"""
.. module:: advocate_uploader.core.fields
   :synopsis: Advocate Uploader Core Model Fields.

.. moduleauthor:: Alex Kavanaugh <kavanaugh.development@outlook.com>

"""

from django.core.exceptions import ValidationError
from django.db.models import BooleanField


class YNBooleanField(BooleanField):

    description = "Stores a Y/N boolean value"

    def from_db_value(self, value, expression, connection, context):
        return self.to_python(value)

    def to_python(self, value):
        if value in (True, False):
            # if value is 1 or 0 than it's equal to True or False, but we want
            # to return a true bool for semantic reasons.
            return bool(value)
        if value == 'Y':
            return True
        if value == 'N':
            return False
        if value == '-':
            return None
        msg = self.error_messages['invalid'] % {'value': value}
        raise ValidationError(msg)

    def get_prep_value(self, value):
        if value is None:
            return None
        if value:
            return 'Y'
        else:
            return 'N'

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)
