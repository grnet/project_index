from django.contrib import admin
from index.models import Project, Repository, Instance, Tag, Docs, Host, Dependency


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
    list_display = ('name', 'hosts')
    list_filter = ('tag',)
    inlines = [
        RepositoryInline,
        InstanceInline,
        DocsInline
    ]


class DependencyAdmin(admin.ModelAdmin):
    list_display = ('name', 'version')

admin.site.register(Project, ProjectAdmin)
admin.site.register(Tag)
admin.site.register(Host)
admin.site.register(Dependency, DependencyAdmin)
