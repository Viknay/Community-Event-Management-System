from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import User, Event,Category
from .serializers import *
from django.shortcuts import render
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

# Signup View (Handles both GET and POST)
@api_view(['GET', 'POST'])
def signup_view(request):
    if request.method == 'GET':
        # Render the signup page (HTML)
        return render(request, 'signup.html')

    elif request.method == 'POST':
        # Handle form submission for signup
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Create JWT tokens for the user
            
            return Response({
                "message":"Signup Successfully"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Login View (Handles both GET and POST)
@api_view(['GET', 'POST'])
def login_view(request):
    if request.method == 'GET':
        # Render the login page (HTML)
        return render(request, 'login.html')

    elif request.method == 'POST':
        # Handle form submission for login
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = User.objects.get(email=email)  # Use email instead of username
        except User.DoesNotExist:
            return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

        # User authenticated, create tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            "message":"login successfully",
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })


# Event creation view (Authenticated User only)
@api_view(['POST'])
def create_event(request):
    # Ensure the user is authenticated
    if not request.user.is_authenticated:
        return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
    
    # Confirm the user is a valid instance of User
    if not isinstance(request.user, User):
        return Response({"detail": "Invalid user."}, status=status.HTTP_400_BAD_REQUEST)

    title = request.data.get('title')
    description = request.data.get('description')
    location = request.data.get('location')
    category = request.data.get('category')
    if request.data.get('rsvp_limit'):
        rsvp_limit = request.data.get('rsvp_limit')
    else:
        rsvp_limit = 9999    

     # Ensure category exists
    try:
        category_instance = Category.objects.get(id=category)
    except Category.DoesNotExist:
        return Response({"detail": "Category not found."}, status=status.HTTP_400_BAD_REQUEST)
    
    # Create event with authenticated user as the organizer
    event = Event.objects.create(
        title=title,
        description=description,
        location=location,
        category_id=category,
        organizer=request.user,
        rsvp_limit=rsvp_limit,
    )
    
    return Response({"message": "Event created successfully", "event_id": event.id}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_event(request, id=None):
    try:
        if id:
            # Retrieve a single event by ID
            event = Event.objects.get(id=id)
            serializer = EventSerializer(event)
            return Response(serializer.data)
        else:
            # Search for events based on query parameters
            query = request.GET.get('query', '')
            category = request.GET.get('category', '')
            location = request.GET.get('location', '')

            # Build query using Q objects
            filters = Q()
            if query:
                filters &= Q(title__icontains=query)
            if category:
                filters &= Q(category__name__icontains=category)
            if location:
                filters &= Q(location__icontains=location)

            # Filter events
            events = Event.objects.filter(filters)
            serializer = EventSerializer(events, many=True)
            return Response(serializer.data)
    except Event.DoesNotExist:
        return Response({"error": "Event not found"}, status=404)
    except Exception as e:
        return Response({"error": f"Unable to retrieve events: {str(e)}"}, status=500)

   


# Update Event View
@api_view(['PUT'])
def update_event(request, id):
    try:
        # Ensure the user is authenticated
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Fetch the event to update
        event = get_object_or_404(Event, id=id)

        # Ensure the authenticated user is the organizer of the event
        if event.organizer != request.user:
            return Response({"detail": "You do not have permission to edit this event."}, status=status.HTTP_403_FORBIDDEN)
        
        # Update the event
        serializer = EventSerializer(event, data=request.data, partial=True)  # Use partial=True to allow partial updates
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Event updated successfully", "event": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": f"Unable to update event: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Delete Event View
@api_view(['DELETE'])
def delete_event(request, id):
    try:
        # Ensure the user is authenticated
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Fetch the event to delete
        event = get_object_or_404(Event, id=id)

        # Ensure the authenticated user is the organizer of the event
        if event.organizer != request.user:
            return Response({"detail": "You do not have permission to delete this event."}, status=status.HTTP_403_FORBIDDEN)
        
        # Delete the event
        event.delete()
        return Response({"message": "Event deleted successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": f"Unable to delete event: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])    
def get_category(request):
    try:
        categorys = Category.objects.all()
        serializer = CategorySerializer(categorys, many=True)    
        return Response(serializer.data)    
    except Event.DoesNotExist:
        return Response({"error": "Category not found"}, status=404)
    except Exception as e:
        return Response({"error": "Unable to retrieve categorys"}, status=500)
    except:
        return Response({"error":"An error occured during fetching category"}, status=500)


@api_view(['POST'])  
def rsvp( request, event_id):
        try:
            if not request.user.is_authenticated:
                return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

            event = Event.objects.get(id=event_id)
    
            if RSVP.objects.filter(user=request.user, event=event).exists():
                return Response("An RSVP with this user and event already exists.")
        
            rsvp_count = RSVP.objects.filter(event=event).count()

            if event.rsvp_limit <= rsvp_count:
                return Response({"error": "Event is full"}, 403)
            
            data = {
                "user": request.user.id,
                "event": event_id
            }
            
            rsvpSerializer = RSVPSerializer(data=data)
            if rsvpSerializer.is_valid(raise_exception=True):
                rsvpSerializer.save()
                if event.rsvp_count is None:
                    event.rsvp_count = 1
                else:
                    event.rsvp_count += 1
                return Response({"success": "RSVP successful"}, status=200)
        
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=500)        