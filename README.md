# 🌦️ FarmSetu Weather Data API & Analytics Platform

[![Build Status](https://github.com/yourusername/farmsetu-weather/actions/workflows/django.yml/badge.svg)](https://github.com/yourusername/farmsetu-weather/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-brightgreen.svg)](https://python.org)
[![Django](https://img.shields.io/badge/django-4.2-green.svg)](https://djangoproject.com)
[![Docker](https://img.shields.io/badge/docker-supported-blue?logo=docker)](https://www.docker.com/)

> **Production-ready weather data processing platform** featuring RESTful APIs, interactive dashboards, and automated data parsing. Built with Django and optimized for scalability and performance.

## 🎯 Project Overview

FarmSetu Weather API is a comprehensive Django-based platform that processes UK MetOffice weather data, providing structured API access and interactive visualizations for agricultural and meteorological applications.

### 🏗️ Key Capabilities

- **Automated Data Processing**: Efficient parsing of MetOffice UK.txt format files
- **RESTful API**: Well-documented endpoints with filtering and aggregation
- **Interactive Dashboard**: Real-time charts and data visualization
- **Production Ready**: Docker containerization with CI/CD pipeline
- **Scalable Architecture**: Clean Django app structure following best practices

## ✨ Core Features

### 📊 Data Processing & Storage
- **Intelligent Parser**: Handles MetOffice UK.txt format with error handling
- **Structured Database**: SQLite for development, PostgreSQL-ready for production
- **Data Validation**: Built-in validation for weather parameters and regions
- **Custom Management Commands**: Automated data import and processing workflows

### 🔗 API Architecture
- **Django REST Framework**: Professional-grade API with serialization
- **Comprehensive Filtering**: Query by region, parameter, date ranges
- **Data Aggregation**: Yearly averages and statistical summaries
- **CORS Support**: Cross-origin requests for frontend integration
- **Admin Interface**: Django admin for data management and monitoring

### 📈 Analytics & Visualization
- **Interactive Charts**: Temperature and rainfall trend visualization
- **Responsive Design**: Mobile-first approach with Bootstrap integration
- **Real-time Updates**: Dynamic chart updates with Chart.js
- **Export Capabilities**: Data export in multiple formats
- **Historical Analysis**: Multi-year trend comparison and analysis

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Backend Framework** | Django 4.2+ | Web application framework |
| **API Layer** | Django REST Framework | RESTful API development |
| **Database** | SQLite (dev) / PostgreSQL (prod) | Data persistence |
| **Frontend** | HTML5, CSS3, Bootstrap | User interface |
| **Visualization** | Chart.js | Interactive charts and graphs |
| **Containerization** | Docker, Docker Compose | Application deployment |
| **CI/CD** | GitHub Actions | Automated testing and deployment |
| **Web Server** | Gunicorn + Nginx | Production serving |
| **Testing** | Django TestCase, Coverage.py | Quality assurance |

## 📁 Project Architecture

```
farmsetu_weather_project/
├── farmsetu_weather_project/    # Django project configuration
│   ├── __init__.py
│   ├── settings.py             # Application settings
│   ├── urls.py                 # Main URL configuration
│   └── wsgi.py                 # WSGI application
│
├── weather/                    # Core weather application
│   ├── management/commands/    # Custom Django commands
│   │   └── parse_weather_data.py  # Data parsing command
│   ├── migrations/             # Database schema migrations
│   ├── admin.py               # Django admin configuration
│   ├── models.py              # Database models (Region, Parameter, WeatherData)
│   ├── parsers.py             # MetOffice data parsing logic
│   ├── serializers.py         # API serialization layer
│   ├── views.py               # API endpoints and dashboard views
│   ├── urls.py                # Application URL routing
│   └── tests.py               # Comprehensive test suite
│
├── static/                     # Static assets (CSS, JavaScript, images)
├── templates/                  # HTML templates
│   └── weather/
│       ├── dashboard.html      # Main dashboard interface
│       └── base.html          # Base template
│
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker container definition
├── docker-compose.yml         # Multi-service Docker setup
└── manage.py                  # Django management script
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** (Python 3.11 recommended for optimal performance)
- **Git** for version control
- **Docker** (optional, for containerized deployment)

### 🏃‍♂️ Local Development

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/farmsetu-weather.git
cd farmsetu-weather

# 2. Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run database migrations
python manage.py migrate

# 5. Create superuser account
python manage.py createsuperuser

# 6. Load sample data (optional)
python manage.py loaddata weather/fixtures/initial_data.json

# 7. Start development server
python manage.py runserver
```

### 🐳 Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d --build

# View application logs
docker-compose logs -f web

# Run management commands in container
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

### 🌐 Access Points

- **Dashboard**: http://localhost:8000/dashboard/
- **API Root**: http://localhost:8000/api/
- **Admin Interface**: http://localhost:8000/admin/
- **API Documentation**: http://localhost:8000/api/docs/ (if DRF browsable API is enabled)

## 📡 API Reference

### Core Endpoints

| Endpoint | Method | Description | Parameters |
|----------|--------|-------------|------------|
| `/api/regions/` | GET | List all available regions | - |
| `/api/parameters/` | GET | List weather parameters | - |
| `/api/weather-data/` | GET | Weather data with filtering | `region`, `parameter`, `year`, `year_from`, `year_to` |
| `/api/weather-data/{id}/` | GET | Specific weather record | - |
| `/api/summary/` | GET | Yearly aggregated data | `region`, `parameter` |
| `/api/chart-data/` | GET | Formatted data for charts | `region`, `parameter`, `year_from`, `year_to` |

### Query Examples

```bash
# Get all UK temperature data for 2023
curl "http://localhost:8000/api/weather-data/?region=UK&parameter=Tmean&year=2023"

# Get rainfall data for date range
curl "http://localhost:8000/api/weather-data/?region=England&parameter=Rainfall&year_from=2020&year_to=2023"

# Get yearly temperature averages
curl "http://localhost:8000/api/summary/?region=UK&parameter=Tmean"

# Get chart-ready data for dashboard
curl "http://localhost:8000/api/chart-data/?region=UK&parameter=Rainfall&year_from=2022"
```

### Sample Response

```json
{
  "count": 156,
  "next": "http://localhost:8000/api/weather-data/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "region": "UK",
      "parameter": "Tmean",
      "year": 2023,
      "jan": 5.2,
      "feb": 6.1,
      "mar": 8.3,
      "apr": 11.7,
      "may": 15.2,
      "jun": 18.4,
      "jul": 20.8,
      "aug": 19.9,
      "sep": 16.5,
      "oct": 12.3,
      "nov": 8.7,
      "dec": 6.1,
      "ann": 12.4
    }
  ]
}
```

## 🧪 Testing & Quality

### Running Tests

```bash
# Run the complete test suite
python manage.py test weather

# Run with coverage reporting
coverage run --source='.' manage.py test weather
coverage report -m
coverage html  # Generate HTML coverage report
```

### Code Quality Standards

```bash
# Format code with Black
black .

# Lint with flake8
flake8 weather/

# Sort imports
isort weather/

# Type checking with mypy
mypy weather/
```

### Test Coverage

The project maintains comprehensive test coverage including:
- Model validation and constraints
- API endpoint functionality
- Data parsing logic
- Admin interface integration
- Error handling and edge cases

## 🚢 Production Deployment

### Environment Configuration

Create a `.env` file for production settings:

```bash
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgres://user:password@localhost:5432/farmsetu_weather
```

### Docker Production Setup

```bash
# Use production Docker Compose
docker-compose -f docker-compose.prod.yml up -d

# Apply migrations in production
docker-compose exec web python manage.py migrate

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput
```

### Recommended Production Stack

- **Application Server**: Gunicorn with multiple workers
- **Web Server**: Nginx for static files and reverse proxy
- **Database**: PostgreSQL 12+ with connection pooling
- **Caching**: Redis for session storage and caching
- **Monitoring**: Application and infrastructure monitoring
- **SSL/TLS**: HTTPS with automatic certificate renewal

## 📊 Performance Features

- **Optimized Queries**: Efficient database queries with proper indexing
- **Caching Strategy**: Template and query result caching
- **Static File Optimization**: Compressed and minified assets
- **Database Indexes**: Strategic indexing on frequently queried fields
- **Pagination**: Efficient data pagination for large datasets

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Write comprehensive tests for new features
- Update documentation for API changes
- Use meaningful commit messages
- Ensure all tests pass before submitting PR

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **MetOffice**: Weather data source
- **Django Community**: Framework and ecosystem
- **Open Source Contributors**: Libraries and tools used

---

**Built for Production • Designed for Scale • Optimized for Performance**
