from django import forms
from .models import Surgeon, Patient, Endoprosthesis
from django.core.validators import MinValueValidator, MaxValueValidator


class SurgeonForm(forms.ModelForm):
    class Meta:
        model = Surgeon
        fields = ['first_name', 'last_name', 'specialization', 'phone', 'email']


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'first_name', 'last_name', 'gender', 'birth_date',
            'phone', 'email', 'surgeon', 'height', 'weight',
            'coxarthrosis_type', 'coxarthrosis_grade',
            'preop_xray_date', 'postop_xray_date',
            'has_complications', 'complications_notes'
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'preop_xray_date': forms.DateInput(attrs={'type': 'date'}),
            'postop_xray_date': forms.DateInput(attrs={'type': 'date'}),
            'complications_notes': forms.Textarea(attrs={'rows': 3}),
        }


class EndoprosthesisForm(forms.ModelForm):
    class Meta:
        model = Endoprosthesis
        fields = '__all__'
        widgets = {
            'operation_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем валидаторы для углов
        angle_fields = [
            'neck_shaft_angle', 'vertical_angle', 'wiberg_angle',
            'cup_inclination', 'sharp_angle'
        ]
        for field in angle_fields:
            self.fields[field].widget.attrs.update({
                'step': '0.1',
                'min': '0',
                'max': '180'
            })