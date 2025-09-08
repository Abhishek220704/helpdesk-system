# Helpdesk Ticketing System

A lightweight **Helpdesk Ticket Management System** built with **Flask**, **SQLite**, and **HTML/CSS**.  
It allows users to register, log in, create support tickets, update them, and track progress via a simple dashboard.

---

## 🚀 Features

- **User Authentication**
  - Register and log in securely
  - Session-based user handling

- **Ticket Management**
  - Create new tickets with title, description, and category
  - Update ticket status and details
  - View all tickets in a personal dashboard

- **Database Integration**
  - SQLite for persistent storage
  - `init_db.py` for easy setup

- **Frontend**
  - HTML templates with Jinja2
  - Styled using `static/style.css`

- **Deployment Ready**
  - `Procfile` for Heroku deployment

---

## 📂 Project Structure

```
helpdesk-system-main/
│── app.py                # Main Flask app
│── init_db.py            # Database initialization script
│── database.db           # SQLite database
│── requirements.txt      # Python dependencies
│── Procfile              # Deployment config
│── static/               # CSS styles
│── templates/            # HTML templates
│── venv/                 # Virtual environment (can be ignored)
```

---

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/helpdesk-system-main.git
cd helpdesk-system-main
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # For Linux/Mac
venv\Scripts\activate    # For Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Initialize the Database
```bash
python init_db.py
```

### 5. Run the Application
```bash
python app.py
```
Visit: **http://127.0.0.1:5000/**

---

## 🌐 Deployment (Heroku Example)
1. Install Heroku CLI and login  
2. Create an app:  
   ```bash
   heroku create
   ```
3. Push to Heroku:  
   ```bash
   git push heroku main
   ```
4. Open your deployed app in browser.

---

## 📸 Screenshots (Optional)
- Login Page  
- Dashboard  
- Create Ticket  

---

## 🤝 Contributing
Contributions, issues, and feature requests are welcome!  
Feel free to fork the repo and submit a pull request.

---

## 📜 License
This project is licensed under the MIT License.
