from django.contrib import admin

from .models import User, Category, Listing, Bid, Comment

# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    filter_horizontal = ('watchers',)
    
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid)
admin.site.register(Comment)
