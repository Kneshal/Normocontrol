from django import forms

from .models import CheckOut
from users.models import Group


class CheckForm(forms.ModelForm):
    class Meta:
        model = CheckOut
        fields = ('docx_file', 'info')


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('title',)
