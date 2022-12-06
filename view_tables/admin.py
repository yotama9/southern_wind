from django.contrib import admin
from .models import Adventure, Registrant,Evening,SimpleRegistrant

# Register your models here.

admin.site.register(SimpleRegistrant)

#admin.site.register(Adventure)
@admin.register(Adventure)
class AdventureAdmin(admin.ModelAdmin):
    list_display = ('title','dm_name','is_dnd5')
    fields = [('title','dm_name'),'teaser','is_dnd5', ('min_level','max_level'),('max_number_of_players','evening')]


#admin.site.register(Registrant)
@admin.register(Registrant)
class RegistrantAdmin(admin.ModelAdmin):
    list_display = ('name','get_adventure')
    list_filter = ['name']


@admin.register(Evening)
class RegisterEvening(admin.ModelAdmin):
    list_display = ['date']

