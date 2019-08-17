from django.urls import path

from .views import StartJobView, StatusView, GetCrawledDataView

app_name = 'processor'

urlpatterns = [
    path('start/', StartJobView.as_view(), name='start'),
    path('status/', StatusView.as_view({'post': 'list'})),
    path('crawled-data/', GetCrawledDataView.as_view({'post': 'list'}))
]