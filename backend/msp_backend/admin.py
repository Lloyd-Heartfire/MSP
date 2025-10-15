from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import (
    UserProfile,
    Pandemic,
    Location,
    DataSource,
    DataFile,
    PandemicData
)

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name = 'Profil utilisateur'
    verbose_name_plural = 'Profils utilisateurs'
    fields = ('user_function', 'user_organization', 'last_connection')

class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_organization')
    
    def get_organization(self, obj):
        return obj.profile.user_organization if hasattr(obj, 'profile') else '-'
    get_organization.short_description = 'Organisation'

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

#AdminPandemic
@admin.register(Pandemic)
class PandemicAdmin(admin.ModelAdmin):
    list_display = ('pandemic_name', 'pathogene_agent', 'who_classification', 'start_date', 'end_date', 'created_at')
    list_filter = ('pathogene_agent', 'who_classification', 'start_date')
    search_fields = ('pandemic_name', 'pandemic_description')
    date_hierarchy = 'start_date'
    ordering = ('-start_date',)
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('pandemic_name', 'pathogene_agent', 'who_classification')
        }),
        ('Description', {
            'fields': ('pandemic_description',)
        }),
        ('Période', {
            'fields': ('start_date', 'end_date')
        }),
        ('Data', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')


#AdminLocation
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('country', 'province_state', 'city', 'iso_code', 'population', 'who_region')
    list_filter = ('who_region', 'country')
    search_fields = ('country', 'province_state', 'city', 'iso_code')
    ordering = ('country', 'province_state')
    
    fieldsets = (
        ('Localisation', {
            'fields': ('country', 'province_state', 'city')
        }),
        ('Codes et régions', {
            'fields': ('iso_code', 'who_region')
        }),
        ('Coordonnées GPS', {
            'fields': ('latitude', 'longitude'),
            'classes': ('collapse',)
        }),
        ('Démographie', {
            'fields': ('population',)
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')


#AdminDataSource
@admin.register(DataSource)
class DataSourceAdmin(admin.ModelAdmin):
    list_display = ('source_name', 'source_type', 'reliability_score', 'created_at')
    list_filter = ('source_type',)
    search_fields = ('source_name', 'source_url')
    ordering = ('source_name',)
    
    fieldsets = (
        ('Informations de la source', {
            'fields': ('source_name', 'source_type')
        }),
        ('Accès', {
            'fields': ('source_url',)
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at', 'reliability_score')
    
    def reliability_score(self, obj):
        return obj.reliability_score
    reliability_score.short_description = 'Score de fiabilité'


#AdminDataFile
@admin.register(DataFile)
class DataFileAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'source', 'upload_date', 'user', 'file_age_days')
    list_filter = ('upload_date', 'source')
    search_fields = ('file_name', 'user__username')
    date_hierarchy = 'upload_date'
    ordering = ('-upload_date',)
    
    fieldsets = (
        ('Fichier', {
            'fields': ('file_name',)
        }),
        ('Source et utilisateur', {
            'fields': ('source', 'user')
        }),
        ('Métadonnées', {
            'fields': ('upload_date',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('upload_date', 'file_age_days')
    
    def file_age_days(self, obj):
        return f"{obj.file_age_days} jours"
    file_age_days.short_description = 'Âge du fichier'


#AdminPandemicData
@admin.register(PandemicData)
class PandemicDataAdmin(admin.ModelAdmin):
    list_display = (
        'pandemic', 
        'location', 
        'observation_date', 
        'total_cases', 
        'new_cases',
        'total_deaths',
        'new_deaths'
    )
    list_filter = ('pandemic', 'observation_date', 'location__who_region')
    search_fields = ('location__country', 'location__province_state', 'pandemic__pandemic_name')
    date_hierarchy = 'observation_date'
    ordering = ('-observation_date', 'location__country')
    
    fieldsets = (
        ('Référence', {
            'fields': ('pandemic', 'location', 'file', 'observation_date')
        }),
        ('Données cumulées', {
            'fields': ('total_cases', 'total_deaths', 'total_recovered')
        }),
        ('Données quotidiennes', {
            'fields': ('new_cases', 'new_deaths')
        }),
        ('Cas actifs', {
            'fields': ('active_cases',),
            'classes': ('collapse',)
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
    
    #On limmite le nbr d'info sur une même page
    list_per_page = 50


#on personnalise le site admin (au cas ou on montre le panel admin par la suite)
admin.site.site_header = "Administration MSP"
admin.site.site_title = "MSP Admin"
admin.site.index_title = "Gestion des données pandémiques"
