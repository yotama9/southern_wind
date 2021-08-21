from django import forms

from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from bootstrap_datepicker_plus import DatePickerInput
from view_tables.models import Adventure,Registrant,Evening
from view_tables.models import get_available_tables, get_available_evenings

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
        has_c = self.cleaned_data['I_already_have_a_character']
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


        

class CreateTableForm(forms.Form):
    title = forms.CharField(help_text="What is your adventure's title?")
    dm_name = forms.CharField(help_text="What is your DM's display name?")
    teaser = forms.CharField(help_text="Please write here a short teaser/description of your adventure",widget=forms.Textarea())
    is_dnd5 = forms.BooleanField(help_text="Is this a D&D5 adventure?", required=False)
    min_level = forms.IntegerField(required=False)
    max_level = forms.IntegerField(required=False)
    limit_number_of_players = forms.BooleanField(help_text='Do you wish to have a limit to the number of players?', required=False)
    max_number_of_players = forms.IntegerField(required=False)
    evening = forms.ChoiceField(help_text="Please select the evening for the adventure.", choices = [])

    limit_number_of_players.widget.attrs.update({'id':'limit_number_of_players',
                                                 'onclick':'toggle_number_of_players_field()'})

    max_number_of_players.widget.attrs.update({'id':'max_number_of_players'})
    min_level.widget.attrs.update({'id':'min_level'})
    max_level.widget.attrs.update({'id':'max_level'})
    is_dnd5.widget.attrs.update({'id':'is_dnd5'})



    def __init__(self, *args, **kwargs):
        super(CreateTableForm,self).__init__(*args,**kwargs)
        choices = get_available_evenings()
        choices = [(-1,'select evenings')] + [(a.pk,a.date) for a in choices]
        self.fields['evening'].choices = choices



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



        
        
            
