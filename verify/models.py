from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class CheckOut(models.Model):
    student = models.ForeignKey(
        User,
        verbose_name='Студент',
        help_text='Выберите студента из списка',
        on_delete=models.CASCADE,
        related_name='checkout_student',
    )
    check_date = models.DateTimeField(
        verbose_name='Дата проверки',
        auto_now_add=True,
        db_index=True,
    )
    info = models.TextField(
        verbose_name='Сопровотельная информация',
        help_text='При необходимости укажите дополнительные сведения',
        max_length=1000,
        null=True,
        blank=True,
    )
    status = models.BooleanField(
        default=False,
        verbose_name='Текущий статус проверки работы',
        help_text='Укажите текущий статус проверки',
        null=True,
    )
    docx_file = models.FileField(
        verbose_name='Файл с дипломной работой',
        help_text='Укажите файл с дипломной работой',
        upload_to='diplomas/%Y/%m/%d/',
    )

    class Meta:
        ordering = ['check_date']


class Remark(models.Model):
    page_number = models.PositiveSmallIntegerField(
        verbose_name='Номер страницы',
        help_text='Укажите номер страницы',
    )
    paragraph = models.PositiveSmallIntegerField(
        verbose_name='Номер абзаца',
        help_text='Укажите номер абзаца',
        null=True,
        blank=True,
    )
    text = models.TextField(
        verbose_name='Текст замечания',
        help_text='Введите текст замечания',
        max_length=1000,
    )
    note = models.TextField(
        verbose_name='Текст примечания',
        help_text='Введите текст примечания',
        max_length=2000,
        null=True,
        blank=True,
    )
    author = models.ForeignKey(User,
                               verbose_name='Автор замечания',
                               help_text='Укажите автора замечания',
                               on_delete=models.CASCADE,
                               related_name='remark')
    check_out = models.ForeignKey(
        CheckOut,
        on_delete=models.CASCADE,
        related_name='remark',
    )
    check_date = models.DateTimeField(
        verbose_name='Дата публикации замечания',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ['check_date']
