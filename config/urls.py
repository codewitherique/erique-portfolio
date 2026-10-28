from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("contact/", views.contact, name="contact"),
    path("projects/<slug:slug>/", views.project_detail, name="project_detail"),
    path("robots.txt", views.robots, name="robots"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
