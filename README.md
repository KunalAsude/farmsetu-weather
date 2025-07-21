# 🌦️ FarmSetu Weather Data API & Dashboard

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-Supported-2496ED?logo=docker)](https://www.docker.com/)
[![GitHub Actions](https://github.com/yourusername/farmsetu-weather/actions/workflows/django.yml/badge.svg)](https://github.com/yourusername/farmsetu-weather/actions)

> **Latest Update (July 2024)**: Added interactive dashboard with yearly averages visualization and improved data filtering capabilities.

A comprehensive Django application featuring a REST API and interactive dashboard for parsing, storing, and visualizing UK weather data from MetOffice's `UK.txt` format. This project provides:

- 📊 Interactive dashboard with charts and data visualization
- 🔍 Clean, well-documented REST API endpoints
- 🐳 Docker support for easy deployment
- 🔄 CI/CD pipeline with GitHub Actions
- 📱 Responsive design for all devices

## Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Docker Deployment](#docker-deployment)
- [Development Setup](#development-setup)
- [Running Tests](#running-tests)
- [License](#license)
- [Key Features](#key-features)
- [API Endpoints](#api-endpoints)
- [Local Development](#local-development)
- [Testing](#testing)
- [Docker Setup](#docker-setup)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

FarmSetu Weather Data API is a Django-based solution that:

- Parses raw weather data from MetOffice's `UK.txt` format
- Stores data in a structured SQLite database
- Exposes RESTful endpoints for data access
- Provides filtering and aggregation capabilities
- Includes a web dashboard for data visualization

## Project Structure

```
farmsetu_weather_project/
├── farmsetu_weather_project/    # Project configuration
│   ├── __init__.py
│   ├── settings.py             # Django settings
│   ├── urls.py                 # Main URL configuration
│   └── wsgi.py                 # WSGI config
├── weather/                    # Main app
│   ├── management/commands/    # Custom management commands
│   ├── migrations/             # Database migrations
│   ├── __init__.py
│   ├── admin.py               # Admin configuration
│   ├── apps.py                # App config
│   ├── models.py              # Database models
│   ├── parsers.py             # Data parsing logic
│   ├── serializers.py         # API serializers
│   ├── tests.py               # Test cases
│   ├── urls.py               # App URL configuration
│   └── views.py              # API views
├── static/                    # Static files (CSS, JS, images)
├── templates/                 # HTML templates
├── manage.py                  # Django management script
└── requirements.txt           # Project dependencies
```

## Key Features

- **Interactive Dashboard**: Real-time visualization of weather data with interactive charts
- **Yearly Averages**: View historical trends with yearly average temperature and rainfall data
- **Responsive Design**: Works on all device sizes from mobile to desktop
- **Data Parsing**: Efficient parsing of MetOffice's `UK.txt` format
- **RESTful API**: Clean, well-documented endpoints following REST principles
- **Data Filtering**: Filter weather data by region, parameter, and date range
- **Data Aggregation**: Built-in support for data summarization
- **Admin Interface**: Built-in Django admin for data management
- **Test Coverage**: Comprehensive test suite for models and API endpoints

## API Endpoints

### Core Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/regions/` | GET | List all available regions |
| `/api/parameters/` | GET | List all weather parameters |
| `/api/weather-data/` | GET | List all weather data (filterable) |
| `/api/weather-data/<id>/` | GET | Get specific weather record |
| `/api/parse-data/` | POST | Trigger data parsing (admin only) |

### Dashboard Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/summary/` | GET | Get yearly averages for a region and parameter |
| `/api/chart-data/` | GET | Get formatted monthly data for charts |

#### Summary Endpoint Parameters
- `region`: Region code (e.g., 'UK')
- `parameter`: Weather parameter (e.g., 'Tmean' for temperature, 'Rainfall')

Example: `/api/summary/?region=UK&parameter=Tmean`

#### Chart Data Endpoint Parameters
- `region`: Region code (e.g., 'UK')
- `parameter`: Weather parameter (e.g., 'Tmean', 'Rainfall')
- `year_from`: Optional start year
- `year_to`: Optional end year

### Query Parameters

Most list endpoints support filtering using query parameters:

- `region`: Filter by region code (e.g., `UK`)
- `parameter`: Filter by parameter code (e.g., `Tmean` for mean temperature)
- `year`: Filter by specific year
- `year_from`: Filter records from this year (inclusive)
- `year_to`: Filter records up to this year (inclusive)

For date range filtering, you can use either:
- Single year: `?year=2023`
- Year range: `?year_from=2020&year_to=2023`

## Dashboard Features

### Interactive Visualization
- **Temperature Trends**: View monthly temperature trends for the last 2 years
- **Rainfall Analysis**: Track rainfall patterns with interactive charts
- **Yearly Averages**: Compare yearly average temperature and rainfall data
- **Responsive Design**: Optimized for both desktop and mobile viewing

### Data Exploration
- Filter data by region and parameter
- View detailed tooltips on hover
- Download charts as images
- Responsive layout adapts to screen size

## Local Development

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd farmsetu-weather-api
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Load sample data (if available)**
   ```bash
   python manage.py loaddata weather/fixtures/initial_data.json
   ```

6. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - API Root: http://127.0.0.1:8000/api/
   - Admin Interface: http://127.0.0.1:8000/admin/

## Testing

Run the test suite:

```bash
python manage.py test weather
```

For coverage reporting (if coverage.py is installed):

```bash
coverage run --source='.' manage.py test weather
coverage report
```

## Docker Setup

1. **Build the Docker image**
   ```bash
   docker build -t farmsetu-weather-api .
   ```

2. **Run the container**
   ```bash
   docker run -p 8000:8000 farmsetu-weather-api
   ```

## Accessing the Dashboard

After starting the application, access the dashboard at:
- Dashboard: http://localhost:8000/dashboard/
- API Documentation: http://localhost:8000/api/docs/

## Deployment

For production deployment, consider the following components:

### Application Server
- Gunicorn or uWSGI

### Database
- PostgreSQL (recommended for production)
- MySQL
- SQLite (development only)

### Web Server
- Nginx (recommended)
- Apache

### Environment Variables

Set the following environment variables for production:

```bash
export DJANGO_SECRET_KEY='your-secret-key'
export DEBUG=False
export ALLOWED_HOSTS='yourdomain.com,www.yourdomain.com'
export DATABASE_URL='your-database-url'
```

### Example Gunicorn Command

```bash
gunicorn --workers 3 --bind 0.0.0.0:8000 farmsetu_weather_project.wsgi:application
```

### Code Style

- Follow PEP 8 style guide
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Maintain test coverage above 80%

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

**Note**: This is a sample weather data API project. Ensure you have proper authorization before using MetOffice data in production environments.
