from django.urls import path
from django.conf import settings 
from django.conf.urls.static import static 
from .views import *
from home import views

urlpatterns = [
    path('', views.Index.as_view(), name = 'index'),
    path('demo/', views.ShipDetection_view, name = 'upload'),
    path('predicting/<scale>', views.predict, name = 'predict'),
    # path('predicting/', views.predict, name = 'process'),
    path('result/', views.display_ship_images, name = 'result')
]

if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, 
    document_root=settings.MEDIA_ROOT)