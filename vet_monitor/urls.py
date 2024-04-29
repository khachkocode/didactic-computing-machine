from django.contrib import admin
from django.urls import path
from monitoring import views  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create-animal/', views.create_animal, name='create_animal'),
    path('delete-animal/<int:animal_id>/', views.delete_animal, name='delete_animal'),
    path('update-animal/<int:animal_id>/', views.update_animal, name='update_animal'),
    path('animal-profile/<int:animal_id>/', views.animal_profile, name='animal_profile'),
    path('create-animal-pdf/<int:animal_id>/', views.create_animal_pdf, name='create_animal_pdf'),
    path('animal-list/', views.animal_list, name='animal_list'),
    path('create-vet/', views.create_vet, name='create_vet'), 
    path('vet-list/', views.vet_list, name='vet_list'),  
    path('vet-profile/<int:vet_id>/', views.vet_profile, name='vet_profile'), 
    path('create-appointment/', views.create_appointment, name='create_appointment'), 
    path('appointment-list/', views.appointment_list, name='appointment_list'), 

]



