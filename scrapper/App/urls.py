from django.contrib import admin
from django.urls import path
from App import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.html_view, name='App'),
    path('query/', views.resolve_query, name='App')
]