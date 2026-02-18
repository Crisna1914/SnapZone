from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from userauth import views


urlpatterns = [
    path('', views.landing, name='landing'),
    path('home/', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('upload/', views.upload, name='upload'),
    path('like-post/<str:id>', views.likes, name='like-post'),
    path('explore/',views.explore, name='explore'),  
    path('profile/<str:id_user>', views.profile, name='profile'),
    path('follow',views.follow,name='follow'),
    path('delete/<str:id>/', views.delete, name="delete"),
    path('search/', views.search_results, name='search_results'),
    path('logout/', views.logout_view, name='logout'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
