from datetime import timedelta

from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from authentication.models import CustomUser
from book.models import Book

from .models import Order


def order_list(request):
    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("login")

    user = get_object_or_404(CustomUser, id=user_id)

    if user.role != 1:
        return redirect("my_orders")

    orders = Order.get_all()

    return render(
        request,
        "order/order_list.html",
        {"orders": orders},
    )


def my_orders(request):
    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("login")

    user = get_object_or_404(CustomUser, id=user_id)

    if user.role == 1:
        return redirect("order_list")

    orders = Order.objects.filter(user=user)

    return render(
        request,
        "order/my_orders.html",
        {"orders": orders},
    )


def create_order(request):
    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("login")

    user = get_object_or_404(CustomUser, id=user_id)

    if user.role == 1:
        return redirect("book_list")

    if request.method == "POST":
        book_id = request.POST.get("book_id")

        if not book_id:
            return redirect("book_list")

        book = get_object_or_404(Book, id=book_id)

        if book.count <= 0:
            return render(
                request,
                "order/create_order.html",
                {
                    "book": book,
                    "error": "Book is not available.",
                },
            )

        planned_end = timezone.now() + timedelta(days=14)

        order = Order.create(
            user=user,
            book=book,
            plated_end_at=planned_end,
        )

        if order is None:
            return render(
                request,
                "order/create_order.html",
                {
                    "book": book,
                    "error": "Book is not available.",
                },
            )

        book.count -= 1
        book.save()

        return redirect("my_orders")

    book_id = request.GET.get("book_id")

    if not book_id:
        return redirect("book_list")

    book = get_object_or_404(Book, id=book_id)

    return render(
        request,
        "order/create_order.html",
        {"book": book},
    )


def close_order(request, order_id):
    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("login")

    user = get_object_or_404(CustomUser, id=user_id)

    if user.role != 1:
        return redirect("my_orders")

    if request.method != "POST":
        return redirect("order_list")

    order = get_object_or_404(Order, id=order_id)

    if order.end_at is None:
        order.update(end_at=timezone.now())

        book = order.book
        book.count += 1
        book.save()

    return redirect("order_list")