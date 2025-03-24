# Django Mini-Blog

A feature-rich mini-blog application built with Django.

## Features

- User Authentication (Registration, Login, Logout)
- Blog Post Management (CRUD operations)
- Comments System
- Categories and Tags
- User Profiles with Profile Pictures
- Search Functionality
- Pagination
- Admin Panel
- Responsive Design with Bootstrap

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

7. Visit http://127.0.0.1:8000/ in your browser

## Project Structure

- `blog/` - Main application directory
  - `templates/` - HTML templates
  - `static/` - Static files (CSS, JS, images)
  - `models.py` - Database models
  - `views.py` - View logic
  - `urls.py` - URL routing
  - `forms.py` - Form definitions

## Custom Features

1. Comments System
   - Users can comment on blog posts
   - Nested comments support
   - Comment moderation

2. Categories and Tags
   - Organize posts by categories
   - Tag-based filtering
   - Category-based navigation

3. User Profiles
   - Profile pictures
   - User bios
   - Profile customization

4. Search Functionality
   - Full-text search
   - Filter by category/tag
   - Search results pagination

5. Pagination
   - Posts per page
   - Category/tag-based pagination
   - Search results pagination 