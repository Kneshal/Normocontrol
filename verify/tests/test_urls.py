from django.core.cache import cache
from django.test import Client, TestCase
from django.contrib.auth import get_user_model

from verify.models import CheckOut, Remark
from verify.tests import constants as cts
from users.models import Group, CustomUser

User = get_user_model()


class VerifyURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title=cts.GROUP_1_TITLE,
            slug=cts.GROUP_1_SLUG,
        )
        cls.student_1 = CustomUser.objects.create(
            username=cts.USERNAME_1,
            group=cls.group,
            allow_manage=False,
        )
        cls.student_2 = CustomUser.objects.create(
            username=cts.USERNAME_2,
            group=cls.group,
            allow_manage=False,
        )
        cls.controller = CustomUser.objects.create(
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
        cls.urls = {
            'index': '/',
            'student_list': '/students/',
            'student_active_check': f'students/{cls.student_1}/',
            'group_list': '/group/',
            'new_group': '/group/new_group/',
            'group_students': f'/group/{cls.group.slug}/',
            'check_list': f'/user/{cls.student_1}/check_list/',
            'archive': f'/user/{cls.student_1}/archive/',
            'new_check': f'/user/{cls.student_1}/new_check/',
            'add_remark': (f'/user/{cls.student_1}/{cls.checkout.id}/'
                           'add_remark/'),
            'delete_remark': (f'/user/{cls.student_1}/{cls.checkout.id}/'
                              f'{cls.remark.id}/delete_remark/'),
            'check_view': (f'/user/{cls.student_1}/{cls.checkout.id}/'
                           'check_view/'),
            'check_delete': (f'/user/{cls.student_1}/{cls.checkout.id}/'
                             'check_delete/'),
            'check_archive': (f'/user/{cls.student_1}/{cls.checkout.id}/'
                              'check_archive/'),
            'check_active': (f'/user/{cls.student_1}/{cls.checkout.id}/'
                             'check_active/'),
            'unknown_page': '/unknown_page/',
        }

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client_1 = Client()
        self.authorized_client_1.force_login(VerifyURLTests.student_1)
        self.authorized_client_2 = Client()
        self.authorized_client_2.force_login(VerifyURLTests.student_2)
        self.authorized_client_3 = Client()
        self.authorized_client_3.force_login(VerifyURLTests.controller)
        cache.clear()

    def test_unknown_url(self):
        """Проверяем доступность неизвестного url."""
        response = self.authorized_client_1.get(
            VerifyURLTests.urls['unknown_page']
        )
        self.assertEqual(response.status_code, 404)

    def test_url_available_to_guest_user(self):
        """Страницы доступны любому пользователю."""
        url_for_guest_user = [
            VerifyURLTests.urls['index'],
        ]
        for url in url_for_guest_user:
            with self.subTest():
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_url_not_available_to_guest_user(self):
        """Страницы не доступны гостевому пользователю."""
        url_for_guest_user = [
            VerifyURLTests.urls['student_list'],
            VerifyURLTests.urls['student_active_check'],
            VerifyURLTests.urls['group_list'],
            VerifyURLTests.urls['new_group'],
            VerifyURLTests.urls['group_students'],
            VerifyURLTests.urls['check_list'],
            VerifyURLTests.urls['archive'],
            VerifyURLTests.urls['new_check'],
            VerifyURLTests.urls['add_remark'],
            VerifyURLTests.urls['delete_remark'],
            VerifyURLTests.urls['check_view'],
            VerifyURLTests.urls['check_archive'],
            VerifyURLTests.urls['check_active'],
        ]
        for url in url_for_guest_user:
            with self.subTest():
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, 302, f'URL {url} работает некорректно')
    '''

    def test_url_redirect_guest_user_to_login(self):
        """Гостя редиректит с недоступных страниц на страницу авторизации."""
        url_for_guest_user = [
            PostsURLTests.urls['new_post'],
            PostsURLTests.urls['post_edit'],
            PostsURLTests.urls['add_comment'],
            PostsURLTests.urls['follow_index'],
            PostsURLTests.urls['profile_follow'],
            PostsURLTests.urls['profile_unfollow']
        ]
        for url in url_for_guest_user:
            with self.subTest():
                response = self.guest_client.get(url, follow=True)
                expected = f"/auth/login/?next={url}"
                self.assertRedirects(response, expected)

    def test_url_available_to_authorized_user(self):
        """Страницы доступны авторизованному пользователю."""
        url_for_auth_user = [
            PostsURLTests.urls['new_post'],
            PostsURLTests.urls['follow_index'],
        ]
        for url in url_for_auth_user:
            with self.subTest():
                response = self.authorized_client_1.get(url)
                self.assertEqual(response.status_code, 200)

    def test_add_comment_redirect(self):
        """Проверка редиректа после создания коммента."""
        response = self.guest_client.get(
            PostsURLTests.urls['add_comment'],
            follow=True
        )
        expected = f"/auth/login/?next={PostsURLTests.urls['add_comment']}"
        self.assertRedirects(response, expected)

    def test_url_profile_follow_redirect(self):
        """Проверка редиректа после подписки на пользователя."""
        response = self.authorized_client_2.get(
            PostsURLTests.urls['profile_follow'],
            follow=True
        )
        expected = PostsURLTests.urls['profile']
        self.assertRedirects(response, expected)

    def test_url_profile_unfollow_redirect(self):
        """Проверка редиректа после отписки от пользователя."""
        self.authorized_client_2.get(PostsURLTests.urls['profile_follow'])
        response = self.authorized_client_2.get(
            PostsURLTests.urls['profile_unfollow'],
            follow=True
        )
        expected = PostsURLTests.urls['profile']
        self.assertRedirects(response, expected)

    def test_url_new_post_redirect(self):
        """Проверка редиректа со страницы создания записи."""
        response = self.guest_client.get(
            PostsURLTests.urls['new_post'],
            follow=True
        )
        expected = f"/auth/login/?next={PostsURLTests.urls['new_post']}"
        self.assertRedirects(response, expected)

    def test_url_edit_post_access(self):
        """Проверка доступа к странице редактирования записи."""
        response = self.guest_client.get(PostsURLTests.urls['post_edit'])
        self.assertEqual(response.status_code, 302)
        response = self.authorized_client_1.get(
            PostsURLTests.urls['post_edit']
        )
        self.assertEqual(response.status_code, 200)
        response = self.authorized_client_2.get(
            PostsURLTests.urls['post_edit']
        )
        self.assertEqual(response.status_code, 302)

    def test_url_edit_post_redirect(self):
        """Проверка редиректа со страницы редактирования записи."""
        response = self.guest_client.get(PostsURLTests.urls['post_edit'],
                                         follow=True)
        expected = f"/auth/login/?next={PostsURLTests.urls['post_edit']}"
        self.assertRedirects(response, expected)
        response = self.authorized_client_2.get(
            PostsURLTests.urls['post_edit'],
            follow=True
        )
        self.assertRedirects(response, PostsURLTests.urls['post_view'])

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            PostsURLTests.urls['index']: 'posts/index.html',
            PostsURLTests.urls['group_posts']: 'posts/group.html',
            PostsURLTests.urls['new_post']: 'posts/new.html',
            PostsURLTests.urls['post_edit']: 'posts/new.html',
            PostsURLTests.urls['post_view']: 'posts/post.html',
            PostsURLTests.urls['profile']: 'profile.html',
            PostsURLTests.urls['follow_index']: 'follow.html',
        }
        for reverse_name, template in templates_url_names.items():
            with self.subTest():
                response = self.authorized_client_1.get(reverse_name)
                self.assertTemplateUsed(response, template)
    '''
