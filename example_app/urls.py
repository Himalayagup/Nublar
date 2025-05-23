from nublar.urls import URLs
from .cbv_example import AboutView  # Importing the AboutView class for handling the '/about' route

# Initialize the router
urls = URLs()

urls.register("/about-cbv", AboutView)