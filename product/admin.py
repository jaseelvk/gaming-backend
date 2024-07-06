from django.contrib import admin
from .models import Product, Feature, PlatformImages, UserProfile, Wishlist

class FeatureInline(admin.TabularInline):
    model = Feature
    extra = 1

class PlatformImagesInline(admin.TabularInline):
    model = PlatformImages
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [FeatureInline, PlatformImagesInline]
    list_display = ('id', 'product_name', 'created_by')
    ordering = ('id', 'product_name')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    ordering = ('user',)

class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'product')
    ordering = ('user',)

admin.site.register(Product, ProductAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Wishlist, WishlistAdmin)  # Register the Wishlist model
