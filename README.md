# Nublar 🦖

Nublar 🦖 is a minimalistic, Python-based web framework designed to handle both function-based views (FBVs) and class-based views (CBVs). It is built with simplicity and flexibility in mind, allowing you to create dynamic web applications with ease.

## Quick Start

```python
# app.py
from nublar.path import path
from response.http_response import text_response

@path("/")
def home(request, method):
    return text_response("Welcome to Nublar!")

# Run the server
python mediator.py start
```

Visit `http://localhost:4000` to see your app running!

## Features

### Core Features
- **Function-based views (FBVs)**: Easily define routes with functions.
- **Cookie Management**: Built-in support for setting, getting, and deleting cookies.
- **URL Routing**: Handle URL routing with dynamic matching.
- **Static File Handling**: Serve static files with ease.
- **Template Rendering**: Render HTML templates using Python context data.
- **Error Handling**: Handle HTTP errors and provide custom error messages.
- **Request Params Handling**: Flexible routing system to handle query params, args, headers, etc.
- **CLI Option**: Offers CLI like tool to start server, run migrations etc

### Development Tools
- **Command Line Interface**: Built-in CLI for common development tasks.

## Documentation

For detailed documentation, visit our [official documentation site](http://himalayagup.github.io/Nublar/). The documentation covers:

- Getting Started Guide
- Features Overview
- API Reference
- Template System
- Database Integration
- Deployment Guide
- Function-Based Views (FBVs)
- Class-Based Views (CBVs)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Himalayagup/Nublar.git
   cd nublar
   ```

2. Create a virtual environment (recommended):

   ```bash
   # On Windows
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

## Project Structure

A typical Nublar project looks like this:

```
myproject/
├── app.py              # Main application file
├── settings.py         # Project settings
├── static/            # Static files (CSS, JS, images)
├── templates/         # HTML templates
├── myapp/            # Your application
│   ├── __init__.py
│   ├── models.py     # Database models
│   └── pages.py      # View handlers and routes
└── run.py            # Server runner
```

## Key Concepts

### 1. Views
Nublar supports both function-based and class-based views:

```python
# Function-based View
@path("/hello")
def hello(request, method):
    return text_response("Hello, World!")

# Class-based View (Under Development)
class AboutView(BaseView):
    def get(self, request, **kwargs):
        return text_response("About Us")
```

### 2. Database Models
Define your models and use migrations:

```python
from database.base import Model, CharField, IntegerField

class User(Model):
    name = CharField(max_length=100)
    age = IntegerField()
    email = CharField(max_length=255)

# Create and apply migrations
python mediator.py makemigrations myapp
python mediator.py migrate
```

### 3. Templates
Render dynamic content with templates:

```python
@path("/profile")
def profile(request, method):
    context = {
        "username": "John",
        "email": "john@example.com"
    }
    return template_response("profile.html", context)
```

## CLI Commands

Nublar provides several CLI commands to help with development:

```bash
# Start the development server
python mediator.py start

# Create a new application
python mediator.py startapp myapp

# Database migrations
python mediator.py makemigrations myapp
python mediator.py migrate

# Run with custom host and port
python mediator.py start --host=0.0.0.0 --port=8000
```

### Features Under Development
- **Class-based views (CBVs)**: Organize views in classes for better reusability and structure (Under Development).
- **Database Integration**: Simple but powerful database system with model definitions and migrations.
  - Retrieving Objects (Under Development)
  - Updating Objects (Under Development)
  - Deleting Objects (Under Development)
  - Advanced Queries (To be added)
- **Template System**:
  - Template Inheritance (To be added)
  - Template Includes (To be added)
- **Deployment Features**:
  - Monitoring and Maintenance (To be added)
  - Advanced Logging (To be added)
  - Performance Monitoring (To be added)

## Contributing

Feel free to fork the project, make changes, and submit pull requests. Contributions are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Made with ❤️ by Himalaya Gupta

You can find me on [LinkedIn](https://www.linkedin.com/in/himalayagupta/) and [GitHub](https://github.com/himalayagup).
