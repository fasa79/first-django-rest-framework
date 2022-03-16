from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', views.Thd_list.as_view()),
    path('<int:pk>/', views.Thd_detail.as_view()),
    # path('heatmap_overall/', views.HeatMapOverallView.as_view()),
    path('heatmap_overall/', views.HeatMapOverallList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
