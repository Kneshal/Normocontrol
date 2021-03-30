import shutil
import tempfile

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from users.models import Group
from verify.models import CheckOut, Remark
from verify.tests import constants as cts
from normocontrol.settings import MEDIA_ROOT

User = get_user_model()


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class VerifyViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        settings.MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)
        cls.group = Group.objects.create(
            title=cts.GROUP_1_TITLE,
            slug=cts.GROUP_1_SLUG,
        )
        cls.student_1 = User.objects.create(
            #email=
            username=cts.USERNAME_1,
            group=cls.group,
            allow_manage=False,
        )
        cls.student_2 = User.objects.create(
            username=cts.USERNAME_2,
            group=cls.group,
            allow_manage=False,
        )
        cls.controller = User.objects.create(
            username=cts.USERNAME_3,
            allow_manage=True,
        )
        cls.checkout = CheckOut.objects.create(
            student=cls.student_1,
            info=cts.INFO,
            status=False,
            docx_file=None,
            pdf_file=None,
        )
        cls.remark = Remark.objects.create(
            section=cts.REMARK_SECTION,
            page_number=cts.REMARK_PAGE_NUMBER,
            paragraph=cts.REMARK_PARAGRAPH,
            text=cts.REMARK_TEXT,
            author=cls.controller,
            check_out=cls.checkout
        )
        cls.static_url = {
            'index': reverse('verify:index'),
        }
        cls.urls_need_access = {
            'student_list': reverse(
                'verify:student_list'
            ),
            'group_list': reverse(
                'verify:group_list'
            ),
            'new_group': reverse(
                'verify:new_group'
            ),
            'student_active_check': reverse(
                'verify:student_active_check',
                kwargs={
                    'username': cls.controller
                }
            ),
            'group_students': reverse(
                'verify:group_students',
                kwargs={
                    'slug': cls.group.slug
                }
            ),
            'add_remark': reverse(
                'verify:add_remark',
                kwargs={
                    'username': cls.controller,
                    'check_id': cls.checkout.id
                }
            ),
            'delete_remark': reverse(
                'verify:delete_remark',
                kwargs={
                    'username': cls.controller,
                    'check_id': cls.checkout.id,
                    'remark_id': cls.remark.id
                }
            ),
            'check_archive': reverse(
                'verify:check_archive',
                kwargs={
                    'username': cls.controller,
                    'check_id': cls.checkout.id
                }
            ),
            'check_active': reverse(
                'verify:check_active',
                kwargs={
                    'username': cls.controller,
                    'check_id': cls.checkout.id
                }
            ),
        }
        cls.urls_user_check = {
            'new_check': reverse(
                'verify:new_check',
                kwargs={
                    'username': cls.student_1
                }
            ),
            'check_delete': reverse(
                'verify:check_delete',
                kwargs={
                    'username': cls.student_1,
                    'check_id': cls.checkout.id
                }
            ),
            'check_view': reverse(
                'verify:check_view',
                kwargs={
                    'username': cls.student_1,
                    'check_id': cls.checkout.id
                }
            ),
            'archive': reverse(
                'verify:archive',
                kwargs={
                    'username': cls.student_1
                }
            ),
            'check_list': reverse(
                'verify:check_list',
                kwargs={
                    'username': cls.student_1
                }
            ),
        }

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.guest_client = Client()
        self.student_client_1 = Client()
        self.student_client_1.force_login(VerifyViewsTests.student_1)
        self.student_client_2 = Client()
        self.student_client_2.force_login(VerifyViewsTests.student_2)
        self.controller_client = Client()
        self.controller_client.force_login(VerifyViewsTests.controller)
        cache.clear()

    def test_new_check_valid_form(self):
        """Валидная форма создает заявку и производит редирект."""
        CheckOut.objects.all().delete()
        checks_count = CheckOut.objects.count()
        pdf_uploaded = SimpleUploadedFile(
            name=cts.PDF_FILE_NAME,
            content=cts.PDF_FILE_CONTENT,
            content_type=cts.PDF_FILE_TYPE
        )
        docx_uploaded = SimpleUploadedFile(
            name=cts.DOCX_FILE_NAME,
            content=cts.DOCX_FILE_CONTENT,
            content_type=cts.DOCX_FILE_TYPE
        )
        form_data = {
            'docx_file': docx_uploaded,
            'pdf_file': pdf_uploaded,
            'info': cts.INFO,
        }
        response = self.student_client_1.post(
            VerifyViewsTests.urls_user_check['new_check'],
            data=form_data,
            follow=True
        )
        self.assertEqual(checks_count + 1, CheckOut.objects.count())
        self.assertRedirects(
            response,
            reverse(
                'verify:check_list',
                kwargs={
                    'username': VerifyViewsTests.student_1
                }
            ),
        )

    def test_new_check_not_valid_form(self):
        """Форма создания заявки не прошла валидацию."""
        CheckOut.objects.all().delete()
        checks_count = CheckOut.objects.count()
        pdf_uploaded = SimpleUploadedFile(
            name=cts.PDF_FILE_NAME,
            content=cts.PDF_FILE_CONTENT,
            content_type=cts.PDF_FILE_TYPE
        )
        docx_uploaded = SimpleUploadedFile(
            name=cts.DOCX_FILE_NAME,
            content=cts.DOCX_FILE_CONTENT,
            content_type=cts.DOCX_FILE_TYPE
        )
        form_data = {
            'docx_file': pdf_uploaded,
            'pdf_file': docx_uploaded,
            'info': '',
        }
        response = self.student_client_1.post(
            VerifyViewsTests.urls_user_check['new_check'],
            data=form_data,
            follow=True
        )
        self.assertEqual(checks_count, CheckOut.objects.count())
        self.assertIsNotNone(response.context.get('form'))

    def test_new_group_valid_form(self):
        """Валидная форма создает группу и производит редирект."""
        group_count = Group.objects.count()
        form_data = {
            'title': cts.GROUP_1_TITLE,
        }
        response = self.controller_client.post(
            VerifyViewsTests.urls_need_access['new_group'],
            data=form_data,
            follow=True
        )
        self.assertEqual(group_count + 1, Group.objects.count())
        self.assertRedirects(
            response,
            reverse(
                'verify:check_list',
                kwargs={
                    'username': VerifyViewsTests.controller
                }
            ),
        )

    def test_new_group_not_valid_form(self):
        """Форма создания группы не прошла валидацию."""
        group_count = Group.objects.count()
        form_data = {
            'title': '',
        }
        response = self.controller_client.post(
            VerifyViewsTests.urls_need_access['new_group'],
            data=form_data,
            follow=True
        )
        self.assertEqual(group_count, Group.objects.count())
        self.assertIsNotNone(response.context.get('form'))

    def test_new_remark_valid_form(self):
        """Валидная форма создает замечания и производит редирект."""
        remark_count = Remark.objects.count()
        form_data = {
            'section': cts.REMARK_SECTION,
            'page_number': cts.REMARK_PAGE_NUMBER,
            'paragraph': cts.REMARK_PARAGRAPH,
            'custom_error': cts.REMARK_TEXT,
            'err_1': True,
        }
        response = self.controller_client.post(
            VerifyViewsTests.urls_need_access['add_remark'],
            data=form_data,
            follow=True
        )
        self.assertEqual(remark_count + 2, Remark.objects.count())
        self.assertRedirects(
            response,
            reverse(
                'verify:check_view',
                kwargs={
                    'username': VerifyViewsTests.controller,
                    'check_id': VerifyViewsTests.checkout.id
                }
            )
        )

    def test_new_remark_not_valid_form(self):
        """Валидная форма создает замечания и производит редирект."""
        remark_count = Remark.objects.count()
        form_data = {
            'section': '',
            'page_number': '',
            'paragraph': '',
            'custom_error': '',
            'err_1': '',
        }
        response = self.controller_client.post(
            VerifyViewsTests.urls_need_access['add_remark'],
            data=form_data,
            follow=True
        )
        self.assertEqual(remark_count, Remark.objects.count())
        self.assertRedirects(
            response,
            reverse(
                'verify:check_view',
                kwargs={
                    'username': VerifyViewsTests.controller,
                    'check_id': VerifyViewsTests.checkout.id
                }
            )
        )
