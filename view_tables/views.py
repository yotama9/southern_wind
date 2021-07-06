from django.shortcuts import render, get_object_or_404
from view_tables.models import Adventure, Registrant, Evening
from view_tables.models import get_tables_for_evening, get_available_tables
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
import datetime
from datetime import timedelta

from view_tables.forms import registerToAdventureForm, CreateTableForm, CreateEveningForm


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
    except Adventure.DoesNotExist:
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
        print(adventures)

        context = {'form':form,'adventure_list':adventures}

        return render(request,'view_tables/register_to_table.html',context=context)



def create_evening(request):
    """View to create a table, this is supposed to be really simple"""
    if request.method == "POST":
        #store the date as a new evening
        form = CreateEveningForm(request.POST)

        if form.is_valid():
            #check that the date is valid
            date = form.cleaned_data['date']
            evening = Evening(date=date)
            evening.save()
            return HttpResponseRedirect(reverse('adventures'))
        else: #invlaid form
            context = {
                'form': form
                }
            return render(request,'view_tables/create_evening.html',context=context)
    else:
        #this is a new attempt to make an evening
        
        form = CreateEveningForm()
        context = {
            'form':form
            }
        return render(request,'view_tables/create_evening.html',context=context)
        
        
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
            evening = form.cleaned_data['evening']

            adventure = Adventure(title=title,
                                  dm_name=dm_name,
                                  teaser=teaser,
                                  is_dnd5=is_dnd5,
                                  min_level=min_level,
                                  max_level=max_level,
                                  max_number_of_players=max_number_of_players,
                                  evening=evening)
            adventure.save()

            return HttpResponseRedirect(reverse('show-evenings'))
        
        else: #the form is not validated. 
            context = {
                'form': form
                }
            return render(request,'view_tables/create_adventure.html',context=context)

    else:
        #this is a GET(or any other request), create an empty form

        #check that the date is valid
        
        form = CreateTableForm(initial={'date':'22/07/test'})
        context = {
            'form':form
            }
        return render(request,'view_tables/create_adventure.html',context=context)
        
        
@permission_required('view_tables.view_evening')
def show_evenings(request):
    #show all available_events
    evenings = Evening.objects.all()
    today = datetime.date.today()
    next_evening = []
    future_evenings = []
    past_evenings = []
    low_delta = -1
    
    for e in evenings:
        delta = (e.date - today).days
        if delta < 0:
            #this is a past event
            past_evenings.append(e)
        elif low_delta == -1:
            #this is the first event that is not in the past, consider this as the upcoming event
            next_evening = [e]
            low_delta = e
        elif low_delta > delta:
            #this event is closer than a stored upcoming event, replace
            future_evenings.append(next_evening[0])
            next_evening = [e]
        else:
            #this is a future event
            future_evenings.append(e)
            

    context = {
        "future": future_evenings,
        "past": past_evenings,
        "upcoming": next_evening,
    }

    return render(request,'view_tables/show_evenings.html',context=context)
    
                                                
@permission_required('view_tables.view_evening')
def show_evenings_details(request,pk):
    try:
        evening = Evening.objects.get(pk=pk)
    except Evening.DoesNotExist:
        raise Http404('Evening does not exist')

    
    context = {
        'date':evening.date,
        'tables':get_tables_for_evening(evening),
    }


    return render(request, 'view_tables/show_evening_details.html',context=context)
