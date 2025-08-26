# admin.py
from django.contrib import admin
from .models import Notice, Training, TrainingRegistration, Vacancy, VacancyRegistration, Information, TrainingStatus

# --- Admin for Status Models ---
@admin.register(TrainingStatus)
class TrainingStatusAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# --- Admin for Notice ---
@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'ward', 'created_at')
    search_fields = ('title', 'description', 'user__email')
    list_filter = ('ward', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('user', 'title', 'description', 'ward')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


# --- Admin for Training ---
@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'ward', 'training_status', 'created_at')
    search_fields = ('title', 'description', 'user__email')
    list_filter = ('ward', 'training_status', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('user', 'title', 'description', 'ward', 'training_status', 'image')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


# --- Admin for TrainingRegistration ---
@admin.register(TrainingRegistration)
class TrainingRegistrationAdmin(admin.ModelAdmin):
    list_display = ('training', 'user', 'registered_at')
    search_fields = ('training__title', 'user__email')
    list_filter = ['registered_at']
    readonly_fields = ('registered_at',)


# --- Admin for Vacancy ---
@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'ward', 'vacancy_status', 'created_at')
    search_fields = ('title', 'description', 'user__email')
    list_filter = ( 'ward', 'vacancy_status', 'created_at')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('user', 'title', 'description', 'ward', 'vacancy_status', 'image')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


# --- Admin for VacancyRegistration ---
@admin.register(VacancyRegistration)
class VacancyRegistrationAdmin(admin.ModelAdmin):
    list_display = ('Vacancy', 'user', 'registered_at')
    search_fields = ('Vacancy__title', 'user__email')
    list_filter = ['registered_at']
    readonly_fields = ('registered_at',)


# --- Admin for Information ---
@admin.register(Information)
class InformationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'ward')
    search_fields = ('title', 'description', 'user__email')
    list_filter = ['ward']
