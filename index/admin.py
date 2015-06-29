from django.contrib import admin
from index.models import Project, Repository, Instance, Tag, Docs, Host


class RepositoryInline(admin.TabularInline):
    extra = 0
    model = Repository


class InstanceInline(admin.TabularInline):
    extra = 0
    model = Instance


class DocsInline(admin.TabularInline):
    extra = 0
    model = Docs


class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    inlines = [
        RepositoryInline,
        InstanceInline,
        DocsInline
    ]

admin.site.register(Project, ProjectAdmin)
admin.site.register(Tag)
admin.site.register(Host)
