# Flask ToDo App

A secure, user-friendly ToDo web application built with Flask, following the MVC (Model-View-Controller) architecture.

## Features

- **User Registration & Login:** Secure authentication with session management.
- **ToDo Management:** Add, edit, delete, filter, and sort your ToDo items.
- **Theme Switching:** Toggle between light and dark themes.
- **Logout:** Securely end user sessions.
- **MVC Architecture:** Clean separation of concerns for maintainability.

## Technologies Used

- **Flask:** Python web framework for routing, session management, and templating.
- **Jinja2:** For dynamic HTML rendering.
- **HTML/CSS:** For the user interface.

## Project Structure
app/ 
├── controllers/ # Controller logic (routes, request handling) 
│ └── user_controller.py 
├── services/ # Business logic and data management 
│ └── user_service.py 
├── templates/ # Jinja2 HTML templates (Views) 
│ └── todo_list.html 
├── static/ # CSS and static files 
└── app.py # App entry point


- **Model:** Data and business logic in `services/`.
- **View:** HTML templates in `templates/`.
- **Controller:** Route handling in `controllers/`.

## How It Works

1. **Authentication:** Users register and log in. Sessions are managed using Flask’s `session` object.
2. **ToDo Operations:** Authenticated users can create, edit, delete, filter, and sort ToDo items.
3. **Theme Switching:** Users can toggle between light and dark themes.
4. **Logout:** Users can securely log out, which clears their session.

## Getting Started

1. Clone the repository.
2. Install dependencies:  
   ```bash
   pip install -r requirements.txt

## Security
Passwords are securely handled.
Session-based authentication protects user data.
Logout functionality ensures sessions are properly terminated.

## License
MIT
