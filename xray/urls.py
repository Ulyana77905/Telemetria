from django.contrib import admin
from django.urls import path

from django.contrib import admin
from django.urls import path
from info_system import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),
    path('add-surgeon/', views.add_surgeon, name='add_surgeon'),
    path('add-patient/', views.add_patient, name='add_patient'),
    path('add-endoprosthesis/', views.add_endoprosthesis, name='add_endoprosthesis'),
    path('patient/<int:patient_id>/', views.patient_detail, name='patient_detail'),
]