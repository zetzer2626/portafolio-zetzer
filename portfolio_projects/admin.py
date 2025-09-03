from django.contrib import admin
from .models import Category, Technology, Project, ProjectImage, ProjectFile, Comment, Vote

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color']
    list_editable = ['color']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon']
    search_fields = ['name']
    list_editable = ['icon']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_categories', 'is_featured', 'created_at', 'views', 'get_likes_count', 'get_dislikes_count']
    list_filter = ['categories', 'is_featured', 'created_at', 'technologies']
    search_fields = ['title', 'description', 'content']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['technologies']
    readonly_fields = ['views', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('title', 'slug', 'description', 'content', 'categories')
        }),
        ('Imagen y URLs', {
            'fields': ('featured_image', 'github_url', 'live_url')
        }),
        ('Tecnologías y Configuración', {
            'fields': ('technologies', 'is_featured')
        }),
        ('Estadísticas', {
            'fields': ('views', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_categories(self, obj):
        return ", ".join([cat.name for cat in obj.categories.all()])
    get_categories.short_description = 'Categorías'

@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'order', 'is_cover', 'created_at']
    list_filter = ['is_cover', 'created_at', 'project']
    search_fields = ['title', 'project__title']
    list_editable = ['order', 'is_cover']
    date_hierarchy = 'created_at'
    ordering = ['project', 'order']

@admin.register(ProjectFile)
class ProjectFileAdmin(admin.ModelAdmin):
    list_display = ['name', 'project', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['name', 'project__title']
    date_hierarchy = 'uploaded_at'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'project', 'created_at', 'is_approved']
    list_filter = ['is_approved', 'created_at', 'project']
    search_fields = ['content', 'user__username', 'project__title']
    list_editable = ['is_approved']
    date_hierarchy = 'created_at'

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'project', 'vote_type', 'created_at']
    list_filter = ['vote_type', 'created_at', 'project']
    search_fields = ['user__username', 'project__title']
    date_hierarchy = 'created_at'
