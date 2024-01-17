from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from wall.models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Posts"""
    list_display = ("user", "published", "create_date", "moderation", "view_count", "id")


@admin.register(Comment)
class CommentAdmin(MPTTModelAdmin, admin.ModelAdmin):
    """ Comments to posts """
    list_display = ("user", "post", "created_date", "update_date", "published", "id")
    # actions = ['unpublish', 'publish']
    mptt_level_indent = 15
