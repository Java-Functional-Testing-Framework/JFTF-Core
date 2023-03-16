from django.urls import path, include

urlpatterns = [
    path('auth/', include('allauth.urls')),
    path('rest-auth/', include('dj_rest_auth.urls')),
]
