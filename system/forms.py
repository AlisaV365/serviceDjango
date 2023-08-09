from django import forms

from system.models import Mailing


class MailingForm(forms.ModelForm):
    """Форма для создания рассылки"""

    class Meta:
        model = Mailing

        fields = ('date_time', 'periodicity', 'client', 'message')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
