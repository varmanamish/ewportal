from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('doctors', views.doctors, name="doctors"),
    path('chatbot', views.chatbot, name="chatbot"),
    path('departments', views.departments, name="departments"),
    path('elements', views.elements, name="elements"),
    path('contact', views.contact, name="contact"),
    path('login', views.login, name="login"),
    path('register', views.register, name="register"),
    path('profile',views.profile,name="profile"),
    path('logout', views.logout, name='logout'),
]