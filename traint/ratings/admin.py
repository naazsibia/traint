from django.contrib import admin
from .models import Rating, Dress, Cluster

# Register your models here.
@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    pass
@admin.register(Dress)
class DressAdmin(admin.ModelAdmin):
    pass
@admin.register(Cluster)
class ClusterAdmin(admin.ModelAdmin):
    model = Cluster
    list_display = ['name', 'get_members']
    
#admin.site.register(Rating, RatingAdmin)
#admin.site.register(Dress, DressAdmin)