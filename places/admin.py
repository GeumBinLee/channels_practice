from django.contrib import admin

from reviews.models import Review

from .models import Place


class ReviewInline(admin.StackedInline):
    model = Review

class PlacewAdmin(admin.ModelAdmin):
    inlines = (
        ReviewInline,
    )
    
admin.site.register(Place, PlacewAdmin)
