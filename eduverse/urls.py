from django.contrib import admin
from django.urls import path
from django.urls.conf import include
#aditya admin123
urlpatterns = [
    path("admin/", admin.site.urls),
    path('courses/', include('courses.urls')),
    path('auth/', include('users.urls')),
]
