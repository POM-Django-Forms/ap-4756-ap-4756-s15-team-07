from django.contrib import admin

from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'description',
        'publication_year',
        'count',
        'display_authors',
    )

    search_fields = (
        'id',
        'name',
        'authors__name',
        'authors__surname',
        'authors__patronymic',
    )

    list_filter = (
        'id',
        'name',
        'authors',
    )

    readonly_fields = (
        'display_authors',
    )

    fieldsets = (
        (
            'Book information',
            {
                'fields': (
                    'name',
                    'description',
                    'authors',
                    'publication_year',
                )
            },
        ),
        (
            'Library information',
            {
                'fields': (
                    'count',
                )
            },
        ),
    )

    def display_authors(self, obj):
        return ', '.join(
            f'{author.name} {author.surname}'
            for author in obj.authors.all()
        )

    display_authors.short_description = 'Authors'