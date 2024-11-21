# Community Event Management System
A Django-based application designed to help users create, manage, and RSVP to community events. The system allows event organizers to create events, manage categories, and users to register, log in, and RSVP to events.

# Features
1. User Authentication: Users can sign up, log in, and manage their account details.
2. Event Management: Organizers can create, update, and delete events.
3. RSVP System: Users can RSVP to events, and organizers can set RSVP limits.
4. Categories: Events can be categorized, making it easier for users to find relevant events.
5. Role-based Access: Admins have full access to all functionalities, while regular users can only manage their own events and RSVPs.

# Technologies Used
Django 5.1.3
Django Rest Framework for building APIs
JWT (JSON Web Token) for secure authentication
SQLite (for development) or any other relational database
Python 3.11 (or higher)

# Installation
Prerequisites
Python 3.11 or higher
Django 5.1.3 or higher
pip (Python package manager)

# Steps

1. Clone the repository:
    git clone https://github.com/viknay/Community-Event-Management-System.git
    
    cd Community-Event-Management-System

2. Setup vertual environment:
     python -m venv myenv
    
    # On Windows, use `myenv\Scripts\activate`

    cd backend 

3. Install dependencies:
    pip install -r requirements.txt

4. Apply migrations to set up the database:
    python manage.py migrate    

5. Create a superuser to access the admin panel:
    python manage.py createsuperuser

6. Start the development server:
    python manage.py runserver   

# How to use application

<!-- To Signup use these data to test -->

    curl -X POST http://127.0.0.1:8000/api/v1/signup/ -H "Content-Type: application/json" -d "{\"username\":\"johndoe\", \"password\":\"67890\", \"email\":\"john.doe@gmail.com\", \"first_name\":\"John\", \"last_name\":\"Doe\", \"contact_number\":\"9876543210\", \"gender\":\"M\"}"

    {"message":"Signup Successfully"}

<!-- To Signup use these data to test -->   

<!-- To login -->
    curl -X POST http://127.0.0.1:8000/api/v1/login/ -H "Content-Type: application/json" -d "{\"email\":\"john.doe@gmail.com\",\"password\":\"67890\"}"

    {"message":"login successfully","refresh":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTczMjI3NzkyNSwiaWF0IjoxNzMyMTkxNTI1LCJqdGkiOiIyNWE2ZmNiMTAwMWI0YThiOTJjODM3MzhmNjdkZGVmMiIsInVzZXJfaWQiOjEzfQ.1_D7xf4W6hKmnf0yTrobuP-IOKniJOYOqLeYsF0T7HU","access":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMyMTkyNDI1LCJpYXQiOjE3MzIxOTE1MjUsImp0aSI6IjM2OTZkYTY2M2Q0ZTQ4OGVhM2FiOTY0ZWRkYTdiOWI4IiwidXNlcl9pZCI6MTN9.S41WA_sSbrUen7iwuyBipeb7aQC7M5zFpw8UfopYPGk"}
<!-- To login -->

<!-- only admin can create category for event so admin have to store category from panel -->

<!-- Add events (only logged in users can create event) -->
    curl -X POST http://127.0.0.1:8000/api/v1/create_event/ -H "Content-Type: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMyMTkyNjcyLCJpYXQiOjE3MzIxOTE3NzIsImp0aSI6IjYyOWVmNDQzZWVlNjRiZDhiNTY1NTAzOTRjYTBlOGYyIiwidXNlcl9pZCI6MTN9.mfCSm7yyyDs3-IwMuNzqupXRjVYe2KOHzAR96NU97jg" -d "{\"title\":\"Tech Conference 2024\", \"description\":\"A conference on the latest in technology\", \"location\":\"New York City\", \"category\":1, \"rsvp_limit\":200}"

    {"message":"Event created successfully","event_id":8}
<!-- Add events (only logged in users can create event) -->

<!-- update event (only who created it) -->

    curl -X PUT http://127.0.0.1:8000/api/v1/update_event/8/ -H "Content-Type: application/json" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMyMjc4NTY4LCJpYXQiOjE3MzIxOTIxNjgsImp0aSI6IjVjMzk0MDY4ZDY2MTQwZThiMDQxNTBlZjJlMWU1YjYzIiwidXNlcl9pZCI6MTN9.xTaYOZjn7J6deWT06gMVKr0H30PQVoP_HdA1BePXUfA" -d "{\"location\":\"San Francisco\"}
{"message":"Event updated successfully","event":{"id":8,"title":"Tech Conference 2024","description":"A conference on the latest in technology","date":"2024-11-21","time":"17:54:13.936124","location":"San Francisco","rsvp_limit":200,"rsvp_count":null,"category":1,"organizer":13}}

<!-- update event (only who created it) -->

<!-- Delete Event (only who created it) -->
    curl -X DELETE http://127.0.0.1:8000/api/v1/delete_event/8/ -H "Authorization: Bearer 
    eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMyMjc4NTY4LCJpYXQiOjE3MzIxOTIxNjgsImp0aSI6IjVjMzk0MDY4ZDY2MTQwZThiMDQxNTBlZjJlMWU1YjYzIiwidXNlcl9pZCI6MTN9.xTaYOZjn7J6deWT06gMVKr0H30PQVoP_HdA1BePXUfA"

    {"message":"Event deleted successfully"}
<!-- Delete Event (only who created it) -->

<!-- get one event -->
     curl -X GET http://127.0.0.1:8000/api/v1/get_event/7/
    {"id":7,"title":"saloni","description":"Event Description","date":"2024-11-21","time":"16:57:22.569389","location":"Raipur","rsvp_limit":9999,"rsvp_count":null,"category":1,"organizer":11}
<!-- get one event -->

<!-- get list of event -->
  
curl -X GET http://127.0.0.1:8000/api/v1/get_event/
[{"id":2,"title":"Dance","description":"Event Description","date":"2024-11-21","time":"16:32:22.455680","location":"Raipur","rsvp_limit":null,"rsvp_count":null,"category":1,"organizer":11},{"id":3,"title":"Jumba","description":"Event Description","date":"2024-11-21","time":"16:45:29.204008","location":"Raipur","rsvp_limit":null,"rsvp_count":null,"category":1,"organizer":11},{"id":4,"title":"bc","description":"Event Description","date":"2024-11-21","time":"16:47:00.766507","location":"Raipur","rsvp_limit":null,"rsvp_count":null,"category":1,"organizer":11},{"id":5,"title":"Lamba","description":"hiii","date":"2024-11-21","time":"16:48:39.638338","location":"Raipur","rsvp_limit":99999,"rsvp_count":null,"category":1,"organizer":7},{"id":6,"title":"dolly","description":"Event Description","date":"2024-11-21","time":"16:49:55.929239","location":"Raipur","rsvp_limit":200,"rsvp_count":1,"category":1,"organizer":11},{"id":7,"title":"saloni","description":"Event Description","date":"2024-11-21","time":"16:57:22.569389","location":"Raipur","rsvp_limit":9999,"rsvp_count":null,"category":1,"organizer":11}]
<!-- get list of event -->

<!-- to RSVP for any event -->
   >curl -X POST http://127.0.0.1:8000/api/v1/rsvp/7/ -H "Authorization: Bearer 
   eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMyMjc5MTM2LCJpYXQiOjE3MzIxOTI3MzYsImp0aSI6IjY0MjJlZDMzNWYwMzQwNjJiMTgxMWI5OTY5OGM0MDNhIiwidXNlcl9pZCI6MTF9.uJN_TucPpwlZHi7Xt3Bmszd0I2IsC4VyQPaETWT3IVU"
    
   {"success":"RSVP successful"}
<!-- to RSVP for any event -->

# Extra details

    Admin have option to searching for events, filtering by date, category or location, and sorting options.
    User have option to searching for events, filtering by date, category or location, and sorting options.
