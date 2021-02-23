from django.db import models
from django.contrib.auth import get_user_model
from pytils.translit import slugify

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
    slug = models.SlugField(
        verbose_name='Slug-метка',
        help_text='Укажите адрес для текущей проверки',
        unique=True,
        null=True
    )

    class Meta:
        ordering = ['-check_date']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'check-%Y%m%d%H%M-{self.student.username}')
        super().save(*args, **kwargs)


class Remark(models.Model):
    text = models.TextField(
        verbose_name='Текст замечания',
        help_text='Введите текст замечания',
        max_length=1000
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
