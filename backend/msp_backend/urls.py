"""
URL configuration for msp_backend project.

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
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .authentication import login, register, profile
from .views import (
    get_continents,
    get_countries,
    get_states,
    get_admin2,
    get_pandemic_data,
    download_pandemic_data_csv
)

urlpatterns = [
    path("admin/", admin.site.urls),
    
    #routes swagger pour la doc interactive
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # route for authentication simple
    path('api/auth/', include([
        path('login/', login, name='login'),
        path('register/', register, name='register'),
        path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('profile/', profile, name='profile'),
    ])),
    
    #routes pour les endpoints de données pandémiques
    path('api/', include([
        #filtres géographique
        path('continents/', get_continents, name='get_continents'),
        path('countries/', get_countries, name='get_countries'),
        path('states/', get_states, name='get_states'),
        path('admin2/', get_admin2, name='get_admin2'),
        
        #récupérer les données
        path('data/', get_pandemic_data, name='get_pandemic_data'),
        
        #télécharger les données en csv
        path('data/download/', download_pandemic_data_csv, name='download_pandemic_data_csv'),
    ])),
]
