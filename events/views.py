from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, Participant, Category
from .forms import EventForm
from django.db.models import Q
from datetime import date
from .forms import ParticipantForm, CategoryForm

# Home/List View
def event_list(request):
    search_query = request.GET.get('q', '')
    category_filter = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    events = Event.objects.select_related('category').prefetch_related('participant_set')

    if search_query:
        events = events.filter(Q(name__icontains=search_query) | Q(location__icontains=search_query))

    if category_filter and category_filter.isdigit():
        events = events.filter(category_id=int(category_filter))

    if start_date and end_date:
        events = events.filter(date__range=[start_date, end_date])

    categories = Category.objects.all()

    return render(request, 'dashboard/event_list.html', {
        'events': events,
        'categories': categories,
        'search_query': search_query,
        'category_filter': category_filter,
        'start_date': start_date,
        'end_date': end_date,
    })


# CRUD Views
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('events:event_list')  # namespace সহ
        else:
            print(form.errors)  # Debugging জন্য
    else:
        form = EventForm()
    return render(request, 'dashboard/event_form.html', {'form': form})

def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('events:event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'dashboard/event_form.html', {'form': form})


def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('events:event_list')
    return render(request, 'dashboard/event_confirm_delete.html', {'event': event})

# Dashboard View
def dashboard(request):
    today = date.today()
    total_participants = Participant.objects.count()
    total_events = Event.objects.count()
    upcoming_events = Event.objects.filter(date__gt=today)
    past_events = Event.objects.filter(date__lt=today)
    todays_events = Event.objects.filter(date=today)
    todays_events = Event.objects.filter(date=today).prefetch_related('participant_set')

    context = {
        'total_participants': total_participants,
        'total_events': total_events,
        'upcoming_count': upcoming_events.count(),
        'past_count': past_events.count(),
        'todays_events': todays_events,
    }
    return render(request, 'dashboard/dashboard.html', context)


# Participant CRUD
def participant_list(request):
    participants = Participant.objects.prefetch_related('events').all()
    return render(request, 'dashboard/participant_list.html', {'participants': participants})

def participant_create(request):
    form = ParticipantForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('events:participant_list')
    return render(request, 'dashboard/participant_form.html', {'form': form})

def participant_update(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    form = ParticipantForm(request.POST or None, instance=participant)
    if form.is_valid():
        form.save()
        return redirect('events:participant_list')
    return render(request, 'dashboard/participant_form.html', {'form': form})

def participant_delete(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    participant.delete()
    return redirect('events:participant_list')

# Category CRUD
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'dashboard/category_list.html', {'categories': categories})

def category_create(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('events:category_list')
    return render(request, 'dashboard/category_form.html', {'form': form})

def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        return redirect('events:category_list')
    return render(request, 'dashboard/category_form.html', {'form': form})

def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('events:category_list')


