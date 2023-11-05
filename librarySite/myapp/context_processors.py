from .models import Genre, Author, BorrowRequestModel


def genres(request):
    return {'genres': Genre.objects.all()}


def authors(request):
    return {'authors': Author.objects.all()}
