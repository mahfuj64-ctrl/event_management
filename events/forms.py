from django import forms
from .models import Event, Participant, Category


text_input_class = "mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
textarea_class = f"{text_input_class} h-24"
select_input_class = text_input_class

# ==============================================================================
#  Event Form
# ==============================================================================
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'class': text_input_class, 'placeholder': 'e.g., Annual Tech Conference'}),
            'description': forms.Textarea(attrs={'class': textarea_class, 'placeholder': 'Provide a detailed description of the event...'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': text_input_class}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': text_input_class}),
            'location': forms.TextInput(attrs={'class': text_input_class, 'placeholder': 'e.g., International Convention City Bashundhara'}),
            'category': forms.Select(attrs={'class': select_input_class}),
        }

# ==============================================================================
#  Participant Form
# ==============================================================================
class ParticipantForm(forms.ModelForm):
    events = forms.ModelMultipleChoiceField(
        queryset=Event.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Select Events to Join"
    )

    class Meta:
        model = Participant
        fields = ['name', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': text_input_class, 'placeholder': 'Enter participant name'}),
            'email': forms.EmailInput(attrs={'class': text_input_class, 'placeholder': 'Enter a valid email address'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)

        if commit:
            instance.save()
            instance.events.set(self.cleaned_data['events']) 
        return instance

# ==============================================================================
#  Category Form
# ==============================================================================
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': text_input_class, 'placeholder': 'e.g., Technology, Workshop, Seminar'}),
            'description': forms.Textarea(attrs={'class': textarea_class, 'placeholder': 'Write a short description for this category...'}),
        }
