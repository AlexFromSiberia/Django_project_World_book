from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('book_list', views.BookListView.as_view(), name='book_list'),
    path('mybooks', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('allborrowedbooks', views.AllBorrowedBooksListView.as_view(), name='all-borrowed'),
    path('book/<int:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('detail_view/<int:pk>/', views.BookDetailView.as_view(), name='detail_view'),
    path('detail_view/<int:pk>/update/', views.BookUpdate.as_view(), name='book_update'),
    path('detail_view/<int:pk>/delete/', views.BookDelete.as_view(), name='book_delete'),
    path('detail_view/create/', views.BookCreate.as_view(), name='book_create'),
    path('author/all', views.AuthorListView.as_view(), name='author_list'),
    path('author/detail_view/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('author/detail_view/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author_update'),
    path('author/detail_view/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author_delete'),
    path('author/detail_view/create/', views.AuthorCreate.as_view(), name='author_create'),
]
