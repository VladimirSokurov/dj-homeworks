from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from books.models import Book
import datetime


def index(request):
    return redirect('/books/')

def books_view(request, pub_date=None):
    template = 'books/books_list.html'
    books = Book.objects.all()
    unique_dates = set(book.pub_date.strftime("%Y-%m-%d") for book in books)
    unique_dates = sorted(list(unique_dates))
    print(unique_dates)
    if pub_date:
        filtred_books = Book.objects.filter(pub_date=pub_date)
        # filtred_books = Book.objects.all()
        print(filtred_books)

        # page_number = int(request.GET.get("page", 1))
        paginator = Paginator(unique_dates, 1)
        page = paginator.get_page(1)

        context = {
            'books': filtred_books,
            'page': page,
            'pub_date': pub_date
        }

    else:
        context = {
                'books': books,
                'pub_date': pub_date
            }
    # print(books[0].pub_date)
    # print(date)
    return render(request, template, context)
