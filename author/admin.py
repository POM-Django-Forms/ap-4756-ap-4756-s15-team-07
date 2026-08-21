from django.contrib import admin

from .models import Author


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'surname',
        'patronymic',
        'display_books',
    )

    search_fields = (
        'id',
        'name',
        'surname',
        'patronymic',
    )

    fieldsets = (
        (
            'Author information',
            {
                'fields': (
                    'name',
                    'surname',
                    'patronymic',
                    'display_books',
                )
            },
        ),
    )

    readonly_fields = (
        'display_books',
    )

    def display_books(self, obj):
        return ', '.join(
            book.name
            for book in obj.books.all()
        )

    display_books.short_description = 'Books'