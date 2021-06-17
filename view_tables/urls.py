from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('adventures',views.AdventureListView.as_view(),name='adventures'),
    path('adventure/<int:pk>', views.adventureDetailView.as_view(),name='adventure-detail'),
    path('registrants',views.RegistrantListView.as_view(),name='registrants'),
    path('register_to_table/',views.register_to_table, name='register-to-table'),
    path('create_adventure/',views.create_adventure, name='create-adventure'),
    ]


