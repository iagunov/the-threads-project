from django.contrib import admin

from .models import Comment, Group, Post, Follow


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'created', 'author', 'group')
    list_editable = ('group',)
    search_fields = ('text',)
    list_filter = ('created',)
    empty_value_display = '-пусто-'


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('slug', 'title', 'description')
    list_filter = ('title', 'slug')
    list_editable = ('title', 'description')
    search_fields = ('slug', 'title', 'description')
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'text')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
