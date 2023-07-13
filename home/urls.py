from django.contrib import admin
from django.urls import path
from home import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.index, name='home'),
    path("about", views.about, name='about'),
    path("contact", views.contact, name='contact'),
    path("database", views.database, name='database'),
    path("verification", views.verification, name='verification'),
    path("verification2", views.verification2, name='verification2'),
    path('verification3', views.verification3, name='verification3'),
    path('final', views.final, name='final'),
    path('privacy&policy', views.privacypolicy, name='privacy&policy'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)