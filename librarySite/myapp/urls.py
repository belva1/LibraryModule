from django.urls import path
from . import views

urlpatterns = [
    path('', views.MainView.as_view(), name='main_view'),

    path('book/create-book/', views.CreateBookView.as_view(), name='create_book_view'),
    path('book/update-book/<str:isbn>', views.UpdateBookView.as_view(), name='update_book_view'),
    path('book/delete-book/<str:isbn>', views.DeleteBookView.as_view(), name='delete_book_view'),
    path('book/<str:isbn>/', views.BookDetailView.as_view(), name='book_detail_view'),

    path('author/create-author/', views.CreateAuthorView.as_view(), name='create_author_view'),
    path('author/update-author/<str:name>', views.UpdateAuthorView.as_view(), name='update_author_view'),
    path('author/delete-author/<str:name>', views.DeleteAuthorView.as_view(), name='delete_author_view'),
    path('author/<str:name>/', views.AuthorView.as_view(), name='author_view'),

    path('genre/create-genre/', views.CreateGenreView.as_view(), name='create_genre_view'),
    path('genre/update-genre/<str:name>', views.UpdateGenreView.as_view(), name='update_genre_view'),
    path('genre/delete-genre/<str:name>', views.DeleteGenreView.as_view(), name='delete_genre_view'),
    path('genre/<str:name>/', views.GenreView.as_view(), name='genre_view'),

    path('borrow/<str:isbn>/', views.CreateBorrowRequestView.as_view(), name='create_borrow_request_view'),
    path('check-borrow/<str:id>/', views.BorrowRequestView.as_view(), name='borrow_request_view'),
    path('request-decline/<str:id>/', views.RequestDeclineView.as_view(), name='request_decline_view'),
    path('request-approve/<str:id>/', views.RequestApproveView.as_view(), name='request_approve_view'),
    path('take-book/<str:id>', views.TakeBookView.as_view(), name='take_book_view'),
    path('return-book/<str:id>', views.ReturnBookView.as_view(), name='return_book_view'),

    path('profile/<str:username>/', views.ProfileView.as_view(), name='profile_view'),
    path('login/', views.LoginView.as_view(), name='login_view'),
    path('register/', views.RegisterView.as_view(), name='register_view'),
    path('logout/', views.LogoutView.as_view(), name='logout_view'),
    path('change-userdata/', views.ChangeUserDataView.as_view(), name='change_user_data_view'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password_view'),
]
