from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'book',
        'created_at',
        'end_at',
        'plated_end_at',
    )

    list_filter = (
        'book',
        'created_at',
        'end_at',
        'plated_end_at',
    )

    search_fields = (
        'book__name',
        'book__authors__name',
        'book__authors__surname',
        'book__authors__patronymic',
    )