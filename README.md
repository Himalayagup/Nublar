# Nublar

Nublar is a minimalistic, Python-based web framework designed to handle both function-based views (FBVs) and class-based views (CBVs). It is built with simplicity and flexibility in mind, allowing you to create dynamic web applications with ease. Whether you prefer using function-based views or class-based views, Nublar supports both mechanisms seamlessly.

## Features

- **Function-based views (FBVs)**: Easily define routes with functions.
- **Class-based views (CBVs)**: Organize views in classes for better reusability and structure.
- **Cookie Management**: Built-in support for setting, getting, and deleting cookies.
- **URL Routing**: Handle URL routing with dynamic matching.
- **Static File Handling**: Serve static files with ease.
- **Template Rendering**: Render HTML templates using Python context data.
- **Error Handling**: Handle HTTP errors and provide custom error messages.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/nublar.git
   cd nublar
    ```

2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up your environment (if required):

   * Create a `.env` file or set environment variables like `HOST`, `PORT`, and `STATIC_FOLDER` to customize the server.

## Usage

1. **Start the server**:

   To start the server, simply run:

   ```bash
   python run.py
   ```

2. **Define Routes**:

   You can define routes using either **Function-Based Views (FBVs)** or **Class-Based Views (CBVs)**.

   ### Function-Based Views (FBVs):

   Example of defining an FBV:

   ```python
   from core.path import path
   from response.http_response import text_response

   @path("/hello")
   def hello(request, method):
       return text_response("Hello, World!")
   ```

   ### Class-Based Views (CBVs):

   Example of defining a CBV:

   ```python
   from core.views import BaseView
   from response.http_response import text_response

   class AboutView(BaseView):
       def get(self, request, **kwargs):
           return text_response("This is the about page.")
   ```

   Registering the CBV with URL routing:

   ```python
   from core.router import router

   router.register("/about", AboutView)
   ```

3. **Handling Cookies**:

   You can easily set, get, and delete cookies using the `core.cookies` utilities.

   * **Set a Cookie**:

     ```python
     from core.cookies import set_cookie

     @path("/set-cookie")
     def set_cookie_view(request, method):
         cookie_header = set_cookie("username", "JohnDoe", max_age=3600)
         response = text_response("Cookie has been set!")
         response.add_cookie(cookie_header)
         return response
     ```

   * **Get a Cookie**:

     ```python
     from core.cookies import get_cookie

     @path("/get-cookie")
     def get_cookie_view(request, method):
         username = get_cookie(request, "username")
         if username:
             return text_response(f"Hello, {username}!")
         else:
             return text_response("No username cookie found.")
     ```

   * **Delete a Cookie**:

     ```python
     from core.cookies import delete_cookie

     @path("/delete-cookie")
     def delete_cookie_view(request, method):
         cookie_header = delete_cookie("username")
         response = text_response("Cookie has been deleted.")
         response.add_cookie(cookie_header)
         return response
     ```

## File Structure

Here’s an overview of the project structure:

```
nublar/
├── app.py              # Main entry point for the application
├── core/
│   ├── __init__.py     # Package initialization
│   ├── path.py         # URL routing system (handles path matching)
│   ├── cookies.py      # Cookie utilities (set, get, delete cookies)
│   ├── views.py        # Base view classes (for CBVs)
│   ├── router.py       # URL registration and resolution
│   ├── utils.py        # Utility functions (e.g., for removing slashes)
│   └── template.py     # Template rendering system
├── response/
│   ├── __init__.py     # Package initialization
│   ├── http_response.py  # HTTP response classes (text, json, html)
│   └── status_codes.py # HTTP status codes (200 OK, 404 Not Found, etc.)
└── templates/
    └── about.html      # Sample HTML template
```

## How It Works

* **Routing**: When a request comes in, the server checks if the path matches any registered URLs. If a match is found, the corresponding view (either CBV or FBV) is called.

* **Views**: You can define views using either function-based views (decorated with `@path()`) or class-based views that extend `BaseView`. You can easily manage HTTP methods (GET, POST, etc.) within each view.

* **Cookies**: The `core.cookies` module provides functions to set, get, and delete cookies, which are then automatically added to the HTTP response.

* **Template Rendering**: Nublar allows you to render HTML templates by passing a context dictionary that will be injected into the template placeholders.

## Example Usage

Here’s an example of a simple app:

```python
# app.py
from core.path import path
from response.http_response import text_response
from core.views import BaseView
from core.router import router

# Simple FBV (Function-based View)
@path("/home")
def home(request, method):
    return text_response("Welcome to the home page!")

# Simple CBV (Class-based View)
class AboutView(BaseView):
    def get(self, request, **kwargs):
        return text_response("This is the about page.")

# Register CBV with the router
router.register("/about", AboutView)
```

## Contributing

Feel free to fork the project, make changes, and submit pull requests. Contributions are welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Made with ❤️ by Himalaya Gupta

You can find me on [LinkedIn](https://www.linkedin.com/in/himalayagupta/) and [GitHub](https://github.com/himalayagup).
