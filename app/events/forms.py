from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Event, Comment, Category


# Form for User Registration (custom user model)
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})


# Form for User Login
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


# Form for Event Creation or Editing
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'region', 'precise_place', 'date', 'repetition', 'duration', 'categories', 'price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'region': forms.TextInput(attrs={'class': 'form-control'}),
            'precise_place': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'repetition': forms.TextInput(attrs={'class': 'form-control'}),
            'duration': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }


# Form for Adding Comments to an Event
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write a comment...'}),
        }


# Form for Liking an Event (no fields required, the form is just for the user-event relationship)
class LikeForm(forms.ModelForm):
    class Meta:
        model = Event.liked_by.through  # Accessing the Many-to-Many through model
        fields = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Custom method to set the like for a user and event
    def save(self, user, event, commit=True):
        instance = super().save(commit=False)
        instance.user = user
        instance.event = event
        if commit:
            instance.save()
        return instance
