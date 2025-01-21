# task_manager

A simple web-based task management application built using Flask, enabling user registration, login, task creation, editing, and deletion.

Features
1. User Authentication:
a. Register new users.
b. Login with secure JWT-based authentication.

2. Task Management:
a. Add new tasks with a title and description.
b. Edit existing tasks.
c. Delete tasks.
d. View tasks in a user-specific dashboard.

3. Security:
a. Passwords are hashed using Werkzeug.
b. JWT tokens for secure session management.

4.Logging:
a. Tracks user actions and errors in app.log.

Images for reference
<img width="1139" alt="Screenshot 2025-01-21 at 6 21 21 PM" src="https://github.com/user-attachments/assets/52a609e2-42aa-43e3-a650-566fef84a4ea" />

<img width="1135" alt="Screenshot 2025-01-21 at 6 21 34 PM" src="https://github.com/user-attachments/assets/2966318e-e938-42d0-bc5e-262d8b8b234c" />

<img width="1144" alt="Screenshot 2025-01-21 at 6 47 42 PM" src="https://github.com/user-attachments/assets/b10f6038-2716-4ce6-ad18-f1df1962647f" />

<img width="1139" alt="Screenshot 2025-01-21 at 6 50 10 PM" src="https://github.com/user-attachments/assets/f53e4954-6b02-45e1-afee-9b7fe7108ee6" />
  
<img width="1141" alt="Screenshot 2025-01-21 at 6 50 22 PM" src="https://github.com/user-attachments/assets/2f0be676-9939-4d0c-82ad-f806063012ad" />


Technology Stack:
Backend: Flask, Flask-SQLAlchemy
Database: SQLite
Authentication: JWT
Frontend: HTML templates with Flask's Jinja2
Logging: Python's logging module

Installation
git clone https://github.com/your-username/task-manager.git
cd task-manager
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask run

Usage
Open the application in your browser: http://127.0.0.1:5000/
Register a new account or log in with existing credentials.
Add, edit, and manage tasks via the dashboard.


