from django.contrib import admin
from .models import Author, Genre, Book, BookInstance, Language

# class AuthorAdmin(admin.ModelAdmin):
    #pass

# Register your models here.
# admin.site.register(Book)
# admin.site.register(Author)
# admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre)
# #admin.site.register(BookInstance)
admin.site.register(Language)

# Improved way to implement
class BookInline(admin.TabularInline):
    model = Book
    extra = 0

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display=('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]

class BookInstanceInline(admin.TabularInline):
    model=BookInstance
    extra = 0

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display=('title', 'author', 'display_genre', 'language')
    inlines = [BookInstanceInline]

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display=('book', 'author', 'borrower', 'id')
    list_filter=('status', 'due_back')

    fieldsets=(
            ( None, {
                    'fields': ('book', 'author', 'imprint', 'id')
            }),
            ( 'Availability', {
                    'fields': ('status', 'due_back', 'borrower')
            }),
        )

