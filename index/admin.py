from django.contrib import admin
from index.models import (
    Project,
    Repository,
    Instance,
    Tag,
    Docs,
    Host,
    Dependency,
    Cronjob
)


class RepositoryInline(admin.TabularInline):
    extra = 0
    model = Repository


class InstanceInline(admin.TabularInline):
    extra = 0
    model = Instance


class DocsInline(admin.TabularInline):
    extra = 0
    model = Docs


class CronjobInline(admin.TabularInline):
    extra = 0
    model = Cronjob


class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'hosts')
    list_filter = ('tag',)
    inlines = [
        RepositoryInline,
        InstanceInline,
        DocsInline,
        CronjobInline,
    ]


class DependencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'version', 'dependent_project_count')

admin.site.register(Project, ProjectAdmin)
admin.site.register(Tag)
admin.site.register(Host)
admin.site.register(Cronjob)
admin.site.register(Dependency, DependencyAdmin)
