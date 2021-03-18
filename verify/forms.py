from django import forms

from .models import CheckOut
from users.models import Group
from . import constants as cts


class RemarkNavForm(forms.Form):
    """Форма для указания страницы и абзаца замечания."""
    SECTION_CHOICES = (
        ('title', 'Титульный лист'),
        ('task', 'Индивидуальное задание на ВКР'),
        ('abstract', 'Реферат'),
        ('contents', 'Оглавление'),
        ('introduction', 'Введение'),
        ('body', 'Основная часть'),
        ('conclusion', 'Заключение'),
        ('source', 'Список использованных источников'),
        ('attachment', 'Приложение'),
    )
    section = forms.ChoiceField(label='Раздел ПЗ',
                                choices=SECTION_CHOICES)
    page_number = forms.IntegerField(label='Номер страницы', required=False)
    paragraph = forms.IntegerField(label='Номер абзаца', required=False)
    custom_error = forms.CharField(
        label='Примечание:',
        widget=forms.Textarea(),
        required=False
    )


class RemarkStandartErrorForm(forms.Form):
    """Форма выбора замечания."""
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
    err_12 = forms.BooleanField(label=cts.ERROR_12, required=False)
    err_13 = forms.BooleanField(label=cts.ERROR_13, required=False)
    err_14 = forms.BooleanField(label=cts.ERROR_14, required=False)
    err_15 = forms.BooleanField(label=cts.ERROR_15, required=False)
    err_16 = forms.BooleanField(label=cts.ERROR_16, required=False)
    err_17 = forms.BooleanField(label=cts.ERROR_17, required=False)
    err_18 = forms.BooleanField(label=cts.ERROR_18, required=False)
    err_19 = forms.BooleanField(label=cts.ERROR_19, required=False)
    err_20 = forms.BooleanField(label=cts.ERROR_20, required=False)
    err_21 = forms.BooleanField(label=cts.ERROR_21, required=False)
    err_22 = forms.BooleanField(label=cts.ERROR_22, required=False)
    err_23 = forms.BooleanField(label=cts.ERROR_23, required=False)
    err_24 = forms.BooleanField(label=cts.ERROR_24, required=False)
    err_25 = forms.BooleanField(label=cts.ERROR_25, required=False)
    err_26 = forms.BooleanField(label=cts.ERROR_26, required=False)
    err_27 = forms.BooleanField(label=cts.ERROR_27, required=False)
    err_28 = forms.BooleanField(label=cts.ERROR_28, required=False)


class CheckForm(forms.ModelForm):
    class Meta:
        model = CheckOut
        fields = ('docx_file', 'info')


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('title',)
