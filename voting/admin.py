from django.contrib import admin
from .models import Project, Vote

admin.site.site_header = 'City Voting Platform'
admin.site.site_title = 'Admin Area'
admin.site.index_title = 'Welcome to Admin Area'


class VoteInline(admin.TabularInline):
    model = Vote
    extra = 2


class ProjectAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'description']}), ]
    inlines = [VoteInline]


admin.site.register(Project, ProjectAdmin)
