from django import forms
from django.core import validators


class CharField(forms.CharField):

    def to_python(self, value):
        if value is None:
            return None
        return super().to_python(value)


class EmailField(CharField):
    widget = forms.widgets.EmailInput
    default_validators = [validators.validate_email]

    def clean(self, value):
        if isinstance(value, str):
            value = self.to_python(value).strip()
        else:
            value = self.to_python(value)
        return super(EmailField, self).clean(value)


class BooleanField(forms.Field):

    empty_values = {None}

    def to_python(self, value):
        if value in (True, False):
            return value
        return None


class MultiValueField(forms.TypedMultipleChoiceField):

    def valid_value(self, value):
        return True


class OffsetLimit(forms.Form):

    offset = forms.IntegerField(required=False, min_value=0)
    limit = forms.IntegerField(required=False)

    @classmethod
    def with_limit_required(cls, *, limit_max_value):
        limit = forms.IntegerField(
            required=True,
            max_value=limit_max_value,
        )
        return type('OffsetLimitRequired', (cls, ), dict(limit=limit))
