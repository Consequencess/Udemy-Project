from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory

from applications.accounts.serializers import ForgotPasswordSerializer, ForgotPasswordConfirmSerializer
from applications.accounts.views import ActivationAPIView, TeacherActivationAPIView

User = get_user_model()


class StudentRegisterAPIViewTestCase(APITestCase):
    def setUp(self):
        self.valid_payload = {
            'email': 'test@example.com',
            'password': 'secret1234',
            'first_name': 'Test',
            'last_name': 'User'
        }

    def test_student_registration(self):
        response = self.client.post(reverse('student_register'), data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'test@example.com')


class TeacherRegisterAPIViewTestCase(APITestCase):
    def setUp(self):
        self.valid_payload = {
            'email': 'test2@example.com',
            'password': 'secret1234',
            'first_name': 'test',
            'last_name': 'user',
            'experience': 'online',
            'audience': 'not at the moment',
        }

    def test_teacher_registration(self):
        response = self.client.post(reverse('teacher_register'), data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'test2@example.com')


class ActivationAPIViewTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(
            email='test@example.com',
            activation_code='abc123'
        )

    def test_get_success(self):
        request = self.factory.get('/activate/abc123')
        view = ActivationAPIView.as_view()
        response = view(request, activation_code='abc123')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'msg': 'Successfully activated.'})

        # Check if the user is activated
        updated_user = User.objects.get(email='test@example.com')
        self.assertTrue(updated_user.is_active)
        self.assertFalse(updated_user.is_mentor)
        self.assertEqual(updated_user.activation_code, '')

    def test_get_wrong_code(self):
        request = self.factory.get('/activate/wrong_code')
        view = ActivationAPIView.as_view()
        response = view(request, activation_code='wrong_code')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'msg': 'Wrong email.'})


class TeacherActivationAPIViewTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(
            email='test@example.com',
            activation_code='abc123'
        )

    def test_get_success(self):
        request = self.factory.get('/activate/teacher/abc123')
        view = TeacherActivationAPIView.as_view()
        response = view(request, activation_code='abc123')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'msg': 'Successfully activated.'})

        # Check if the user is activated as a mentor
        updated_user = User.objects.get(email='test@example.com')
        self.assertTrue(updated_user.is_active)
        self.assertTrue(updated_user.is_mentor)
        self.assertEqual(updated_user.activation_code, '')

    def test_get_wrong_code(self):
        request = self.factory.get('/activate/teacher/wrong_code')
        view = TeacherActivationAPIView.as_view()
        response = view(request, activation_code='wrong_code')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'msg': 'Wrong email.'})


class StudentActivationAPIViewTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(
            email='test2@example.com',
            activation_code='abc123'
        )

    def test_get_success(self):
        request = self.factory.get('/activate/student/abc123')
        view = TeacherActivationAPIView.as_view()
        response = view(request, activation_code='abc123')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'msg': 'Successfully activated.'})

        updated_user = User.objects.get(email='test2@example.com')
        self.assertTrue(updated_user.is_active)
        # self.assertTrue(updated_user.is_mentor)
        self.assertEqual(updated_user.activation_code, '')

    def test_get_wrong_code(self):
        request = self.factory.get('/activate/student/wrong_code')
        view = TeacherActivationAPIView.as_view()
        response = view(request, activation_code='wrong_code')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'msg': 'Wrong email.'})


class ForgotPasswordSerializerTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            password='testpassword',
            email='test@example.com'
        )

    def test_valid_email(self):
        data = {'email': 'test@example.com'}
        serializer = ForgotPasswordSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_email(self):
        data = {'email': 'invalid@example.com'}
        serializer = ForgotPasswordSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors,
            {'email': ['Такого пользователя не существует.']}
        )


class ForgotPasswordConfirmSerializerTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            password='testpassword',
            email='test@example.com'
        )

    def test_valid_email(self):
        data = {
            'email': 'test@example.com',
            'password': 'newpassword',
            'password_confirm': 'newpassword'
        }
        serializer = ForgotPasswordConfirmSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_email(self):
        data = {
            'email': 'invalid@example.com',
            'password': 'newpassword',
            'password_confirm': 'newpassword'
        }
        serializer = ForgotPasswordConfirmSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors,
            {'email': ['Такого пользователя не существует.']}
        )

    def test_password_mismatch(self):
        data = {
            'email': 'test@example.com',
            'password': 'newpassword',
            'password_confirm': 'mismatch'
        }
        serializer = ForgotPasswordConfirmSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors,
            {'non_field_errors': ['Пароли не совпадают.']}
        )





