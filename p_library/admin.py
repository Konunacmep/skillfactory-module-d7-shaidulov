from django.contrib import admin
from .models import Book, Author, Publisher, Inspiration, Friend, RentedBooks

class inspiration_inline(admin.TabularInline):
    model = Inspiration
    extra = 2

class rentedbooks_inline(admin.TabularInline):
    model = RentedBooks

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    inlines = (inspiration_inline,)

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass

@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    pass

@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    inlines = (rentedbooks_inline,)