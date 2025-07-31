# Expense Tracker Service

## Overview
The Expense Tracker Service is a comprehensive system designed to help users manage their personal finances effectively. It enables users to track their income, expenses, and savings, providing insights into their spending habits and assisting them in achieving their financial goals.

## Features
- **User Authentication**: Secure login and registration system to safeguard user data.
- **Expense Management**: Add, edit, and delete expenses with categories such as food, transportation, entertainment, etc.
- **Income Tracking**: Record and categorize income sources.
- **Budgeting**: Set monthly budgets and monitor progress.
- **Goal Management**: Define and track personalized financial goals, such as saving for a vacation, paying off debt, or building an emergency fund.

## Directory Structure
    expense-tracker/
    |── apps/                 # Sub-applications for modular design
    │   ├── expenses_system/  # Expense tracking functionality       
    │   ├── user_profile/     # User profile management
    │   ├── user_budget/      # Budgeting functionality
    │   └── user_auth/        # User authentication and authorization
    |
    ├── expenseTracker/       # Main Django application directory
    │   ├── __init__.py       # Package initialization
    │   ├── settings.py       # Django settings
    │   ├── urls.py           # URL routing
    │   ├── wsgi.py           # WSGI application
    │   └── asgi.py           # ASGI application 
    |
    ├── manage.py             # Django management script
    ├── requirements.txt      # Python dependencies
    ├── .env                  # Environment variables
    ├── .pg_service.conf      # Database Configuration
    ├── .gitignore            # Git ignore file
    └── README.md             # Project documentation

## System Architecture
The system is built using a modular architecture to ensure scalability and maintainability.

### Backend
- **Framework**: Django with Django REST Framework for building RESTful APIs.
- **Database**: PostgreSQL for storing user data, expenses, and budgets.
- **Authentication**: JSON Web Tokens (JWT) for secure user authentication.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/expense-tracker.git
    ```
2. Navigate to the project directory:
    ```bash
    cd expense-tracker
    ```
2. Create a python virtual environment:
    - **Windows**:
        ```powershell
        python -m venv venv
        ```
    - **Linux**:
        ```bash
        python3 -m venv venv
        ```
4. Install dependencies:
    - **Windows**:
        ```powershell
        pip install -r requirements.txt
        ```
    - **Linux**:
        ```bash
        pip3 install -r requirements.txt
        ```
5. Set up environment variables in a `.env` file:
    ```plaintext
    DJANGO_SECRET_KEY=<secret key for Django>
    ```
6. Configure Database Connectivity:
    - Create a `.pg_service.conf` file to store the database configuration:
        ```plaintext
        [my_service]
        host=<hosting> # Default: localhost
        port=<database connection port number> # Default: 5432
        user=<database username> # Default: postgres
        dbname=<database name> # Create a database and specify its name
        password=<database password>
        ```
    - Test the database connection:
        ```python
        import os
        import django
        from django.db import connections
        from django.db.utils import OperationalError

        # Set the DJANGO_SETTINGS_MODULE to your project's settings module
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expenseTracker.settings')  # Replace 'expenseTracker' with your project's name

        # Initialize Django
        django.setup()

        # Test the database connection
        try:
            connection = connections['default']
            connection.connect()
            print("Database connection successful!")
        except OperationalError as e:
            print(f"Database connection failed: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        ```
7. Start the development server:
    - **Windows**:
        ```powershell
        python manage.py runserver
        ```
    - **Linux**:
        ```bash
        python3 manage.py runserver
        ```

## API Documentation

For detailed API specifications and usage examples, refer to the Postman documentation:

- [Expense Tracker API Documentation](https://documenter.getpostman.com/view/31120750/2sAYkLmx6e)

This documentation provides a comprehensive guide to all available endpoints, request/response formats, and authentication requirements.

## Usage
1. Register a new account or log in with existing credentials.
2. Add your income and expenses with appropriate categories.
3. Set a monthly budget to monitor your spending.
4. View detailed reports and insights on the dashboard.