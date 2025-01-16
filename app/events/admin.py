# events/admin.py

from django.contrib import admin
from .models import User, Category, Event, Comment


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'registration_method', 'is_email_password_enabled')
    search_fields = ('username', 'email')
    list_filter = (
    'registration_method', 'is_email_password_enabled')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'date', 'price', 'get_categories')
    search_fields = ('name', 'region', 'categories__name')
    list_filter = ('date', 'price', 'categories')

    def get_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])

    get_categories.short_description = 'Categories'  # Name to column


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'created_at', 'content')
    search_fields = ('user__username', 'event__name', 'content')
    list_filter = ('created_at', 'event')


admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Comment, CommentAdmin)
