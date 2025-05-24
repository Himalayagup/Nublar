# urls.py
from nublar.urls import URLs
from .cbv_example import AboutView

urls = URLs()
urls.register("/about-cbv", AboutView)
