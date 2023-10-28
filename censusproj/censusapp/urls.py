from django.urls import path
from censusapp import views

app_name = 'censusapp'

urlpatterns = [
    path('', views.index, name='home'),
    path('all/', views.all_indigene, name='all_indigene'),
    path('about/', views.about, name='about'),
    path('birth-query/', views.birth, name='birth'),
    path('create/', views.create, name='create'),
    path('edit/<pk>', views.IndigeneUpdateView.as_view(), name='edit'),
    path('delete/<pk>', views.IndigeneDeleteView.as_view(), name='delete'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('new-adult/<pk>', views.create_adult, name='new_adult'),
    path('new-child/<pk>', views.create_child, name='new_child'),
    path('query/<str:query>', views.get_query, name='query'),
    path('register/', views.register, name='register')
]
