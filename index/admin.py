from django import forms
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
    Virtualenv,
    Database,
    ViewDependency,
    DeploymentInfo
)
from notes.models import Note


class RepositoryInline(admin.TabularInline):
    extra = 0
    model = Repository


class NoteInline(admin.TabularInline):
    extra = 0
    model = Note.project.through


class InstanceInline(admin.TabularInline):
    extra = 0
    model = Instance


class DocsInline(admin.TabularInline):
    extra = 0
    model = Docs


class CronjobInline(admin.TabularInline):
    extra = 0
    model = Cronjob


class CronjobTroughInline(admin.TabularInline):
    extra = 0
    model = Cronjob.hosts.through


class DatabaseTroughInline(admin.TabularInline):
    extra = 0
    model = Database.instances.through


class NoteDatabaseInline(admin.TabularInline):
    extra = 0
    model = Note.database.through


class ViewDependencyInline(admin.TabularInline):
    extra = 0
    model = ViewDependency


class ProjectAdmin(admin.ModelAdmin):
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'hosts', 'databases')
    list_filter = ('tag', 'instance__host')
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
    list_filter = ('instance__project__name', )
    list_display = ('name', 'cronjob_list', 'project_list')
    inlines = [
        InstanceInline,
        CronjobTroughInline,
    ]


class CronjobAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ('project', 'hosts')
    list_display = ('name', 'period', 'user', 'command', 'host_list')


class VirtualenvAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'path')


class DependencyAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'version', 'dependent_project_count')


class AdminDatabaseForm(forms.ModelForm):
    passwd = forms.CharField(widget=forms.PasswordInput(), required=False)


class DatabaseAdmin(admin.ModelAdmin):
    form = AdminDatabaseForm
    search_fields = ['name']
    list_display = (
        'name',
        'user',
        # 'passwd',
        'host',
        'port',
        'engine',
        'get_project',
        'app_name'
    )
    list_filter = ('instances__project__name', )

    inlines = [
        NoteDatabaseInline,
        ViewDependencyInline
    ]

    def get_project(self, obj):
        return ', '.join(['%s (%s)' % (i.project.name, i.instance_type) for i in obj.instances.all()])
    get_project.short_description = 'Project'
    get_project.admin_order_field = 'instances__project__name'


class InstanceAdmin(admin.ModelAdmin):
    list_display = ('project', 'instance_type', 'description', 'databases')
    inlines = [
        DatabaseTroughInline,
    ]


class ViewDependencyAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'in_db', 'to_dbs_list', 'create_view')


admin.site.register(Database, DatabaseAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Instance, InstanceAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Host, HostAdmin)
admin.site.register(Cronjob, CronjobAdmin)
admin.site.register(Virtualenv, VirtualenvAdmin)
admin.site.register(Dependency, DependencyAdmin)
admin.site.register(ViewDependency, ViewDependencyAdmin)
admin.site.register(Repository)
admin.site.register(DeploymentInfo)
