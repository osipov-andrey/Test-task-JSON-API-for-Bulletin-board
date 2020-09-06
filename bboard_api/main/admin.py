from django.contrib import admin

from .models import AdditionalImage, Bulletin


class AdditionalImageInLine(admin.TabularInline):
    model = AdditionalImage


class BulletinsAdmin(admin.ModelAdmin):
    model = Bulletin
    inlines = (AdditionalImageInLine, )


class AdditionalImageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'bulletin')
    list_display_links = ('bulletin', )
    fields = ('bulletin', 'image')


admin.site.register(Bulletin, BulletinsAdmin)
admin.site.register(AdditionalImage, AdditionalImageAdmin)
