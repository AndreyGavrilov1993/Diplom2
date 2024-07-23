from django.urls import path
from . import views

urlpatterns = [
    path('', views.book, name='book'),
    path('book/', views.book, name='book_booking'),
    path('book_computer/', views.book_computer, name='book_computer'),
    path('book_printing/', views.book_printing, name='book_printing'),
]