from django.urls import path, include
from apps.books import views


urlpatterns = [
    path('', views.index, name='index'),
    path('page/<int:page>/', views.show_page, name='browser_page'),
    path('book/<slug:book_name>/', views.show_book, name='book_slug'),
]