from django.urls import path
from . import views
from django.contrib import admin

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('blog/', views.blog, name='blog'),
    path('contact/', views.contact, name='contact'),
    path('recommendations/', views.get_recommendations, name='recommendations'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name='logout'),
    path('my-account/', views.my_account, name='my_account'),
    path('user_popup/', views.user_popup, name='user_popup'),
    path('user_page/', views.user_page, name='user_page'), 
    path('update_profile_picture/', views.update_profile_picture, name='update_profile_picture'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('edit-user-details/', views.edit_user_details, name='edit_user_details'),
    path('submit-measurements/', views.submit_measurements, name='submit_measurements'),
    path('edit-measurements/', views.edit_measurements, name='edit_measurements'),
    path('admin/', admin.site.urls),
    path('admin-user/', views.admin_user_view, name='admin_user'),
    path('api/user/<int:user_id>/', views.user_api, name='user_api'),
]