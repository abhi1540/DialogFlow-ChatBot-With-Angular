from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from . import views

app_name='covid19dashboardapi'

# router = routers.DefaultRouter()
# router.register(r"test", views.Webhook.as_view())
# router.register(r'covidapicountrywise', views.getCoviddetails, name="covidcountry")
# urlpatterns = router.urls
urlpatterns = [
    #path('', include(router.urls), basename='test'),
    # path(r'users', views.UserViewSet.as_view()),
    path(r"test", views.Webhook.as_view()),
    # path(r'covidapi', views.getCoviddetails),
    path(r'covidapicountrywise/', views.getCoviddetails, name="covidcountry"),
    #path(r"saveconv", views.func),

    ]
