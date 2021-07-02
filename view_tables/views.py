from django.shortcuts import render, get_object_or_404
from view_tables.models import Adventure, Registrant, get_available_tables
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
import datetime

from view_tables.forms import registerToAdventureForm, CreateTableForm


def index(request):
    """View function for home page of site """
    #Count stuff
    num_adventures = Adventure.objects.all().count()
    num_registrants = Registrant.objects.all().count()

    context = {
        'num_adventures':num_adventures,
        'num_registrants':num_registrants,
    }

    #render the HTML template index.html
    return render (request, 'index.html', context=context)


class AdventureListView(generic.ListView):
    model = Adventure

class adventureDetailView(generic.DetailView):
    model = Adventure

def adventure_detail_view(request,primary_key):
    try:
        adventure = Adventure.objects.get(pk=primary_key)
    except Book.DoesNotExist:
        raise Http404('Adventure does not exist')

class RegistrantListView(generic.ListView):
    model = Registrant
    


def register_to_table(request):
    #if this is a POST request ten process the form data
    if request.method == 'POST':
        # a form instance and populate it with data from the request (binding):
        form = registerToAdventureForm(request.POST)
        #check if the form is valid:
        if form.is_valid():
            #process the data in form.cleaned_data as required
            adventure_id = form.cleaned_data['adventure']
            adventure = Adventure.objects.filter(pk=adventure_id)[0]
            reg = Registrant(name=form.cleaned_data['player'],adventure=adventure)
            reg.save()

            #redirect to an new URL:
            return HttpResponseRedirect(reverse('adventures'))
        else:
            context = {
                'form': form
                }
            return render(request,'view_tables/register_to_table.html',context=context) 

        #if this is a GET (or any other method) create the default form
    else:
        form = registerToAdventureForm()

        adventures = get_available_tables()

        context = {'form':form,'adventure_list':adventures}

        return render(request,'view_tables/register_to_table.html',context=context)


                   

@permission_required('view_tables.add_adventure')
def create_adventure(request):
    """View fucntion for creating a table"""

    #if this is a POST request, create a table
    if request.method == "POST":

        #create a form instance and populate it with data.
        form = CreateTableForm(request.POST)

        #check if the form is valid:
        if form.is_valid():
            #process the data in the form.cleaned_data and store the new advanture
            fields = ['title',
                  'dm_name',
                  'teaser',
                  'is_dnd5',
                  'min_level',
                  'max_level',
                  'max_number_of_players',
                  'date',]
                    
            title = form.cleaned_data['title']
            dm_name = form.cleaned_data['dm_name']
            teaser = form.cleaned_data['teaser']
            is_dnd5 = form.cleaned_data['is_dnd5']
            min_level = form.cleaned_data['min_level']
            max_level = form.cleaned_data['max_level']
            max_number_of_players = form.cleaned_data['max_number_of_players']
            date = form.cleaned_data['date']

            adventure = Adventure(title=title,
                                  dm_name=dm_name,
                                  teaser=teaser,
                                  is_dnd5=is_dnd5,
                                  min_level=min_level,
                                  max_level=max_level,
                                  max_number_of_players=max_number_of_players,
                                  date=date)
            adventure.save()

            return HttpResponseRedirect(reverse('adventures'))
        
        else: #the form is not validated. 
            context = {
                'form': form
                }
            return render(request,'view_tables/create_adventure.html',context=context)

    else:
        #this is a GET(or any other request), create an empty form
        context = {
            'form':CreateTableForm(),
            }
        return render(request,'view_tables/create_adventure.html',context=context)
        
        
            

            
