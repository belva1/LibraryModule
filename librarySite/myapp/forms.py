from django import forms
from django.utils import timezone

from .models import Genre, Book, Author, UserProfile
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

UserModel = get_user_model()


class LoginViewForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput(
        attrs={
            'placeholder': 'Username',
            'class': 'form-control',
        }
    ))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Password',
            'class': 'form-control',
        }
    ))

    def clean(self):
        if not authenticate(**self.cleaned_data):
            raise ValidationError('Incorrect username or password.')


class RegisterViewForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput(
        attrs={
            'placeholder': 'Username',
            'class': 'form-control',
        }
    ))
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(
        attrs={
            'placeholder': 'First Name',
            'class': 'form-control',
        }
    ))
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(
        attrs={
            'placeholder': 'Last Name',
            'class': 'form-control',
        }
    ))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Password',
            'class': 'form-control',
        }
    ))
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Confirm Password',
            'class': 'form-control',
        }
    ))

    def clean(self):
        username = self.cleaned_data['username']
        try:
            UserModel.objects.get(username=username)
            self.add_error('username', 'User with this username already exist.')
        except UserModel.DoesNotExist:
            if self.cleaned_data['password'] != self.cleaned_data['confirm_password']:
                self.add_error('password', 'Password does not match.')
                self.add_error('confirm_password', 'Confirm password does not match.')

    def create_user(self):
        del self.cleaned_data['confirm_password']
        UserModel.objects.create_user(**self.cleaned_data)


class ChangePasswordForm(forms.ModelForm):
    new_password = forms.CharField(widget=forms.PasswordInput, label='New Password:')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirm Password:')

    class Meta:
        model = User
        fields = ('new_password', 'confirm_password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        password = self.cleaned_data["new_password"]
        confirm_password = self.cleaned_data["confirm_password"]
        if password != confirm_password:
            self.add_error("new_password", "Does not match")
            self.add_error("confirm_password", "Does not match")

    def change_password(self, user):
        password = self.cleaned_data["new_password"]
        user.set_password(password)
        user.save()


class ChangeUserDataForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        labels = {
            'username': 'Username',
            'email': 'Email',
            'first_name': 'First Name',
            'last_name': 'Last Name'
        }
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
            'email': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class CreateNewGenreForm(forms.Form):
    name = forms.CharField(label='Name', widget=forms.TextInput(
        attrs={
            'placeholder': 'Name',
            'class': 'form-control',
        }
    ))

    def clean(self):
        name = self.cleaned_data['name']
        if len(Genre.objects.filter(name=name)):
            self.add_error('name', 'Genre with this name already exist.')

    def create_genre(self):
        Genre.objects.create(**self.cleaned_data)


class UpdateGenreForm(forms.Form):
    name = forms.CharField(label='Name', widget=forms.TextInput(
        attrs={
            'placeholder': 'Name',
            'class': 'form-control',
        }
    ))

    def clean(self):
        name = self.cleaned_data['name']
        if len(Genre.objects.filter(name=name)):
            self.add_error('name', 'Genre with this name already exist.')


class CreateNewAuthorForm(forms.Form):
    name = forms.CharField(label='Name', widget=forms.TextInput(
        attrs={
            'placeholder': 'Name',
            'class': 'form-control',
        }
    ))
    bio = forms.CharField(label='Bio', widget=forms.TextInput(
        attrs={
            'placeholder': 'Bio',
            'class': 'form-control',
        }
    ))

    def clean(self):
        name = self.cleaned_data['name']
        if Author.objects.filter(name=name).exists():
            self.add_error('name', 'Author with this name already exists.')

    def create_author(self):
        Author.objects.create(**self.cleaned_data)


class UpdateAuthorForm(forms.Form):
    name = forms.CharField(label='Name', widget=forms.TextInput(
        attrs={
            'placeholder': 'Name',
            'class': 'form-control',
        }
    ))
    bio = forms.CharField(label='Bio', widget=forms.TextInput(
        attrs={
            'placeholder': 'Bio',
            'class': 'form-control',
        }
    ))

    def clean(self):
        name = self.cleaned_data['name']
        if len(Author.objects.filter(name=name)):
            self.add_error('name', 'Author with this name already exist.')


class CreateNewBookForm(forms.Form):
    title = forms.CharField(label='Title', widget=forms.TextInput(
        attrs={
            'placeholder': 'Title',
            'class': 'form-control',
        }
    ))
    summary = forms.CharField(label='Summary', widget=forms.Textarea(
        attrs={
            'placeholder': 'Summary',
            'class': 'form-control',
        }
    ))
    isbn = forms.CharField(label='ISBN', widget=forms.TextInput(
        attrs={
            'placeholder': 'ISBN',
            'class': 'form-control',
        }
    ))
    published_date = forms.DateField(label='Published Date',widget=forms.DateInput(
        attrs={
            'type': 'date',
            'class': 'form-control'
        }
    ))
    publisher = forms.CharField(label='Publisher', widget=forms.TextInput(
        attrs={
            'placeholder': 'Publisher',
            'class': 'form-control',
        }
    ))
    genre = forms.ModelMultipleChoiceField(label='Genre', queryset=Genre.objects.all(), widget=forms.SelectMultiple(
        attrs={
            'class': 'form-control',
        }
    ))
    authors = forms.ModelMultipleChoiceField(label='Authors', queryset=Author.objects.all(), widget=forms.SelectMultiple(
        attrs={
            'class': 'form-control',
        }
    ))
    borrower = forms.ModelChoiceField(label='Borrower', queryset=UserProfile.objects.all(), required=False, widget=forms.Select(
        attrs={
            'class': 'form-control',
        }
    ))

    def clean(self):
        title = self.cleaned_data['title']
        if len(Book.objects.filter(title=title)):
            self.add_error('title', 'Book with this title already exist.')
        isbn = self.cleaned_data['isbn']
        if len(Book.objects.filter(isbn=isbn)):
            self.add_error('isbn', 'Book with this isbn already exist.')
        date = self.cleaned_data['published_date']
        if date > timezone.now().date():
            self.add_error('published_date', 'Unreal date for field "published date".')

    def create_book(self):
        genre = self.cleaned_data['genre']
        authors = self.cleaned_data['authors']

        book = Book.objects.create(
            title=self.cleaned_data['title'],
            summary=self.cleaned_data['summary'],
            isbn=self.cleaned_data['isbn'],
            published_date=self.cleaned_data['published_date'],
            publisher=self.cleaned_data['publisher'],
            available=True,
            borrower=self.cleaned_data['borrower']
        )

        book.genre.set(genre)
        book.authors.set(authors)
        book.save()


class UpdateBookForm(forms.Form):
    title = forms.CharField(label='Title', widget=forms.TextInput(
        attrs={
            'placeholder': 'Title',
            'class': 'form-control',
        }
    ))
    summary = forms.CharField(label='Summary', widget=forms.Textarea(
        attrs={
            'placeholder': 'Summary',
            'class': 'form-control',
        }
    ))
    published_date = forms.DateField(label='Published Date', widget=forms.DateInput(
        attrs={
            'type': 'date',
            'class': 'form-control'
        }
    ))
    publisher = forms.CharField(label='Publisher', widget=forms.TextInput(
        attrs={
            'placeholder': 'Publisher',
            'class': 'form-control',
        }
    ))
    genre = forms.ModelMultipleChoiceField(label='Genre', queryset=Genre.objects.all(), widget=forms.SelectMultiple(
        attrs={
            'class': 'form-control',
        }
    ))
    authors = forms.ModelMultipleChoiceField(label='Authors', queryset=Author.objects.all(), widget=forms.SelectMultiple(
        attrs={
            'class': 'form-control',
        }
    ))
    borrower = forms.ModelChoiceField(label='Borrower', queryset=UserProfile.objects.all(), required=False, widget=forms.Select(
        attrs={
            'class': 'form-control',
        }
    ))

    def clean(self):
        title = self.cleaned_data['title']
        if len(Book.objects.filter(title=title)):
            self.add_error('title', 'Book with this title already exist.')
        date = self.cleaned_data['published_date']
        if date > timezone.now().date():
            self.add_error('published_date', 'Unreal date for field "published date".')
