from django.db import models
from django.urls import reverse
import datetime



class Adventure(models.Model):
    title = models.CharField(max_length=200,help_text='Please enter the adventure\'s title')
    dm_name = models.CharField(max_length=200,help_text='Please enter your name or a display name')
    teaser = models.TextField(max_length=2000,help_text='Please enter the teaser for the adventure')
    is_dnd5 = models.BooleanField(help_text='Is this a D&D5 adventure?')
    min_level = models.IntegerField(help_text='What is the minimum character level for this adventure?')
    max_level = models.IntegerField(help_text='What is the maximum character level for this adventure?')
    max_number_of_players = models.IntegerField(help_text='Total numbers of players you are willing to host')    
    date = models.DateField()

    def __str__(self):
        """String for representing the Model object"""
        return f'{self.title} ({self.dm_name})'

    class Meta:
        ordering = ['title']

    def get_absolute_url(self):
        """Return the url to access a detail record for this book"""
        return reverse('adventure-detail', args=[str(self.id)])

    


                            

class Registrant(models.Model):
    name = models.CharField(max_length=200,help_text='Please enter the name so we can know you')
    adventure = models.ForeignKey(Adventure,help_text='Which adventure do you want to play?',on_delete=models.SET_NULL,null=True)
    

    
    def get_adventure(self):
        return f'{self.adventure.title} ({self.adventure.dm_name})'
    def get_adventure_url(self):
        return f'{self.adventure.get_absolute_url()}'


    class Meta:
        ordering = ['name']






def get_available_tables():
    registrants = Registrant.objects.all()
    counter = {}
    for r in registrants:
        if not r.adventure.pk in counter:
            counter[r.adventure.pk] = 0
        counter[r.adventure.pk] += 1

    adventures_all = [a for a in Adventure.objects.filter(date__gte=datetime.date.today())]
    adventures = [a for a in adventures_all if (a.pk not in counter or a.max_number_of_players > counter[a.pk])]
    return adventures
