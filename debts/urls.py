from django.urls import path
from . import views

app_name = 'debts'
urlpatterns = [
    path('', views.debt_list, name='list'),
    path('stats/', views.debt_stats, name='stats'),
    path('search/', views.search_debts, name='search'),
    path('<int:debt_id>/', views.debt_detail, name='detail'),
]