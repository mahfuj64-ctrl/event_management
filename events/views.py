from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, Participant, Category
from .forms import EventForm, ParticipantForm, CategoryForm
from django.db.models import Q, Count
from django.utils import timezone
from django.contrib import messages

# =================================
# Dashboard View (Timezone Fixed)
# =================================
def organizer_dashboard(request):
    filter_type = request.GET.get('type', 'today')

    today = timezone.localdate()

    counts = Event.objects.aggregate(
        total_events=Count('id'),
        upcoming_events=Count('id', filter=Q(date__gte=today)),
        past_events=Count('id', filter=Q(date__lt=today))
    )
    counts['total_participants'] = Participant.objects.count()
    base_query = Event.objects.select_related('category').annotate(participant_count=Count('participants__id', distinct=True))
    

    if filter_type == 'upcoming':
        events = base_query.filter(date__gte=today)
    elif filter_type == 'past':
        events = base_query.filter(date__lt=today)
    elif filter_type == 'total':
        events = base_query.all()
    else: 
        events = base_query.filter(date=today)
    
    context = {
        'events': events,
        'counts': counts,
        'current_filter': filter_type,
    }

    if request.headers.get('HX-Request'):
        return render(request, 'dashboard/partials/filtered_events_section.html', context)

    return render(request, "dashboard/dashboard.html", context)

# =================================
# Event CRUD Views
# =================================
def event_list(request):
    search_query = request.GET.get('q', '')
    category_filter = request.GET.get('category')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    events = Event.objects.select_related('category').prefetch_related('participants')
    
    if search_query:
        events = events.filter(Q(name__icontains=search_query) | Q(location__icontains=search_query))
    if category_filter and category_filter.isdigit():
        events = events.filter(category_id=int(category_filter))
    if start_date and end_date:
        events = events.filter(date__range=[start_date, end_date])
        
    categories = Category.objects.all()
    return render(request, 'dashboard/event_list.html', {'events': events, 'categories': categories})

def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event successfully created!')
    else:
        form = EventForm()
    return render(request, 'dashboard/event_form.html', {'form': form, 'form_title': 'Create a New Event'})

def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event successfully updated!')
            return redirect('events:event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'dashboard/event_form.html', {'form': form, 'form_title': 'Update Event'})

def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event has been deleted.')
        return redirect('events:event_list')
    return render(request, 'dashboard/event_confirm_delete.html', {'event': event})

# =================================
# Participant CRUD Views
# =================================
def participant_list(request):
    participants = Participant.objects.prefetch_related('events').all()
    return render(request, 'dashboard/participant_list.html', {'participants': participants})

def participant_create(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Participant successfully registered!')
    else:
        form = ParticipantForm()
    return render(request, 'dashboard/participant_form.html', {'form': form})

def participant_update(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == 'POST':
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            messages.success(request, 'Participant details updated.')
            return redirect('events:participant_list')
    else:
        form = ParticipantForm(instance=participant)
    return render(request, 'dashboard/participant_form.html', {'form': form})

def participant_delete(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == 'POST':
        participant.delete()
        messages.success(request, 'Participant has been removed.')
        return redirect('events:participant_list')
    return render(request, 'dashboard/participant_confirm_delete.html', {'participant': participant})

# =================================
# Category CRUD Views
# =================================
def category_list(request):
    categories = Category.objects.annotate(event_count=Count('events')).all()
    return render(request, 'dashboard/category_list.html', {'categories': categories})

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully.')
            return redirect('events:category_list')
    else:
        form = CategoryForm()
    return render(request, 'dashboard/category_form.html', {'form': form})

def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully.')
            return redirect('events:category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'dashboard/category_form.html', {'form': form})

def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted.')
        return redirect('events:category_list')
    return render(request, 'dashboard/category_confirm_delete.html', {'category': category})