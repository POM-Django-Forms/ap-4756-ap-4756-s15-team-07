from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from authentication.models import CustomUser

from .models import Book


def book_list(request):
    books = Book.objects.all()

    name = request.GET.get("name", "").strip()
    author = request.GET.get("author", "").strip()
    description = request.GET.get("description", "").strip()
    count = request.GET.get("count", "").strip()

    if name:
        books = books.filter(name__icontains=name)

    if author:
        for word in author.split():
            books = books.filter(
                Q(authors__name__icontains=word)
                | Q(authors__surname__icontains=word)
                | Q(authors__patronymic__icontains=word)
            )

    if description:
        books = books.filter(description__icontains=description)

    if count:
        books = books.filter(count=count)

    books = books.distinct()

    is_librarian = False

    user_id = request.session.get("user_id")

    if user_id:
        user = get_object_or_404(
            CustomUser,
            id=user_id,
        )
        is_librarian = user.role == 1

    return render(
        request,
        "book/book_list.html",
        {
            "books": books,
            "name": name,
            "author": author,
            "description": description,
            "count": count,
            "is_librarian": is_librarian,
        },
    )


def book_detail(request, book_id):
    book = get_object_or_404(
        Book,
        id=book_id,
    )

    is_librarian = False

    user_id = request.session.get("user_id")

    if user_id:
        user = get_object_or_404(
            CustomUser,
            id=user_id,
        )
        is_librarian = user.role == 1

    return render(
        request,
        "book/book_detail.html",
        {
            "book": book,
            "is_librarian": is_librarian,
        },
    )