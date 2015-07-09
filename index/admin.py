from django.contrib import admin
from index.models import (
    Project,
    Repository,
    Instance,
    Tag,
    Docs,
    Host,
    Dependency,
    Cronjob,
    Virtualenv
)
from notes.models import Note


class RepositoryInline(admin.TabularInline):
    extra = 0
    model = Repository


class NoteInline(admin.TabularInline):
    extra = 0
    model = Note


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
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'hosts')
    list_filter = ('tag',)
    inlines = [
        RepositoryInline,
        InstanceInline,
        DocsInline,
        CronjobInline,
        NoteInline,
    ]


class TagAdmin(admin.ModelAdmin):
    search_fields = ['name']


class HostAdmin(admin.ModelAdmin):
    search_fields = ['name']


class CronjobAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ('project', 'hosts')
    list_display = ('name', 'period', 'user', 'command', 'host_list')


class VirtualenvAdmin(admin.ModelAdmin):
    search_fields = ['name']


class DependencyAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'version', 'dependent_project_count')


admin.site.register(Project, ProjectAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Host, HostAdmin)
admin.site.register(Cronjob, CronjobAdmin)
admin.site.register(Virtualenv, VirtualenvAdmin)
admin.site.register(Dependency, DependencyAdmin)
