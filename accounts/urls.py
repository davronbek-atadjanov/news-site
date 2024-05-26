from django.urls import path
from .views import user_login, dashboard_view, user_register, SignUpView, edit_user, EditUserView, admin_page_view, SearchResultsList
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
urlpatterns = [
    # path('login/', user_login,name='login'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', dashboard_view, name='user_profile'),
    path('password-change/', PasswordChangeView.as_view(), name='password_change'),
    path('passoword-change-done/',PasswordChangeDoneView.as_view(), name='password_change-done'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('signup/', user_register, name='user_register'),
    # path('signup/',SignUpView.as_view(),name='user_register'),
    path('profile/edit/', edit_user, name='edit_user_information'),
    path('adminpage/', admin_page_view, name='admin_page'),
    path('searchresult/', SearchResultsList.as_view(), name='search_results'),
]
