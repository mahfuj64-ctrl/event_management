from django import forms
from .models import Event, Participant, Category

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location', 'category']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'border rounded p-2 w-full'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'border rounded p-2 w-full'}),
            'name': forms.TextInput(attrs={'class': 'border rounded p-2 w-full'}),
            'location': forms.TextInput(attrs={'class': 'border rounded p-2 w-full'}),
            'description': forms.Textarea(attrs={'class': 'border rounded p-2 w-full'}),
            'category': forms.Select(attrs={'class': 'border rounded p-2 w-full'}),
        }

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = '__all__'
        widgets = {
            'events': forms.CheckboxSelectMultiple() 
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'