# Zoombayit

Booking API for a fictional fitness studio using Python. The goal is to evaluate your coding skills, design thinking, and understanding of backend development principles.

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/jaypareek/Zoombayit.git
   ```

2. **Create a virtual environment**
   ```bash
   # Windows
   python -m venv zoo
   & '.\zoo\Scripts\Activate.ps1'

   # macOS/Linux
   python3 -m venv zoo
   source zoo/bin/activate
   ```

3. **Install dependencies**
   ```bash
   cd Zoombayit
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser and seed data**
   ```bash
   python manage.py organizer
   ```
   This command will:
   - Create a superuser (username: admin, password: admin)
   - Import activities from file/organizer/activities.csv
   - Import classes from file/organizer/classes.csv
   - Create sample bookings from file/organizer/bookings.csv

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```
   The API will be available at http://127.0.0.1:8000/core/api/v1.0/ or http://localhost:8000/core/api/v1.0/

## API Endpoints

### Base URL
```
/core/api/v1.0/
```

### Activities
- **GET /core/api/v1.0/activities/** - List all activities
- **GET /core/api/v1.0/activities/{id}/** - Get activity details
- **POST /core/api/v1.0/activities/** - Create a new activity
- **PUT /core/api/v1.0/activities/{id}/** - Update an activity
- **DELETE /core/api/v1.0/activities/{id}/** - Delete an activity

### Classes
- **GET /core/api/v1.0/classes/** - List all classes
- **POST /core/api/v1.0/classes/?tz={Asia/Kolkata}** - List Class by Given TimeZome
- **GET /core/api/v1.0/classes/{id}/** - Get class details
- **POST /core/api/v1.0/classes/** - Create a new class
- **PUT /core/api/v1.0/classes/{id}/** - Update a class
- **DELETE /core/api/v1.0/classes/{id}/** - Delete a class

### Bookings
- **GET /core/api/v1.0/bookings/** - List all bookings
- **GET /core/api/v1.0/bookings/?email={email}** - Get bookings for a specific email

### Book
- **POST /core/api/v1.0/book/** - Create a new booking

## Sample API Requests and Responses

### Create a New Activity
**Request:**
```json
POST /api/v1.0/activities/
{
  "name": "Yoga",
  "description": "Beginner friendly yoga class",
  "created_by": 1,
  "updated_by": 1
}
```

**Response:**
```json
{
  "id": 1,
  "name": "Yoga",
  "description": "Beginner friendly yoga class",
  "created_at": "2023-11-15T10:30:00Z",
  "updated_at": "2023-11-15T10:30:00Z",
  "created_by": 1,
  "updated_by": 1
}
```

### Create a New Class
**Request:**
```json
POST /api/v1.0/classes/
{
  "name": "Morning Yoga",
  "description": "Start your day with energizing yoga",
  "delivery_date": "2023-12-01T08:00:00Z",
  "cutoff_date": "2023-11-30T20:00:00Z",
  "allow_waitlist": true,
  "instructor": 2,
  "activities": [1],
  "available_slots": 15,
  "is_active": true,
  "created_by": 1,
  "updated_by": 1
}
```

**Response:**
```json
{
  "id": 1,
  "name": "Morning Yoga",
  "description": "Start your day with energizing yoga",
  "delivery_date": "2023-12-01T08:00:00Z",
  "cutoff_date": "2023-11-30T20:00:00Z",
  "delivery_date_local": "2023-12-01T08:00:00+05:30",
  "cutoff_date_local": "2023-11-30T20:00:00+05:30",
  "server_timezone": "UTC",
  "server_time": "2023-11-15T10:35:00Z",
  "allow_waitlist": true,
  "instructor": 2,
  "activities": [1],
  "available_slots": 15,
  "is_active": true,
  "created_at": "2023-11-15T10:35:00Z",
  "updated_at": "2023-11-15T10:35:00Z",
  "created_by": 1,
  "updated_by": 1
}
```

### Create a New Booking
**Request:**
```json
POST /api/v1.0/book/
{
  "client_name": "John Doe",
  "client_email": "john.doe@example.com",
  "classes": 1
}
```

**Response:**
```json
{
  "id": 1,
  "client_name": "John Doe",
  "client_email": "john.doe@example.com",
  "classes": 1,
  "created_at": "2023-11-15T11:00:00Z",
  "updated_at": "2023-11-15T11:00:00Z",
  "created_by": 1,
  "updated_by": 1,
  "is_active": true,
  "is_waitlisted": false
}
```

### Get Bookings for a Specific Email
**Request:**
```
GET /api/v1.0/bookings/?email=john.doe@example.com
```

**Response:**
```json
[
  {
    "id": 1,
    "client_name": "John Doe",
    "client_email": "john.doe@example.com",
    "classes": 1,
    "created_at": "2023-11-15T11:00:00Z",
    "updated_at": "2023-11-15T11:00:00Z",
    "created_by": 1,
    "updated_by": 1,
    "is_active": true,
    "is_waitlisted": false
  }
]
```

## Features
- Timezone support for class delivery and cutoff dates
- Waitlist functionality when classes are full
- Email validation for bookings
- Prevention of duplicate bookings (unique constraint on email and class)
