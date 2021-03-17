from django import forms

from .models import CheckOut
from users.models import Group
from . import constants as cts


class RemarkForm(forms.Form):
    PAGE_CHOICES = (('1', '-1'), ('2', '-2'))
    page_number = forms.ChoiceField(label='Номер страницы',
                                    choices=PAGE_CHOICES)
    paragraph = forms.ChoiceField(label='Номер абзаца',
                                  choices=PAGE_CHOICES)

    err_1 = forms.BooleanField(label=cts.ERROR_1, required=False)
    err_2 = forms.BooleanField(label=cts.ERROR_2, required=False)
    err_3 = forms.BooleanField(label=cts.ERROR_3, required=False)
    err_4 = forms.BooleanField(label=cts.ERROR_4, required=False)
    err_5 = forms.BooleanField(label=cts.ERROR_5, required=False)
    err_6 = forms.BooleanField(label=cts.ERROR_6, required=False)
    err_7 = forms.BooleanField(label=cts.ERROR_7, required=False)
    err_8 = forms.BooleanField(label=cts.ERROR_8, required=False)
    err_9 = forms.BooleanField(label=cts.ERROR_9, required=False)
    err_10 = forms.BooleanField(label=cts.ERROR_10, required=False)
    err_11 = forms.BooleanField(label=cts.ERROR_11, required=False)


class CheckForm(forms.ModelForm):
    class Meta:
        model = CheckOut
        fields = ('docx_file', 'info')


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('title',)
