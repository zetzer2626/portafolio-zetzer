from django.contrib import admin
from .models import Profile, Experience, Certification, Skill, UserSkill

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'phone', 'updated_at']
    list_filter = ['updated_at']
    search_fields = ['user__username', 'user__email', 'location']
    readonly_fields = ['updated_at']

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'user', 'experience_type', 'start_date', 'end_date', 'current']
    list_filter = ['experience_type', 'current', 'start_date', 'user']
    search_fields = ['title', 'company', 'user__username']
    date_hierarchy = 'start_date'
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('user', 'title', 'company', 'experience_type')
        }),
        ('Fechas', {
            'fields': ('start_date', 'end_date', 'current')
        }),
        ('Detalles', {
            'fields': ('description', 'technologies_used', 'achievements', 'location')
        }),
    )

@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ['name', 'issuing_organization', 'user', 'issue_date', 'expiry_date']
    list_filter = ['issue_date', 'expiry_date', 'user']
    search_fields = ['name', 'issuing_organization', 'user__username']
    date_hierarchy = 'issue_date'
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('user', 'name', 'issuing_organization')
        }),
        ('Fechas', {
            'fields': ('issue_date', 'expiry_date')
        }),
        ('Detalles', {
            'fields': ('credential_id', 'credential_url', 'description', 'document')
        }),
    )

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'proficiency_level', 'icon', 'color']
    list_filter = ['category', 'proficiency_level']
    search_fields = ['name']
    list_editable = ['proficiency_level', 'icon', 'color']

@admin.register(UserSkill)
class UserSkillAdmin(admin.ModelAdmin):
    list_display = ['user', 'skill', 'proficiency_level', 'years_experience']
    list_filter = ['proficiency_level', 'skill__category']
    search_fields = ['user__username', 'skill__name']
