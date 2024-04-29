from django.contrib import admin
from .models import Animal, CustomUser, Appointment, Vet

admin.site.register(Animal)
admin.site.register(CustomUser)
admin.site.register(Appointment)
admin.site.register(Vet)