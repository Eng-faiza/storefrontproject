from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.contenttypes.admin import GenericTabularInline
from store.admin import ProductAdmin
from tags.models import TaggedItem
from store.models  import Product
from .models import User
from store.admin import ProductImageInline


@admin.register(User)
class UserAdmin(BaseUserAdmin):
      add_fieldsets = (
            (
                None,
                {
                    "classes": ("wide",),
                    "fields": ("username", "usable_password", "password1", "password2","email","first_name","last_name"),
                },
            ),
        )

# Register your models here.
class TagInLine(GenericTabularInline):
    autocomplete_fields=['tag']
    model = TaggedItem 

class CustomProductAdmin(ProductAdmin):
    inlines=[TagInLine, ProductImageInline]

admin.site.unregister(Product)
admin.site.register(Product,CustomProductAdmin)