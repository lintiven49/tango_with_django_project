from django.contrib import admin

from rango.models import Category, Page, UserProfile
# Register your models here.


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')


class PageInline(admin.TabularInline):
    model = Page
    extra = 2


class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        ('Views and likes', {'fields': ['views', 'likes']}),
    ]
    inlines = [PageInline]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)
