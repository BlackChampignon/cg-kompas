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
    first_category = serializers.SerializerMethodField()
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()
    # categories = CategorySerializer(many=True)  # Nested representation of categories
    liked_by = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )  # Users who liked this event
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Event
        fields = [
            'id', 'name', 'description', 'region', 'precise_place',
            'latitude', 'longitude', 'date', 'repetition', 'duration',
            'first_category', 'price', 'liked_by', 'image', 'theme_color'
        ]

    def get_first_category(self, obj):
        # Return the first category, or None if no categories exist
        first_category = obj.categories.first()
        return {
            "id": first_category.id,
            "name": first_category.name
        } if first_category else None

    def get_latitude(self, obj):
        # Extract latitude from precise_place
        if obj.precise_place:
            try:
                return float(obj.precise_place.split(",")[0].strip())
            except (ValueError, IndexError):
                return None
        return None

    def get_longitude(self, obj):
        # Extract longitude from precise_place
        if obj.precise_place:
            try:
                return float(obj.precise_place.split(",")[1].strip())
            except (ValueError, IndexError):
                return None
        return None


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())

    class Meta:
        model = Comment
        fields = ['id', 'event', 'user', 'content', 'created_at']
