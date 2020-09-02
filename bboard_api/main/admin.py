from django.contrib import admin

from .models import AdditionalImage, Bulletin


class AdditionalImageInLine(admin.TabularInline):
    model = AdditionalImage


class BulletinsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'price', 'date')
    list_display_links = ('name', )
    fields = ('name', 'price', 'date', 'description', 'main_photo')
    inlines = (AdditionalImageInLine, )


class AdditionalImageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'bulletin')
    list_display_links = ('bulletin', )
    fields = ('bulletin', 'image')


admin.site.register(Bulletin, BulletinsAdmin)
admin.site.register(AdditionalImage, AdditionalImageAdmin)
