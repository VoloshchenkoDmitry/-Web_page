from django.contrib import admin
from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'created_at', 'views_count')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('views_count', 'created_at')

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'content', 'preview')
        }),
        ('Публикация', {
            'fields': ('is_published',),
            'classes': ('collapse',)
        }),
        ('Статистика', {
            'fields': ('views_count', 'created_at'),
            'classes': ('collapse',)
        })
    )