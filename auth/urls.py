from django.urls import path


from auth import views


urlpatterns = [
    path('login/', views.Login, name = 'login'),
    path('logout/', views.Logout, name = 'logout'),
    path('signup/', views.Signup , name = 'signup')
]