# Library Management System

A simple library management system implemented using Flask, SQLAlchemy, and other technologies.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction

This project is a library management system developed using Flask, SQLAlchemy, and other Python libraries. It provides basic functionality for managing books, customers, and loans within a library. The system includes features such as adding, updating, and deleting books and customers, managing loans, and user authentication.

## Features

- Add and display books.
- AAdd and display customers.
- Manage book loans, including due dates and return status.
- User authentication with JWT (JSON Web Tokens).
- ...

## Prerequisites

- Python 3.x
- Flask
- Flask-SQLAlchemy
- Flask-CORS
- Flask-JWT-Extended
- Flask-Bcrypt
- ...

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/library-management-system.git
    ```

2. Change to the project directory:

    ```bash
    cd library-management-system
    ```

3. Create a virtual environment (optional but recommended):

    ```bash
    python -m venv venv
    ```

4. Activate the virtual environment:

    ```bash
    # On Windows
    .\venv\Scripts\activate

    # On macOS/Linux
    source venv/bin/activate
    ```

5. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the application:

    ```bash
    python app.py
    ```

2. Access the application in your web browser at `http://127.0.0.1:5000/`.

## API Endpoints

API Endpoints
/add_book: Add a new book.
/books: View all books.
/loan_book: Loan a book to a customer.
/loans: View all loans.
/late_loans: View late loans.
/loans/<int:loan_id>: Delete a loan.
/customers: View all customers.
/add_customer: Add a new customer.
/search_books: Search for books by name.
/search_customers: Search for customers by name.
/user/register: Register a new user.
/user/login: Login as a user.
/logout: Logout a user.

For more details on API endpoints and usage, refer to the [API Documentation](API_DOCUMENTATION.md).

## Authentication

The application uses JSON Web Tokens (JWT) for user authentication. To register and log in users, use the following endpoints:

- **POST** `/user/register`: Register a new user.
- **POST** `/user/login`: Log in and get a JWT token.
- ...

## Contributing

If you'd like to contribute to this project, please follow the [Contributing Guidelines](CONTRIBUTING.md).

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

For any inquiries or issues, please contact [mohamed daief](mohameddaief.@gmail.com).
