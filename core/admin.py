from django.contrib import admin
from django.utils.html import format_html
from .models import SiteSettings, Education, Skill, Project, Referee, ContactMessage


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Branding", {"fields": ("brand_name", "full_name", "title", "profile_photo")}),
        ("Profile", {"fields": ("intro", "summary", "focus", "location")}),
        ("Contact & Social", {"fields": ("email", "github_url", "youtube_url", "whatsapp_url")}),
        ("Sections", {"fields": ("show_referees",)}),
        ("SEO", {"fields": ("meta_title", "meta_description")}),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("title", "institution", "period", "order", "published")
    list_editable = ("order", "published")
    search_fields = ("title", "institution")


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "icon", "level", "order", "published")
    list_editable = ("order", "published")
    search_fields = ("name",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("preview", "title", "category", "featured", "published", "order", "created_at")
    list_editable = ("featured", "published", "order")
    list_filter = ("published", "featured", "category")
    search_fields = ("title", "tech_stack")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at",)

    @admin.display(description="Image")
    def preview(self, obj):
        return format_html('<img src="{}" style="height:36px">', obj.thumbnail.url) if obj.thumbnail else "—"


@admin.register(Referee)
class RefereeAdmin(admin.ModelAdmin):
    list_display = ("full_name", "organization", "order", "published")
    list_editable = ("order", "published")
    search_fields = ("full_name", "organization")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "name", "email", "created_at", "is_read")
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("name", "email", "subject", "message", "created_at")

    def has_add_permission(self, request):
        return False
