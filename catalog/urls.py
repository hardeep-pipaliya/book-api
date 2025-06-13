from django.urls import path
from catalog import views


urlpatterns = [
    path('books/', views.books_list_create),
    path('books/<int:pk>/', views.book_detail_update_delete),
    path('books/<int:pk>/upload-cover/', views.upload_cover),
    
]






