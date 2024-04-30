from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm, AnimalForm, VetForm, AppointmentForm
from .models import Animal, Vet, Appointment

def unauthenticated_user(view_func):
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated: 
            return redirect('animal_list')
        return view_func(request, *args, **kwargs) 
    return wrapped_view

@unauthenticated_user
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@unauthenticated_user
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('create_animal')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def animal_list(request):
    animals = Animal.objects.filter(owner=request.user)
    return render(request, 'animals/animal_list.html', {'animals': animals})

@login_required
def animal_profile(request, animal_id):
    animal = get_object_or_404(Animal, id=animal_id, owner=request.user)  
    return render(request, 'animals/animal_profile.html', {'animal': animal})  

@login_required  
def create_animal_pdf(request, animal_id):
    animal = get_object_or_404(Animal, id=animal_id, owner=request.user) 
    
    response = HttpResponse(content_type='application/pdf')  
    response['Content-Disposition'] = f'attachment; filename="{animal.name}_profile.pdf"' 

    p = canvas.Canvas(response, pagesize=letter)  
    p.drawString(100, 750, f"Animal Profile: {animal.name}") 
    p.drawString(100, 730, f"Species: {animal.species}") 
    p.drawString(100, 710, f"Age: {animal.age} years")  
    p.drawString(100, 690, f"Height: {animal.height} cm") 
    p.drawString(100, 670, f"Weight: {animal.weight} kg") 
    p.drawString(100, 650, f"Medical History: {animal.medical_history}")  

    p.showPage()  
    p.save()
    
    return response  

@login_required
def create_animal(request):
    form = AnimalForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        animal = form.save(commit=False)
        animal.owner = request.user
        animal.save()
        return redirect('animal_list') 
    return render(request, 'animals/create_animal.html', {'form': form})

@login_required
def update_animal(request, animal_id):
    animal = get_object_or_404(Animal, id=animal_id, owner=request.user)
    form = AnimalForm(request.POST or None, instance=animal)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('animal_list')
    return render(request, 'animals/update_animal.html', {'form': form})

@login_required
def delete_animal(request, animal_id):
    animal = get_object_or_404(Animal, id=animal_id, owner=request.user)
    if request.method == 'POST': 
        animal.delete()
        return redirect('animal_list')
    return render(request, 'animals/delete_animal.html', {'animal': animal})

@login_required
def create_vet(request):
    form = VetForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('vet_list')  
    return render(request, 'vet/create_vet.html', {'form': form})

@login_required
def vet_list(request):
    vets = Vet.objects.all() 
    return render(request, 'vet/vet_list.html', {'vets': vets})

@login_required  
def vet_profile(request, vet_id):
    vet = get_object_or_404(Vet, id=vet_id)  
    return render(request, 'vet/vet_profile.html', {'vet': vet}) 

@login_required
def create_appointment(request):
    form = AppointmentForm(request.POST or None)  # Ініціалізація форми
    if request.method == 'POST' and form.is_valid():  # Перевірка POST-запиту
        form.save()  # Збереження нового запису
        return redirect('appointment_list')  # Перенаправлення після створення
    return render(request, 'appointment/create_appointment.html', {'form': form})  # Передача форми

@login_required
def appointment_list(request):
    appointments = Appointment.objects.filter(animal__owner=request.user)  
    return render(request, 'appointment/appointment_list.html', {'appointments': appointments})