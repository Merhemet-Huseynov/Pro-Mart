from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
<<<<<<< HEAD
from django.utils.translation import gettext_lazy as _
from users.models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("email", "phone_number", "user_type", "is_active", "is_staff")
    list_filter = ("user_type", "is_staff", "is_superuser", "is_active")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("phone_number",)}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
        (_("User Type"), {"fields": ("user_type",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "user_type", "phone_number"),
        }),
    )

    search_fields = ("email", "phone_number")
    ordering = ("email",)
=======
from django.utils.html import mark_safe
from django.contrib.auth.models import User
from django.http import HttpRequest

from ..forms import CustomUserCreationForm, CustomUserChangeForm
from ..models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Admin configuration for managing the CustomUser model in the Django admin panel.
    """

    model = CustomUser
    list_display = [
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
        "profile_picture_preview",
    ]
    list_filter = [
        "is_active", 
        "is_staff"
    ]
    search_fields = [
        "email", 
        "first_name", 
        "last_name"
    ]
    ordering = [
        "email"
    ]

    fieldsets = (
        (None, {"fields": (
            "email", 
            "password"
        )}),
        ("Personal info", {"fields": (
            "first_name", 
            "last_name", 
            "bio", 
            "profile_picture", 
        )}),
        ("Permissions", {"fields": (
            "is_active", 
            "is_staff", 
            "is_superuser", 
            "groups", 
            "user_permissions"
        )}),
        ("Important dates", {"fields": (
            "last_login", 
            "date_joined"
        )}),
    )

    add_fieldsets = (
        (None, {"fields": (
            "email", 
            "password1", 
            "password2"
        )}),
        ("Personal info", {"fields": (
            "first_name", 
            "last_name", 
            "bio", 
            "profile_picture", 
        )}),
        ("Permissions", {"fields": (
            "is_active", 
            "is_staff", 
            "is_superuser"
        )}),
    )

    filter_horizontal = ("groups", "user_permissions")

    def profile_picture_preview(self, obj: CustomUser) -> str:
        """
        Displays a small preview of the profile picture in the admin panel.

        Args:
            obj (CustomUser): The CustomUser instance.

        Returns:
            str: HTML string for displaying the profile picture or "No Image" 
            if not available.
        """
        if obj.profile_picture:
            try:
                return mark_safe(
                    f'<img src="{obj.profile_picture.url}" width="50" height="50" />'
                )
            except Exception as e:
                return "No Image"
        return "No Image"

    profile_picture_preview.short_description = "Profile Picture"
>>>>>>> 0fcf8c5f75a945c84a88977ec1336a8f80e94c41
