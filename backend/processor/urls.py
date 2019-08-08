from django.urls import path

from .views import StartJobView

app_name = 'processor'

urlpatterns = [
    path('start/', StartJobView.as_view(), name='start_job'),
]