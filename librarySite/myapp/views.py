from datetime import timedelta

from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, ListView, DetailView

from .forms import *
from .models import UserProfile, Book, Author, Genre, BorrowRequestModel


# MAIN VIEW
class MainView(ListView):
    template_name = 'books/index.html'
    context_object_name = 'books'

    def get_queryset(self):
        return Book.objects.all()


# VIEWS FOR USER FUNCTIONALITY (LOGIN, REGISTRATION, PROFILE, CHANGE USER DATA, CHANGE PASSWORD, LOGOUT)
class LoginView(View):
    template_name = 'user/login_view.html'

    def get(self, request):
        form = LoginViewForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginViewForm(request.POST)
        if form.is_valid():
            user = authenticate(**form.cleaned_data)
            if user is not None:
                login(request, user)
                url = reverse('profile_view', kwargs={'username': user.username})
                return HttpResponseRedirect(url)
        return render(request, self.template_name, {'form': form})


class RegisterView(View):
    template_name = 'user/register_view.html'

    def get(self, request):
        form = RegisterViewForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegisterViewForm(request.POST)
        if form.is_valid():
            form.create_user()
            url = reverse('login_view')
            return HttpResponseRedirect(url)
        return render(request, self.template_name, {'form': form})


class ProfileView(DetailView):
    template_name = 'user/profile_view.html'
    model = UserProfile
    context_object_name = 'user'

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        return self.model.objects.get(username=username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        if user.is_librarian:
            context['borrow_requests'] = BorrowRequestModel.objects.filter(status=1)
        user_requests = BorrowRequestModel.objects.filter(borrower=user)
        context['user_requests'] = user_requests
        return context


class ChangeUserDataView(View):
    template_name = 'user/change_user_data_view.html'
    form_class = ChangeUserDataForm
    model = User

    def get_object(self, queryset=None):
        return self.request.user

    def get(self, request):
        if not self.request.user.is_authenticated:
            return redirect('login_view')
        user_data = {
            'username': request.user.username,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        }
        form = self.form_class(user_data)
        return render(request, self.template_name, {'form': form})

    def get_success_url(self):
        return reverse_lazy('profile_view', kwargs={'username': self.request.user.username})

    def post(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login_view')

        form = self.form_class(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(self.get_success_url())

        return render(request, self.template_name, {'form': form})


class ChangePasswordView(View):
    template_name = 'user/change_password_view.html'
    form_class = ChangePasswordForm
    success_url = reverse_lazy('login_view')

    def get(self, request):
        if not self.request.user.is_authenticated:
            return redirect('login_view')
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.change_password(request.user)
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})


class LogoutView(View):

    def get(self, request):
        url = reverse('login_view')
        logout(request)
        return HttpResponseRedirect(url)


# VIEWS FOR GENRE FUNCTIONALITY(GENRE VIEW, CREATE, UPDATE, DELETE)
class GenreView(DetailView):
    model = Genre
    template_name = 'genres/genre_view.html'
    context_object_name = 'genre'

    def get_object(self, queryset=None):
        name = self.kwargs.get('name')
        return self.model.objects.get(name=name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cur_genre = self.get_object()
        context['books'] = Book.objects.filter(genre=cur_genre)
        context['genre'] = cur_genre
        return context


class CreateGenreView(CreateView):
    model = Genre
    template_name = 'genres/create_genre_view.html'

    def get(self, request):
        if not request.user.is_librarian and not request.user.is_staff:
            url = reverse('main_view')
            return HttpResponseRedirect(url)
        form = CreateNewGenreForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CreateNewGenreForm(request.POST)
        if form.is_valid():
            form.create_genre()
            url = reverse('main_view')
            return HttpResponseRedirect(url)
        return render(request, self.template_name, {'form': form})


class UpdateGenreView(View):
    template_name = 'genres/update_genre_view.html'

    def get(self, request, name):
        if not request.user.is_librarian and not request.user.is_staff:
            url = reverse('main_view')
            return HttpResponseRedirect(url)
        genre = Genre.objects.get(name=name)
        form = UpdateGenreForm({'name': genre.name})

        return render(request, self.template_name, {'form': form})

    def post(self, request, name):
        genre = Genre.objects.get(name=name)
        form = UpdateGenreForm(request.POST)

        if form.is_valid():
            genre.name = form.cleaned_data['name']
            genre.save()
            url = reverse('main_view')
            return HttpResponseRedirect(url)

        return render(request, self.template_name, {'form': form})


class DeleteGenreView(View):
    def get(self, request, name):
        if not request.user.is_librarian and not request.user.is_staff:
            url = reverse('main_view')
            return HttpResponseRedirect(url)
        genre = Genre.objects.get(name=name)
        genre.delete()
        url = reverse('main_view')
        return HttpResponseRedirect(url)


# VIEWS FOR AUTHOR FUNCTIONALITY(AUTHOR VIEW, CREATE, UPDATE, DELETE)
class AuthorView(DetailView):
    model = Author
    template_name = 'authors/author_view.html'
    context_object_name = 'author'

    def get_object(self, queryset=None):
        name = self.kwargs.get('name')
        return self.model.objects.get(name=name)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cur_author = self.get_object()
        context['books'] = Book.objects.filter(authors=cur_author)
        context['author'] = cur_author
        return context


class CreateAuthorView(CreateView):
    model = Author
    template_name = 'authors/create_author_view.html'

    def get(self, request):
        if not request.user.is_librarian and not request.user.is_staff:
            url = reverse('main_view')
            return HttpResponseRedirect(url)
        form = CreateNewAuthorForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CreateNewAuthorForm(request.POST)
        if form.is_valid():
            form.create_author()
            url = reverse('main_view')
            return HttpResponseRedirect(url)
        return render(request, self.template_name, {'form': form})


class UpdateAuthorView(View):
    template_name = 'authors/update_author_view.html'

    def get(self, request, name):
        if not request.user.is_librarian and not request.user.is_staff:
            url = reverse('main_view')
            return HttpResponseRedirect(url)
        author = Author.objects.get(name=name)
        form = UpdateAuthorForm({'name': author.name, 'bio': author.bio})

        return render(request, self.template_name, {'form': form})

    def post(self, request, name):
        author = Author.objects.get(name=name)
        form = UpdateAuthorForm(request.POST)

        if form.is_valid():
            author.name = form.cleaned_data['name']
            author.bio = form.cleaned_data['bio']
            author.save()
            url = reverse('main_view')
            return HttpResponseRedirect(url)

        return render(request, self.template_name, {'form': form})


class DeleteAuthorView(View):
    def get(self, request, name):
        if not request.user.is_librarian and not request.user.is_staff:
            url = reverse('main_view')
            return HttpResponseRedirect(url)
        author = Author.objects.get(name=name)
        author.delete()
        url = reverse('main_view')
        return HttpResponseRedirect(url)


# VIEWS FOR BOOK FUNCTIONALITY(BOOK VIEW, CREATE, UPDATE, DELETE)
class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'

    def get_object(self, queryset=None):
        isbn = self.kwargs.get('isbn')
        return self.model.objects.get(isbn=isbn)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        book = self.get_object()
        if self.request.user.is_authenticated:
            borrow_requests = BorrowRequestModel.objects.filter(borrower=user, book=book)
            if borrow_requests.exists():
                context['borrow_request'] = borrow_requests.first()
            else:
                context['borrow_request'] = None

        return context

    def post(self, request):
        return redirect('main_view')


class CreateBookView(CreateView):
    model = Book
    template_name = 'books/create_book_view.html'

    def get(self, request):
        if not request.user.is_librarian and not request.user.is_staff:
            url = reverse('main_view')
            return HttpResponseRedirect(url)
        form = CreateNewBookForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CreateNewBookForm(request.POST)
        if form.is_valid():
            form.create_book()
            url = reverse('main_view')
            return HttpResponseRedirect(url)
        return render(request, self.template_name, {'form': form})


class UpdateBookView(View):
    template_name = 'books/update_book_view.html'

    def get(self, request, isbn):
        if not request.user.is_librarian and not request.user.is_staff:
            url = reverse('main_view')
            return HttpResponseRedirect(url)
        book = Book.objects.get(isbn=isbn)
        form = UpdateBookForm({
            'title': book.title,
            'summary': book.summary,
            'published_date': book.published_date,
            'publisher': book.publisher,
            'genre': book.genre.all(),
            'authors': book.authors.all(),
            'borrower': book.borrower,
        })

        return render(request, self.template_name, {'form': form})

    def post(self, request, isbn):
        book = Book.objects.get(isbn=isbn)
        form = UpdateBookForm(request.POST)

        if form.is_valid():
            book.title = form.cleaned_data['title']
            book.summary = form.cleaned_data['summary']
            book.published_date = form.cleaned_data['published_date']
            book.publisher = form.cleaned_data['publisher']
            book.borrower = form.cleaned_data['borrower']
            book.genre.set(form.cleaned_data['genre'])
            book.authors.set(form.cleaned_data['authors'])
            book.save()
            url = reverse('main_view')
            return HttpResponseRedirect(url)

        return render(request, self.template_name, {'form': form})


class DeleteBookView(View):
    def get(self, request, isbn):
        if not request.user.is_librarian and not request.user.is_staff:
            url = reverse('main_view')
            return HttpResponseRedirect(url)
        book = Book.objects.get(isbn=isbn)
        book.delete()
        url = reverse('main_view')
        return HttpResponseRedirect(url)


# VIEWS FOR BORROW REQUEST FUNCTIONALITY(REQUESTS / BORROW REQUEST VIEW, APPROVE, DECLINE)
class RequestsView(ListView):
    template_name = 'user/requests_view.html'
    model = BorrowRequestModel
    context_object_name = 'requests'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not (request.user.is_librarian or request.user.is_staff):
            return redirect('main_view')
        return super().dispatch(request, *args, **kwargs)


class BorrowRequestView(DetailView):
    template_name = 'user/borrow_request_view.html'
    model = BorrowRequestModel
    context_object_name = 'borrow_request'

    def get_object(self, queryset=None):
        id = self.kwargs.get('id')
        return self.model.objects.get(id=id)


class CreateBorrowRequestView(View):
    model = BorrowRequestModel

    def get(self, request, *args, **kwargs):
        isbn = self.kwargs['isbn']
        book = Book.objects.get(isbn=isbn)
        user = request.user
        self.model.objects.create(book=book, borrower=user, request_date=timezone.now().date())

        return redirect('profile_view', username=request.user.username)


class RequestApproveView(View):
    model = BorrowRequestModel

    def get(self, request, *args, **kwargs):
        id = kwargs['id']
        book_request = self.model.objects.get(id=id)
        if not request.user.is_authenticated or not request.user.is_librarian:
            url = reverse('main_view')
            return HttpResponseRedirect(url)
        book_request.status = 2
        book_request.approval_date = timezone.now().date()
        book_request.save()

        return redirect('profile_view', username=request.user.username)


class RequestDeclineView(View):
    model = BorrowRequestModel

    def get(self, request, *args, **kwargs):
        id = kwargs['id']
        book_request = self.model.objects.get(id=id)
        if not request.user.is_authenticated or not request.user.is_librarian:
            url = reverse('main_view')
            return HttpResponseRedirect(url)
        book_request.status = 5
        book_request.save()

        return redirect('profile_view', username=request.user.username)


# VIEWS FOR TAKING / RETURNING BOOKS
class TakeBookView(View):
    model = BorrowRequestModel

    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']
        borrow_request = self.model.objects.get(id=id)
        if not request.user.is_authenticated or borrow_request.borrower != request.user:
            url = reverse('main_view')
            return HttpResponseRedirect(url)
        if borrow_request.status != 2:
            return redirect('book_detail_view', isbn=borrow_request.book.isbn)
        else:
            borrow_request.status = 3
            current_date = timezone.now().date()
            new_date = current_date + timedelta(weeks=2)
            borrow_request.due_date = new_date
            borrow_request.save()
            book = borrow_request.book
            book.available = False
            book.save()

        return redirect('profile_view', username=request.user.username)


class ReturnBookView(View):
    model = BorrowRequestModel

    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']
        borrow_request = self.model.objects.get(id=id)
        if not request.user.is_authenticated or borrow_request.borrower != request.user:
            url = reverse('main_view')
            return HttpResponseRedirect(url)
        if borrow_request.status != 3:
            return redirect('book_detail_view', isbn=borrow_request.book.isbn)
        else:
            borrow_request.status = 4
            current_date = timezone.now().date()
            if current_date > borrow_request.due_date:
                borrow_request.overdue = True
            borrow_request.complete_date = current_date
            borrow_request.save()
            book = borrow_request.book
            book.available = True
            book.save()

        return redirect('profile_view', username=request.user.username)