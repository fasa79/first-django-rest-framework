from unicodedata import name
from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', views.Thd_list.as_view(), name='all-data'),
    path('<int:pk>/', views.Thd_detail.as_view()),
    path('heatmap_overall/', views.HeatMapOverall.as_view(), name='thd-overall-heat-map'),
    path('topcomplaintsite_overall/', views.OverallTopComplaintSites.as_view(), name='thd-overall-top-complaint-site'),
]

urlpatterns = format_suffix_patterns(urlpatterns)