from django.db import models
from django.urls import reverse
import datetime



    

class Adventure(models.Model):
    title = models.CharField(max_length=200,help_text='Please enter the adventure\'s title')
    dm_name = models.CharField(max_length=200,help_text='Please enter your name or a display name')
    teaser = models.TextField(max_length=2000,help_text='Please enter the teaser for the adventure')
    is_dnd5 = models.BooleanField(help_text='Is this a D&D5 adventure?')
    min_level = models.IntegerField(help_text='What is the minimum character level for this adventure?',null=True,blank=True)
    max_level = models.IntegerField(help_text='What is the maximum character level for this adventure?',null=True,blank=True)
    limit_number_of_players = models.BooleanField(help_text="Do you wish to limit the number of players?",default=False)
    max_number_of_players = models.IntegerField(help_text='Total numbers of players you are willing to host',null=True,blank=True)    
    evening = models.ForeignKey("Evening",help_text="what is the relevant evening?",on_delete=models.SET_NULL,null=True)

    def __str__(self):
        """String for representing the Model object"""
        return f'{self.title} ({self.dm_name})'

    class Meta:
        ordering = ['title']

    def get_absolute_url(self):
        """Return the url to access a detail record for this book"""
        return reverse('adventure-detail', args=[str(self.id)])


    

class Evening(models.Model):
    date = models.DateField(help_text="When will the evening take place?")
    
    def get_absolute_url(self):
        """Return the url to access adventures in an evening"""
        return reverse('evening-detail', args=[str(self.id)])

    def __str__(self):
        """String representation of the evening (the date)"""
        day = self.date.day
        month = self.date.month
        year = self.date.year
        date = '{}/{}/{}'.format(day,month,year)
        return date



class SimpleRegistrant(models.Model):
    name = models.CharField(max_length=20,help_text='Please enter your name. It doesn\'t have to be your real name, but try and remember it when you arrive in the evening')

    evening = models.ForeignKey("Evening",on_delete=models.SET_NULL,null=True)
    arrived = models.BooleanField("Present",null=True)

    willing_for_non_dnd = models.BooleanField('Are you interested in methods other than D&D?', null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f'{self.name} ({self.evening})'



class Registrant(models.Model):
    name = models.CharField(max_length=200,help_text='Please enter the name so we can know you')
    adventure = models.ForeignKey(Adventure,help_text='Which adventure do you want to play?',on_delete=models.SET_NULL,null=True)
    has_character = models.BooleanField(help_text="Do you have a character relevant (level and gaming system) for this table?",null=True)
    character_level = models.IntegerField(help_text="What is your character level?", null=True,blank=True)
    character_name = models.CharField(max_length=200,help_text="Please write your character's name",null=True,blank=True)
    
    
    def get_adventure(self):
        return f'{self.adventure.title} ({self.adventure.dm_name})'
    def get_adventure_url(self):
        return f'{self.adventure.get_absolute_url()}'


    class Meta:
        ordering = ['name']

def get_available_tables(include_full=False):
    #getting relevant evening
    evenings = Evening.objects.filter(date__gte=datetime.date.today())
    
    out = {}
    for e in evenings:
        for a in Adventure.objects.filter(evening=e):

            n_registrants = Registrant.objects.filter(adventure=a).count()
            if a.max_number_of_players == None or (include_full or n_registrants < a.max_number_of_players):
                out[a] = {'evening':e,'n_registrants':n_registrants}
    return out





def get_tables_for_evening(evening):
    tables = Adventure.objects.filter(evening=evening)
    out = {}
    for table in tables:
        out[table] = Registrant.objects.filter(adventure=table)
    return out




def get_available_evenings():
    out = Evening.objects.filter(date__gte=datetime.date.today())
    return out
    
