from django.urls import path
from WAIB3_app.views import save_entity, get_entity

urlpatterns = [
    path('api/save-entity', save_entity, name='save-entity'),
    path('api/get-entity', get_entity, name='get-entity'),
]