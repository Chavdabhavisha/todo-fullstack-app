📝 Todo App (React + Flask + MongoDB + Google Auth + Email Notification)
This is a full-stack Todo List application built using:

✅ React (frontend)

🐍 Flask (backend)

🌱 MongoDB Atlas (database)

🔐 JWT Authentication with Google Login

📧 Email notification when a todo is created

🚀 Features
Sign in using Google

Create, edit, complete, or delete todos

Email is sent on new todo creation

Fully authenticated CRUD with JWT tokens

Mobile-friendly and styled UI

📁 Project Structure
java
Copy
Edit
todo-app/
├── backend/
│   ├── app.py
│   ├── extensions.py
│   ├── routes/
│   │   ├── auth_routes.py
│   │   └── todo_routes.py
│   ├── .env
│   └── requirements.txt
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
├── .gitignore
├── README.md
⚙️ Setup Instructions
1. Clone the repository
bash
Copy
Edit
git clone https://github.com/YOUR_USERNAME/todo-fullstack.git
cd todo-fullstack
2. Backend Setup (Flask)
bash
Copy
Edit
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
Create .env file inside backend/ and add:

ini
Copy
Edit
MONGO_URI=your_mongodb_uri
JWT_SECRET_KEY=your_jwt_secret
GOOGLE_CLIENT_ID=your_google_client_id

MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=youremail@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_DEFAULT_SENDER=youremail@gmail.com
Run the backend:

bash
Copy
Edit
python app.py
3. Frontend Setup (React)
bash
Copy
Edit
cd ../frontend
npm install
npm start
The app will run at http://localhost:3000 and connect with the Flask backend.

🌐 Live Demo
To be added after Render deployment.

✅ Todo Before Deployment
Push this project to GitHub ✅

Deploy Flask backend on Render

Deploy React frontend on Render

Configure .env in Render dashboard (never upload .env to GitHub)

🛡️ Environment Variables (example)
Create a file named .env.example and add:

makefile
Copy
Edit
MONGO_URI=
JWT_SECRET_KEY=
GOOGLE_CLIENT_ID=
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_DEFAULT_SENDER=
🔒 Do not include .env in the repo. It’s already protected in .gitignore.

📧 Email Feature
When a todo is created, an email is sent to the authenticated user (email from Google Login) via Gmail SMTP.

You must generate a Gmail App Password to enable sending.

🙋‍♀️ Author
Bhavisha Chavda
Built with ❤️ and chai ☕
GITHUB-https://github.com/Chavdabhavisha
LINKEDIN-https://www.linkedin.com/in/bhavisha-chavda-6a170627b?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app 