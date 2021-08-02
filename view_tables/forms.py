from django import forms

from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from bootstrap_datepicker_plus import DatePickerInput
from view_tables.models import Adventure,Registrant,get_available_tables,Evening

import datetime


class registerToAdventureForm(forms.Form):
    player = forms.CharField(help_text="What is your name?")
    adventure = forms.ChoiceField(help_text="Which adventure do you want to play?", choices= [])
    I_already_have_a_character = forms.BooleanField(required=False)
    character_level = forms.IntegerField(required=False)

    def __init__(self, *args, **kwargs):
        super(registerToAdventureForm,self).__init__(*args,**kwargs)
        choices = get_available_tables()
        choices = [(-1,'select adventure')] + [(a.pk,a.title) for a in choices]
        self.fields['adventure'].choices = choices

    def clean(self):
        p_name = self.cleaned_data['player']

        #check if player name is not empty
        if p_name.strip() == '':
            raise ValidationError(_('Plesae provide a player name'))

        adventure_ = self.cleaned_data['adventure']
        if adventure_ == '-1':
            raise ValidationError(_('Please select the adventure you wish to join'))

        #check if the player has a character and if there is a level
        print (self.cleaned_data)
        has_c = self.cleaned_data['has_character']
        char_level = self.cleaned_data['character_level']
        if has_c:
            if char_level == None:
                raise ValidationError(_('Please state your character level'))
            if char_level < 1 or char_level > 20:
                raise ValidationError(_('Please add a valid character level'))



class CreateEveningForm(ModelForm):
    class Meta:
        model = Evening
        fields =['date',]
        widgets = {
            'date':DatePickerInput(
                options={
                    'format':"MM/DD/YYYY",
                    },
                attrs={'onclick':'test()'},
                )
            }

    def clean(self):
        _date = self.cleaned_data['date']
        today = datetime.date.today()

        if _date < datetime.date.today():
            raise ValidationError(_('Please use date in the future'))
        
class CreateTableForm(ModelForm):
    class Meta:
        model = Adventure
        fields = ['title',
                  'dm_name',
                  'teaser',
                  'is_dnd5',
                  'min_level',
                  'max_level',
                  'limit_number_of_players',
                  'max_number_of_players',
                  'evening',]
        widgets = {
            'limit_number_of_players':forms.CheckboxInput(
                attrs={'id':'limit_number_of_players',
                       'onclick':'toggle_number_of_players_field()',
                       }
                ),
            'is_dnd5':forms.CheckboxInput(
                attrs={'id':'is_dnd5',}
                ),
            'max_number_of_players':forms.NumberInput(
                attrs={'id':'max_number_of_players',}
                ),
            'min_level':forms.NumberInput(
                attrs={'id':'min_level',}
                ),
            'max_level':forms.NumberInput(
                attrs={'id':'max_level',}
                ),

            }





    def clean(self):
        print('clean')
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



        
        
            
