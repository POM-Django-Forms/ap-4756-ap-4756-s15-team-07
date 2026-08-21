from django.shortcuts import get_object_or_404, redirect, render

from authentication.models import CustomUser

from .models import Author


def author_list(request):
    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("login")

    user = get_object_or_404(CustomUser, id=user_id)

    if user.role != 1:
        return redirect("book_list")

    authors = Author.get_all()

    return render(
        request,
        "author/author_list.html",
        {"authors": authors},
    )


def create_author(request):
    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("login")

    user = get_object_or_404(CustomUser, id=user_id)

    if user.role != 1:
        return redirect("book_list")

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        surname = request.POST.get("surname", "").strip()
        patronymic = request.POST.get("patronymic", "").strip()

        author = Author.create(
            name=name,
            surname=surname,
            patronymic=patronymic,
        )

        if author is None:
            return render(
                request,
                "author/create_author.html",
                {"error": "Invalid author data."},
            )

        return redirect("author_list")

    return render(request, "author/create_author.html")


def delete_author(request, author_id):
    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("login")

    user = get_object_or_404(CustomUser, id=user_id)

    if user.role != 1:
        return redirect("book_list")

    author = get_object_or_404(Author, id=author_id)

    if author.books.exists():
        return redirect("author_list")

    author.delete()

    return redirect("author_list")