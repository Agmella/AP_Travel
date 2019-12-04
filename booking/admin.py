from django.contrib import admin
from .models import User, Review, Flight, Train

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']


admin.site.register(Flight)
admin.site.register(Train)
admin.site.register(Review)
