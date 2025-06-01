# Codder

## a freelancer platform build with Django

This is the backend of a Freelancer Platform built with Django and Django REST Framework (DRF). It provides a RESTful API for a marketplace where freelancers can offer services and clients can browse and order.

# Key Features

- 🔐 **Authentication**: Secure login with two user roles – **Client** and **Freelancer**
- 🧑‍💼 **Freelancers**: Create and manage service offers; track and update order status
- 🛒 **Clients**: Browse offers, place orders, and leave reviews
- ⭐ **Reviews**: Clients can rate freelancers

# How To Use

## 🚀 Installation

Follow these steps to set up and run the Django backend locally:

### 1. Clone the Repository

```bash
git clone https://github.com/KaloyanIvan0v/coderr-backend.git
cd your-project-name
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv env
source env/bin/activate # On macOS/Linux
env\Scripts\activate # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up the Database

```bash
python manage.py migrate
```

### 5. Create a Superuser (for Admin Panel)

```bash
python manage.py createsuperuser
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

# License

MIT
