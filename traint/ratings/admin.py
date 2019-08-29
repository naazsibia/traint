from django.contrib import admin
from .models import Rating, Dress

# Register your models here.
@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    pass
@admin.register(Dress)
class DressAdmin(admin.ModelAdmin):
    pass

#admin.site.register(Rating, RatingAdmin)
#admin.site.register(Dress, DressAdmin)