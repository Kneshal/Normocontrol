from django.contrib.auth import get_user_model
from django.test import TestCase

from verify.models import CheckOut, Remark
from verify.tests import constants as cts

User = get_user_model()


class PostsModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        user = User.objects.create(username=cts.USERNAME_1)
        '''
        user.profile.image = None
        cls.group = Group.objects.create(
            title=cts.LONG_TEXT,
            slug=cts.GROUP_1_SLUG,
            description=cts.GROUP_1_DESCRIPTION)
        cls.post = Post.objects.create(
            text=cts.LONG_TEXT,
            author=user,
            group=cls.group
        )
        cls.comment = Comment.objects.create(
            post=cls.post,
            author=user,
            text=cts.LONG_TEXT
        )
        '''

    def test_post_object_name_is_title_field(self):
        """__str__  post - это строчка с содержимым post.title."""
        pass
        #expected_object_name = PostsModelTest.post.text[
        #    :PostsModelTest.post.limit_str]
        #self.assertEquals(expected_object_name, str(PostsModelTest.post))
    '''
    def test_post_object_name_not_exceed(self):
        """Текст поста обрезается корректно."""
        expected_max_length = PostsModelTest.post.limit_str
        length_object_name = len(str(PostsModelTest.post))
        self.assertEquals(expected_max_length, length_object_name)

    def test_post_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        field_verboses = {
            'text': Post._meta.get_field('text').verbose_name,
            'pub_date': Post._meta.get_field('pub_date').verbose_name,
            'author': Post._meta.get_field('author').verbose_name,
            'group': Post._meta.get_field('group').verbose_name,
            'image': Post._meta.get_field('image').verbose_name
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    PostsModelTest.post._meta.get_field(value).verbose_name,
                    expected
                )

    def test_post_help_text(self):
        """help_text в полях совпадает с ожидаемым."""
        field_help_texts = {
            'text': Post._meta.get_field('text').help_text,
            'pub_date': Post._meta.get_field('pub_date').help_text,
            'author': Post._meta.get_field('author').help_text,
            'group': Post._meta.get_field('group').help_text,
            'image': Post._meta.get_field('image').help_text,
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    PostsModelTest.post._meta.get_field(value).help_text,
                    expected
                )
    '''