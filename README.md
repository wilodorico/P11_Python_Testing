# Gudlift Competition Registration Platform

[![Python Version](https://img.shields.io/badge/python-3.x-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-1.1.2-green.svg)](https://flask.palletsprojects.com/)
[![Pytest](https://img.shields.io/badge/pytest-8.3.5-red.svg)](https://docs.pytest.org/)
[![Locust](https://img.shields.io/badge/locust-2.37.11-orange.svg)](https://locust.io/)

## 📚 Overview

This platform allows sports clubs to register for competitions, book places for their members, and manage their competition points. 
The application follows a clean architecture approach with separation of concerns between entities, 
repositories, and use cases.

## 🌟 Features

- **User Authentication**: Clubs can log in using their registered email addresses
- **Competition Listing**: View available competitions with dates and available places
- **Place Booking**: Clubs can reserve places in competitions
- **Points Management**: Clubs have points that are used for booking places
- **Dashboard**: View points status across all clubs

## 🏗️ Project Structure

This project follows **Clean Architecture** principles, which separates the application into distinct layers with clear dependencies flowing inward. This architecture ensures better maintainability, testability, and independence from external frameworks and databases.

### Clean Architecture Benefits:
- **Independence**: Business logic is isolated from external concerns (UI, database, frameworks)
- **Testability**: Each layer can be tested independently with mock implementations
- **Flexibility**: Easy to change external dependencies without affecting business rules
- **Maintainability**: Clear separation of concerns makes the code easier to understand and modify

```
├── entities/              # Domain models (Club, Competition, Reservation)
├── adapters/              # JSON data access implementations and in memory repository for tests
├── ports/                 # Interface definitions for repositories
├── templates/             # HTML templates for the web interface
├── tests/                 # Test suite
│   ├── integrations/      # Integration tests
│   ├── performance_tests/ # Locust performance tests
│   ├── units/             # Unit tests
│   └── conftest.py        # Pytest fixtures
├── usecases/              # Business logic implementations
├── *.json                 # Data files (clubs, competitions, reservations)
├── server.py              # Flask application
└── globals.py             # Global constants and configurations
```

## 💻 Installation

### Prerequisites

- Python 3.x
- [Virtualenv](https://virtualenv.pypa.io/en/stable/installation.html) (installed globally)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/wilodorico/P11_Python_Testing.git
   cd P11_Python_Testing
   ```

2. **Create and activate a virtual environment**
   ```bash
   # For Windows:
   python -m venv venv
   venv\Scripts\activate

   # For macOS/Linux:
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create .env file and paste**
   ```bash
   FLASK_APP=server.py
   FLASK_ENV=development
   FLASK_DEBUG=1
   SECRET_KEY="secret_key_mode_debug"
   ```

5. **Switch to QA branch for testing**
   ```bash
   git checkout QA
   ```

6. **Run the application**
   ```bash
   # For Windows:
   flask run
   # OR
   python -m flask run
   ```

7. **Access the application**
   Open your browser and go to `http://127.0.0.1:5000`

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Generates HTML report in htmlcov/
pytest --cov=. --cov-report=html
```

### Performance Testing

```bash
# Start the Flask server
flask run

# In a separate terminal, run Locust
cd tests/performance_tests

# Run in Web interface
# Run command and click on link
locust

# Run in terminal
# Run command
locust --headless --users 50 --spawn-rate 3 -H http://127.0.0.1:5000

```
Access the Locust web interface at `http://localhost:8089` to configure and run performance tests.

## 📊 Data Structure

The application uses JSON files for data storage:

- **clubs.json**: Contains club information including name, email, and points
- **competitions.json**: Lists available competitions with dates and places
- **reservations.json**: Tracks bookings made by clubs

## 👥 Test Users

You can log in using the following credentials:

| Club | Email | Points |
|------|-------|--------|
| Simply Lift | john@simplylift.co | 13 |
| Iron Temple | admin@irontemple.com | 4 |
| She Lifts | kate@shelifts.co.uk | 12 |

## 👤 Authors

wilodorico
