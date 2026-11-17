from django.urls import path

from ads import views

urlpatterns = [
    path('', views.AdListView.as_view(), name='ad_list'),
    path('my/', views.MyAdListView.as_view(), name='my_ads'),
    path('ads/create/', views.AdCreateView.as_view(), name='ad_create'),
    path('ads/<int:pk>/', views.AdDetailView.as_view(), name='ad_detail'),
    path('ads/<int:pk>/edit/', views.AdUpdateView.as_view(), name='ad_update'),
    path('ads/<int:pk>/delete/', views.AdDeleteView.as_view(), name='ad_delete'),
]
