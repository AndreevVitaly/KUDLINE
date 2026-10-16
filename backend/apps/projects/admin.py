from django.contrib import admin
from .models import Project, ProjectImage
class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "location", "year", "published", "featured", "updated_at")
    list_filter = ("published", "featured", "year")
    search_fields = ("title", "location", "description")
    prepopulated_fields = {"slug": ("title",)}
    inlines = (ProjectImageInline,)

