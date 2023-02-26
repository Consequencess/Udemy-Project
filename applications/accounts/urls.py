from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from applications.accounts import views


urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("refresh/", TokenRefreshView.as_view(), name='token_refresh'),
    path("student_register/", views.StudentRegisterAPIView.as_view(), name='student_register'),
    path("teacher_register/", views.TeacherRegisterAPIView.as_view(), name='teacher_register'),
    path("confirm-mentor/<uuid:activation_code>/", views.TeacherActivationAPIView.as_view()),
    path("confirm/<uuid:activation_code>/", views.StudentActivationAPIView.as_view()),
    path("forgot_password/", views.ForgotPasswordAPIView.as_view()),
    path("recovery/<uuid:activation_code>/", views.NewPasswordAPIView.as_view()),
]

