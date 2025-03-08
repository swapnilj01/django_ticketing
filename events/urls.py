from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    RegisterView, CustomLoginView, EventListView, EventDetailView,
    EventCreateView, EventDeleteView, EventAttendanceView, EventAttendeesView
)

urlpatterns = [
    # User authentication
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Event routes
    path('events/', EventListView.as_view(), name='event-list'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('events/create/', EventCreateView.as_view(), name='event-create'),
    path('events/<int:pk>/delete/', EventDeleteView.as_view(), name='event-delete'),

    # Attendance routes
    path('events/<int:event_id>/attend/', EventAttendanceView.as_view(), name='event-attend'),
    path('events/<int:event_id>/attendees/', EventAttendeesView.as_view(), name='event-attendees'),
]
