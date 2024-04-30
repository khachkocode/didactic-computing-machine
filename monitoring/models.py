from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
  role = models.CharField(max_length=10, choices=[("user", "User"), ("admin", "Admin")], default="user")

class Animal(models.Model):
	name = models.CharField(max_length=100)
	species = models.CharField(max_length=100)
	height = models.FloatField()
	weight = models.FloatField()
	age = models.PositiveIntegerField()
	medical_history = models.TextField(blank=True, null=True)
	owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='animals')

	def __str__(self):
			return f"{self.name} ({self.species})"
 
class Vet(models.Model):
	name = models.CharField(max_length=100)
	specialization = models.CharField(max_length=100)
	contact_info = models.CharField(max_length=255)
 
	def __str__(self):
		return f"{self.name} ({self.specialization})"

class Appointment(models.Model):
	date = models.DateTimeField()  
	reason = models.TextField()
	animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
	vet = models.ForeignKey(Vet, on_delete=models.CASCADE)