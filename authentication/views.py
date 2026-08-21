from django.shortcuts import get_object_or_404, redirect, render

from .models import CustomUser


def register(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        middle_name = request.POST.get("middle_name")
        last_name = request.POST.get("last_name")
        role = int(request.POST.get("role"))

        if CustomUser.objects.filter(email=email).exists():
            return render(
                request,
                "auth/register.html",
                {"error": "User already exists"},
            )

        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            role=role,
        )

        request.session["user_id"] = user.id

        return redirect("login")

    return render(request, "auth/register.html")


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = CustomUser.objects.filter(email=email).first()

        if user and user.check_password(password):
            request.session["user_id"] = user.id
            return redirect("book_list")

        return render(
            request,
            "auth/login.html",
            {"error": "Invalid email or password"},
        )

    return render(request, "auth/login.html")


def logout_view(request):
    request.session.flush()
    return redirect("login")


def user_list(request):
    user_id = request.session.get("user_id")

    if not user_id:
        return redirect("login")

    current_user = get_object_or_404(
        CustomUser,
        id=user_id,
    )

    if current_user.role != 1:
        return redirect("book_list")

    users = CustomUser.get_all()

    return render(
        request,
        "auth/user_list.html",
        {"users": users},
    )


def user_detail(request, user_id):
    current_user_id = request.session.get("user_id")

    if not current_user_id:
        return redirect("login")

    current_user = get_object_or_404(
        CustomUser,
        id=current_user_id,
    )

    if current_user.role != 1:
        return redirect("book_list")

    user = get_object_or_404(
        CustomUser,
        id=user_id,
    )

    return render(
        request,
        "auth/user_detail.html",
        {"user": user},
    )