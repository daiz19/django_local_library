from django.contrib import admin

# Register your models here.

from .models import Author, Genre, Book, BookInstance, Language

# admin.site.register(Book)
# admin.site.register(Author)
admin.site.register(Genre)
# admin.site.register(BookInstance)
admin.site.register(Language)

class BookInline(admin.TabularInline):
  model = Book

class AuthorAdmin(admin.ModelAdmin):
  list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
  fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
  inlines = [BookInline]

admin.site.register(Author, AuthorAdmin)

class BookInstanceInline(admin.TabularInline):
  model = BookInstance
  
class BookAdmin(admin.ModelAdmin):
  # list_display = ('title', 'author', 'summary', 'display_genre', 'language')
  list_display = ('title', 'author', 'display_genre')
  inlines = [BookInstanceInline]

admin.site.register(Book, BookAdmin)

class BookInstanceAdmnin(admin.ModelAdmin):
  list_display = ('book', 'status', 'borrower', 'due_back', 'id')
  list_filter = ('status', 'due_back')
  fieldsets = (
    ('Basic Info', {
      'fields': ('book', 'imprint', 'id')
    }),
    ('Avaliability', {
      'fields': ('status', 'due_back', 'borrower')
    }),
  )

admin.site.register(BookInstance, BookInstanceAdmnin)

