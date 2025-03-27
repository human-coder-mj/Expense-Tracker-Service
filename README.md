# Expense Tracker Service

## Overview
The Expense Tracker Service is a comprehensive system designed to help users manage their personal finances effectively. It enables users to track their income, expenses, and savings, providing insights into their spending habits and assisting them in achieving their financial goals.

## Features
- **User Authentication**: Secure login and registration system to safeguard user data.
- **Expense Management**: Add, edit, and delete expenses with categories such as food, transportation, entertainment, etc.
- **Income Tracking**: Record and categorize income sources.
- **Budgeting**: Set monthly budgets and monitor progress.

## System Architecture
The system is built using a modular architecture to ensure scalability and maintainability.

### Backend
- **Framework**: Django with Django REST Framework for building RESTful APIs.
- **Database**: PostgreSQL for storing user data, expenses, and budgets.
- **Authentication**: JSON Web Tokens (JWT) for secure user authentication.

### Deployment
- **Hosting**: Deployed on cloud platforms such as AWS.
- **CI/CD**: Automated pipelines for testing and deployment using GitHub Actions.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/expense-tracker.git
    ```
2. Navigate to the project directory:
    ```bash
    cd expense-tracker
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Set up environment variables in a `.env` file:
    ```plaintext
    DJANGO_SECRET_KEY=<secret key for Django>
    ```
5. Start the development server:
    - **Windows**:
        ```powershell
        python manage.py runserver
        ```
    - **Linux**:
        ```bash
        python3 manage.py runserver
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

## API Documentation

For detailed API specifications and usage examples, refer to the Postman documentation:

- [Expense Tracker API Documentation](https://documenter.getpostman.com/view/31120750/2sAYkLmx6e)

This documentation provides a comprehensive guide to all available endpoints, request/response formats, and authentication requirements.

## Usage
1. Register a new account or log in with existing credentials.
2. Add your income and expenses with appropriate categories.
3. Set a monthly budget to monitor your spending.
4. View detailed reports and insights on the dashboard.

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push them to your fork.
4. Submit a pull request with a detailed description of your changes.
