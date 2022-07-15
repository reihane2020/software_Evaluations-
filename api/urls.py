"""Evaluation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'auth/', include('authentication.urls')),
    path(r'upload/', include('upload.urls')),
    path(r'setting/', include('setting.urls')),

    path(r'software/', include('software.urls')),
    path(r'metric/', include('metric_evaluation.urls')),
    path(r'comment/', include('comment_evaluation.urls')),
    path(r'rating/', include('rating_evaluation.urls')),
    path(r'compare/', include('compare_evaluation.urls')),
    path(r'questionnaire/', include('questionnaire_evaluation.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
