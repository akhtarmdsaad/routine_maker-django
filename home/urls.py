
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('fixed/',views.fixed,name="fixed"),
    path('needed/',views.needed_stuffs,name="needed"),
    path('preferred/',views.preferred,name="preferred"),
    path('result/',views.result,name="result"),
]