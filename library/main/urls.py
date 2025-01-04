from django.urls import path, include
from . import views


urlpatterns = [
    path('books/', views.GetAllCreateBooks.as_view(), name='get-all-create-books'),
    path('books/<int:id>/', views.GetDeleteUpdateBookById.as_view(), name='get-delete-update-books'),
    path('books/delivery/', views.DeliveryBooks.as_view(), name='delivery-books'),
    path('authors/', views.GetAllCreateAuthors.as_view(), name='get-all-create-authors'),
    path('authors/<int:id>/', views.GetDeleteUpdateAuthorById.as_view(), name='get-delete-update-authors'),
    path('authors/stat/', views.GetAuthorStat.as_view(), name='get-author-stat'),
    path('authors/<int:id>/stat/', views.GetAuthorStatID.as_view(), name='get-author-stat-id'),
    path('books/copies/', views.GetTopCopies.as_view(), name='get-top-copies'),   
]