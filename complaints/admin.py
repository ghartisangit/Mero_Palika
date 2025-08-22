from django.contrib import admin
from .models import Municipality, Category, Complaint, Status, Ward, Comment, Like
from .forms import ComplaintAdminForm


@admin.register(Municipality)
class MunicipalityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display = ['id', 'ward_number', 'municipality_name']
    list_filter = ['municipality']
    search_fields = ['municipality__name', 'ward_number']

    def municipality_name(self, obj):
        return obj.municipality.name
    municipality_name.short_description = 'Municipality'

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    form = ComplaintAdminForm
    list_display = [
        'id', 'title', 'municipality', 'ward', 'status', 'user', 'is_hidden',
        'like_count', 'comment_count'  # removed report_count
    ]
    list_filter = ['municipality', 'status', 'is_hidden']
    search_fields = ['title', 'description', 'user__email', 'user__username']
    readonly_fields = ('like_count', 'comment_count')  # removed report_count

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'user', 'municipality', 'ward', 'category', 'status', 'is_hidden')
        }),
        ('Counts', {
            'fields': ('like_count', 'comment_count'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'complaint', 'short_content', 'created_at']
    readonly_fields = ['created_at']
    search_fields = ['user__email', 'complaint__title', 'content']

    def short_content(self, obj):
        return (obj.content[:50] + '...') if len(obj.content) > 50 else obj.content
    short_content.short_description = 'Content'


admin.site.register(Category)
admin.site.register(Status)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'complaint']
    search_fields = ['user__email', 'complaint__title']
