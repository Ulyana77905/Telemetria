from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Surgeon, Patient, Endoprosthesis
from .forms import SurgeonForm, PatientForm, EndoprosthesisForm



def dashboard(request):
    patients = Patient.objects.select_related('surgeon')
    operations = Endoprosthesis.objects.select_related('patient', 'surgeon')
    surgeons = Surgeon.objects.all()
    context = {
        'patients': patients,
        'operations': operations,
        'surgeons': surgeons,
        'Patient': Patient,
    }
    return render(request, 'info_system/dashboard.html', context)


def add_surgeon(request):
    if request.method == 'POST':
        form = SurgeonForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Хирург успешно добавлен')
        else:
            messages.error(request, 'Ошибка при добавлении хирурга')
    return redirect('dashboard')



def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Пациент успешно добавлен')
        else:
            print("Ошибки формы:", form.errors)  # <---- Добавь это
            messages.error(request, 'Ошибка при добавлении пациента')
    return redirect('dashboard')


def add_endoprosthesis(request):
    if request.method == 'POST':
        form = EndoprosthesisForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Данные об эндопротезе успешно добавлены')
        else:
            messages.error(request, 'Ошибка при добавлении данных')
    return redirect('dashboard')


@login_required
def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    operations = Endoprosthesis.objects.filter(patient=patient).order_by('-operation_date')

    context = {
        'patient': patient,
        'operations': operations,
    }
    return render(request, 'info_system/patient_detail.html', context)