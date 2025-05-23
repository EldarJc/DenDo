from django.urls import path
# from django.urls.utils import vie
from .views import  *

app_name = 'dendo_users'

urlpatterns = [
    path('test-page/', test_view, name='test_page'),
    path('login/', LoginView.as_view(), name='login_page'),
    path('signup/', SignupView.as_view(), name='signup_page'),
    path('logout/', logout_view, name='logout_page'),
    path('profile/<str:username>/', UserProfileView.as_view(), name='user_page'),
    path('profile/<str:username>/update-password/', UpdatePasswordView.as_view(), name='password_reset_page'),
    path('profile/<str:username>/edit-profile/', EditProfileView.as_view(), name='user_edit_page'),
]