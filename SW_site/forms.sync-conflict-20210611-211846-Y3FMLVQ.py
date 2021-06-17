from django import forms

class registerToAdventureForm(forms.Form):
    adventure = forms.TextField(help_text="adventure name")
