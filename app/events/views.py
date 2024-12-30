from rest_framework import viewsets
from .models import User, Category, Event, Comment
from .serializers import UserSerializer, CategorySerializer, EventSerializer, CommentSerializer


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Event, Comment, User, Category
from .forms import CustomUserCreationForm, CustomAuthenticationForm, EventForm, CommentForm, LikeForm
from django.http import HttpResponse

# These down are for API
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


# User Actions
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list_events')
    else:
        form = CustomUserCreationForm()
    return render(request, 'events/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('list_events')
        else:
            return render(request, 'events/login.html', {'error': 'Invalid credentials'})
    return render(request, 'events/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def delete_account(request):
    request.user.delete()
    return redirect('register')


# Event Actions
def list_events(request):
    events = Event.objects.all()
    return render(request, 'events/list_events.html', {'events': events})


@login_required
def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.save()
            form.save_m2m()  # Save many-to-many relationships
            return redirect('list_events')
    else:
        form = EventForm()
    return render(request, 'events/add_event.html', {'form': form})


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    comments = Comment.objects.filter(event=event)
    has_liked = request.user in event.liked_by.all()
    return render(request, 'events/event_detail.html', {'event': event, 'comments': comments, 'has_liked': has_liked})


@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    return redirect('list_events')


# Comment Actions
@login_required
def add_comment(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.event = event
            comment.save()
            return redirect('event_detail', event_id=event.id)
    else:
        form = CommentForm()
    return render(request, 'events/add_comment.html', {'form': form, 'event': event})


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    event_id = comment.event.id
    comment.delete()
    return redirect('event_detail', event_id=event_id)


# Like Actions
@login_required
def like_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    user = request.user._wrapped
    if user in event.liked_by.all():
        event.liked_by.remove(user)  # Unlike
    else:
        event.liked_by.add(user)  # Like

    return redirect('event_detail', event_id=event.id)


# Categories: kabum
@login_required
def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            category = Category.objects.create(name=name)
            return redirect('category_list')  # Redirect to the list of categories after adding
    return render(request, 'events/add_category.html')  # Render a form to add category


@login_required
def modify_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            category.name = name
            category.save()
            return redirect('category_list')  # Redirect to category list after modification
    return render(request, 'events/modify_category.html', {'category': category})  # Render form to modify category


@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')  # Redirect to the category list after deletion
    return render(request, 'events/delete_category.html', {'category': category})  # Render a confirmation page for deletion


# Note to self: somewhy my categories aren't listed in event_details
# !must fix!
@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'events/category_list.html', {'categories': categories})

# def list_events(request):
#      adasdasdasdasdasdasdas UPDATE DAMN TEMPLATE!!!
#     events = Event.objects.all()
#     return render(request, 'events/list_events.html', {'events': events})


# The following are api calls
@api_view(['GET'])
def api_events(request):
    event = Event.objects.all()
    serializer = EventSerializer(event, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def api_get_event(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
        serializer = EventSerializer(event)
        return Response(serializer.data)
    except Event.DoesNotExist:
        return Response({"error": "Event instance not found."}, status=status.HTTP_404_NOT_FOUND)


# These down don't work aahhhh
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
