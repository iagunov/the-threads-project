from django.contrib import admin

from .models import Idea, Tag, TagIdea, Team, TeamUser

class TeamUserInline(admin.TabularInline):
    model = TeamUser
    fk_name = 'team'
    can_delete = False
    verbose_name_plural = 'TeaMembers'


class TeamInLine(admin.StackedInline):
    model = Team
    can_delete = False
    verbose_name_plural = 'Teams'

class TeamAdmin(admin.ModelAdmin):
    list_display = ('pk', 'idea', 'owner')
    search_fields = ('idea',)
    empty_value_display = '-пусто-'
    inlines = (TeamUserInline,)

class TagInline(admin.TabularInline):
    model = TagIdea
    fk_name = 'idea'
    can_delete = False
    verbose_name_plural = 'Tags'

class IdeaAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'created', 'author')
    search_fields = ('title',)
    list_filter = ('created',)
    empty_value_display = '-пусто-'
    inlines = (TeamInLine, TagInline,)

class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')
    empty_value_display = '-пусто-'


admin.site.register(Idea, IdeaAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Tag, TagAdmin)