from rest_framework import viewsets
from .serializers import UserSerializer, CategorySerializer, EventSerializer, CommentSerializer

from .models import Event, Comment, User, Category

from django.apps import apps

# These down are for API
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes

# For google and facebook login/registration
from rest_framework.views import APIView
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token
import requests as http_requests
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken


GOOGLE_ID = "<YOUR_GOOGLE_CLIENT_ID>"
FACEBOOK_ID = "<YOUR_FACEBOOK_APP_ID>"
FACEBOOK_SECRET = "<YOUR_FACEBOOK_APP_SECRET>"


class Socials(APIView):

    def post(self, request):
        provider = request.data.get('provider')
        token = request.data.get('token')
        email = request.data.get('email')

        if provider == 'google':
            return self.handle_google_token(token)
        elif provider == 'facebook':
            return self.handle_facebook_token(token, request)
        elif provider == 'email':
            return self.handle_social_login(email, provider)
        else:
            return Response({"error": "Invalid provider"}, status=status.HTTP_400_BAD_REQUEST)

    def handle_google_token(self, token):
        try:
            idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), GOOGLE_ID)
            email = idinfo.get('email')

            if not email:
                return Response({"error": "Email not found in Google token"}, status=status.HTTP_400_BAD_REQUEST)

            return self.handle_social_login(email, 'google')

        except ValueError:
            return Response({"error": "Invalid Google token"}, status=status.HTTP_400_BAD_REQUEST)

    def handle_facebook_token(self, token, request):
        try:
            app_id = FACEBOOK_ID
            app_secret = FACEBOOK_SECRET
            url = f"https://graph.facebook.com/debug_token?input_token={token}&access_token={app_id}|{app_secret}"
            resp = http_requests.get(url).json()

            if not resp.get('data', {}).get('is_valid'):
                return Response({"error": "Invalid Facebook token"}, status=status.HTTP_400_BAD_REQUEST)

            email = request.data.get('email')  # !Check if facebook returns the email

            if not email:
                return Response({"error": "Email not found in Facebook token"}, status=status.HTTP_400_BAD_REQUEST)

            return self.handle_social_login(email, 'facebook')

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def handle_social_login(self, email, provider):
        User = get_user_model()
        user = User.objects.filter(email=email).first()

        if not user:
            # Modify dat (create a user)
            pass

        # gen JWT tokens for the user and return dem
        refresh = RefreshToken.for_user(user)

        return Response({
            'access_token': str(refresh.access_token),  # Access token
            'refresh_token': str(refresh),              # Refresh token
        })


class RegisterAPI(APIView):
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if User.objects.filter(email=email).exists():
            return Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            registration_method='email'
        )
        return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)


class LoginAPI(APIView):
    def post(self, request):
        email = str(request.data.get('email'))
        password = str(request.data.get('password'))

        if not email or not password:
            return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        User = apps.get_model('events', 'User')

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"error": "Invalid email "}, status=status.HTTP_401_UNAUTHORIZED)
        print(user.email)
        print(email)
        # if not authenticate(request, email=email, password=password):
        if (email != user.email) or (password != user.password):
            return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "Login successful",
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
        }, status=status.HTTP_200_OK)


# The following are API calls
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


# Here we test!
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def api_aut_event(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
        serializer = EventSerializer(event)
        return Response(serializer.data)
    except Event.DoesNotExist:
        return Response({"error": "Event instance not found."}, status=status.HTTP_404_NOT_FOUND)


# These down don't work aahhhh hell
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
