from rest_framework import serializers
from .models import Event, User, Category, Comment


class UserSerializer(serializers.ModelSerializer):
    liked_events = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
        source='liked_events'  # Uses the reverse relationship from `Event.liked_by`
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'liked_events']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class EventSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)  # Nested representation of categories
    liked_by = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )  # Users who liked this event

    class Meta:
        model = Event
        fields = [
            'id', 'name', 'description', 'region', 'precise_place', 'date',
            'repetition', 'duration', 'categories', 'price', 'liked_by'
        ]


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())

    class Meta:
        model = Comment
        fields = ['id', 'event', 'user', 'content', 'created_at']
