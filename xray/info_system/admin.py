from django.contrib import admin
from .models import Surgeon, Patient, Endoprosthesis


@admin.register(Surgeon)
class SurgeonAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'specialization', 'phone', 'email')
    search_fields = ('last_name', 'first_name', 'specialization', 'phone', 'email')
    list_filter = ('specialization',)
    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'specialization')
        }),
        ('Контактная информация', {
            'fields': ('phone', 'email'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        'last_name',
        'first_name',
        'age_display',
        'coxarthrosis_display',
        'bmi_display',
        'surgeon'
    )
    search_fields = ('last_name', 'first_name', 'phone', 'email')
    list_filter = (
        'surgeon',
        'coxarthrosis_type',
        'coxarthrosis_grade',
        'gender',
        'has_complications'
    )
    readonly_fields = ('created_at', 'age_display', 'bmi_display')
    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'gender', 'birth_date')
        }),
        ('Антропометрия', {
            'fields': ('height', 'weight', 'bmi')
        }),
        ('Диагностика', {
            'fields': (
                'coxarthrosis_type',
                'coxarthrosis_grade',
                'preop_xray_date',
                'postop_xray_date',
                'has_complications',
                'complications_notes'
            )
        }),
        ('Контактная информация', {
            'fields': ('phone', 'email', 'surgeon'),
            'classes': ('collapse',)
        }),
    )

    def age_display(self, obj):
        return f"{obj.age} лет"

    age_display.short_description = 'Возраст'

    def coxarthrosis_display(self, obj):
        return f"{obj.get_coxarthrosis_type_display()} ({obj.get_coxarthrosis_grade_display()})"

    coxarthrosis_display.short_description = 'Коксартроз'

    def bmi_display(self, obj):
        return f"{obj.bmi:.1f}" if obj.bmi else "-"

    bmi_display.short_description = 'ИМТ'


@admin.register(Endoprosthesis)
class EndoprosthesisAdmin(admin.ModelAdmin):
    list_display = (
        'operation_date',
        'patient_info',
        'surgeon_info',
        'model_display',
        'cup_size',
        'stem_number',
        'head_size'
    )
    search_fields = (
        'patient__last_name',
        'patient__first_name',
        'surgeon__last_name',
        'surgeon__first_name',
        'model_name'
    )
    list_filter = (
        'operation_date',
        'model_name',
        'surgeon'
    )
    date_hierarchy = 'operation_date'
    fieldsets = (
        (None, {
            'fields': ('patient', 'surgeon', 'operation_date', 'model_name')
        }),
        ('Установленные параметры', {
            'fields': (
                'cup_size',
                'stem_number',
                'head_size'
            )
        }),
        ('Планируемые параметры', {
            'fields': (
                'planned_cup_size',
                'planned_stem_number',
                'planned_head_immersion'
            ),
            'classes': ('collapse',)
        }),
        ('Рентгенометрические параметры', {
            'fields': (
                'acetabular_diameter',
                'head_height',
                'femoral_offset',
                'acetabular_depth',
                'neck_shaft_angle',
                'vertical_angle',
                'wiberg_angle',
                'cup_inclination',
                'sharp_angle',
                'head_coverage'
            ),
            'classes': ('collapse',)
        }),
        ('Примечания', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )

    def patient_info(self, obj):
        return f"{obj.patient.last_name} {obj.patient.first_name}"

    patient_info.short_description = 'Пациент'

    def surgeon_info(self, obj):
        return f"{obj.surgeon.last_name} {obj.surgeon.first_name[0]}." if obj.surgeon else "-"

    surgeon_info.short_description = 'Хирург'

    def model_display(self, obj):
        return obj.model_name

    model_display.short_description = 'Модель'