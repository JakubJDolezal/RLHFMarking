"""
URL configuration for RLHFMarking project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from Marking.views import response_view, score_view, question_view, home_view, question_responses_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path('responses/', response_view, name='response_view'),
    path('responses/<int:response_id>/score/', score_view, name='score_view'),
    path('ask/', question_view, name='question_view'),
    path('', home_view, name='home_view'),
    path('questions/<int:question_id>/responses/', question_responses_view, name='question_responses_view'),
]
