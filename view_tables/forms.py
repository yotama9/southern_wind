from django import forms

from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from bootstrap_datepicker_plus import DatePickerInput
from view_tables.models import Adventure,Registrant,get_available_tables

import datetime


class registerToAdventureForm(forms.Form):
    player = forms.CharField(help_text="What is your name?")
    #getting all adventures




    
    #adventure = forms.ChoiceField(help_text="Which adventure do you want to play?",choices =choices)
    adventure = forms.ChoiceField(help_text="Which adventure do you want to play?", choices= [])

    def __init__(self, *args, **kwargs):
        super(registerToAdventureForm,self).__init__(*args,**kwargs)
        choices = get_available_tables()
        choices = ((a.pk,a.title) for a in choices)
        self.fields['adventure'].choices = choices

    def clean_player(self):
        data = self.cleaned_data['player']

        #check if player name is not empty
        if data.strip() == '':
            raise ValidationError(_('Plesae provide a player name'))

        return data


    
class CreateTableForm(ModelForm):
    class Meta:
        model = Adventure
        fields = ['title',
                  'dm_name',
                  'teaser',
                  'is_dnd5',
                  'min_level',
                  'max_level',
                  'max_number_of_players',
                  'date',]

        widgets = {
            'date':DatePickerInput(
                options={
                    "format": "DD/MM/YYYY",
                },
            )
        }

    def clean(self):
        _title = self.cleaned_data['title']
        if _title.strip() == '':
            raise ValidationError(_('Please provide a title to the adventure'))
        
        _dm_name = self.cleaned_data['dm_name']
        if _dm_name.strip() == '':
            raise ValidationError(_('Please insert a DM display name'))

        _teaser = self.cleaned_data['teaser']
        if _teaser.strip() == '':
            raise ValidationError(_('Please add a teaser'))

        _is_dnd5 = self.cleaned_data['is_dnd5']
        _min_level = self.cleaned_data['min_level']
        _max_level = self.cleaned_data['max_level']
        if _is_dnd5 == True:
            if _min_level == None or _max_level == None:
                raise ValidationError(_('D&D5 tables require minimum and maximum level level'))

            if _min_level > _max_level:
                raise ValidationError(_('Minumum character level has to be equal or smaller than maximum character level'))

        _data = self.cleaned_data['date']
        if _data < datetime.date.today():
            raise ValidationError(_('Please update the date of the adventure to be in the future'))


        
        
            
