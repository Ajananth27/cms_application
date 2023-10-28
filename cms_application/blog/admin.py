from django.contrib import admin

from .models import *

class BlogAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "created_by"]
    raw_id_fields = ['created_by']
    readonly_fields = ['created_by']

class CommentAdmin(admin.ModelAdmin):
    list_display = ["blog", "created_at"]
    raw_id_fields = ['created_by']
    readonly_fields = ['created_by']

admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentAdmin)
