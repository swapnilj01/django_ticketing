from django.utils.timezone import now
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from rest_framework import serializers, exceptions
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate

from .models import User, Event, EventAttendance
from .serializers import UserSerializer, EventSerializer, EventAttendanceSerializer
from .permissions import IsAdminUser

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response(
            {"message": "User registered successfully! Please log in."},
            status=status.HTTP_201_CREATED
        )

# List all events
class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

# Retrieve a single event
class EventDetailView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

# Attend / Unattend an event
class EventAttendanceView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EventAttendanceSerializer

    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        
        if event.date < now():
            return Response({'error': 'Cannot attend past events'}, status=status.HTTP_400_BAD_REQUEST)

        # Apply 5% discount for females
        ticket_price = event.ticket_price
        if request.user.gender == 'Female':
            ticket_price *= 0.95

        attendance, created = EventAttendance.objects.get_or_create(user=request.user, event=event)

        if created:
            return Response({'message': 'Successfully attended the event', 'discounted_price': ticket_price}, status=status.HTTP_201_CREATED)
        else:
            attendance.delete()
            return Response({'message': 'You have unattended the event'}, status=status.HTTP_200_OK)

# See who is attending an event
class EventAttendeesView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        event_id = self.kwargs['event_id']
        return User.objects.filter(eventattendance__event_id=event_id)


# Admin: Create an event
class EventCreateView(generics.CreateAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]  # Admin-only

    @swagger_auto_schema(
        operation_description="🔒 Admin Only: Create a new event.",
        responses={201: EventSerializer(), 403: "Forbidden: Only Admins can create events."},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

# Admin: Delete an event
class EventDeleteView(generics.DestroyAPIView):
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]  # Admin-only

    @swagger_auto_schema(
        operation_description="🔒 Admin Only: Delete an event.",
        responses={204: "Event deleted successfully", 403: "Forbidden: Only Admins can delete events."},
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
    
# Custom Token Serializer (Override Default JWT Login to Accept Email)
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "email" 

    def validate(self, attrs):
        email = attrs.get("email", None)
        password = attrs.get("password", None)

        user = User.objects.filter(email=email).first()

        if not user or not user.check_password(password):
            raise exceptions.AuthenticationFailed(
                {"detail": "Invalid email or password."},
                "no_active_account"
            )

        if not user.is_active:
            raise exceptions.AuthenticationFailed(
                {"detail": "This account is inactive."},
                "no_active_account"
            )

        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "user_id": user.id,
                "user_email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name
            }
        }

# Custom Login View
class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer