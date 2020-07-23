from django.urls import path
from .views import Base, Homepage, Register,Login, Activate, Profile, Profileupdate, Createblog, BlogEdit, Blogdetail,\
    BlogDelete, Profile

urlpatterns = [
    path('', Base.as_view(), name='base'),
    path('home/', Homepage.as_view(), name='home'),
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('activate/<uid>/', Activate.as_view(), name='activate'),
    path('profile/', Profile.as_view(), name='profile'),
    path('profile-update/<int:pk>/', Profileupdate.as_view(), name='profile-update'),
    path('blog-create', Createblog.as_view(), name='blog-create'),
    path('blog-update/<int:pk>/', BlogEdit.as_view(), name='blog-update'),
    path('blog-detail/<int:pk>/', Blogdetail.as_view(), name='blog-detail'),
    path('blog-delete/<int:pk>/', BlogDelete.as_view(), name='blog-delete'),



]
