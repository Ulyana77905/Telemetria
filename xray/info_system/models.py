from django.db import models
from django.utils import timezone


class Surgeon(models.Model):
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    specialization = models.CharField(max_length=100, blank=True, default="Ортопед-травматолог")
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class Patient(models.Model):
    # Типы коксартроза
    COXARTHROSIS_TYPES = [
        ('PRIMARY', 'Первичный'),
        ('DYSPLASTIC', 'Диспластический'),
        ('POSTTRAUMATIC', 'Посттравматический'),
        ('OTHER', 'Другой'),
    ]

    # Степени коксартроза (по Келлгрен-Лоуренсу)
    COXARTHROSIS_GRADES = [
        (0, '0 — Нет изменений'),
        (1, 'I — Сомнительные признаки'),
        (2, 'II — Минимальные изменения'),
        (3, 'III — Умеренные изменения'),
        (4, 'IV — Тяжёлые изменения'),
    ]

    # Пол
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birth_date = models.DateField()
    phone = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    surgeon = models.ForeignKey(Surgeon, on_delete=models.SET_NULL, null=True)

    # Антропометрия
    height = models.FloatField(verbose_name="Рост (см)", help_text="В сантиметрах")
    weight = models.FloatField(verbose_name="Вес (кг)")
    bmi = models.FloatField(verbose_name="ИМТ", editable=False)  # Авторасчёт при сохранении

    # Диагностика
    coxarthrosis_type = models.CharField(max_length=50, choices=COXARTHROSIS_TYPES, default='PRIMARY')
    coxarthrosis_grade = models.IntegerField(choices=COXARTHROSIS_GRADES, default=0)

    # Даты рентгенов
    preop_xray_date = models.DateField(verbose_name="Дата рентгена до операции", null=True, blank=True)
    postop_xray_date = models.DateField(verbose_name="Дата рентгена после операции", null=True, blank=True)

    # Осложнения
    has_complications = models.BooleanField(default=False, verbose_name="Осложнения после операции")
    complications_notes = models.TextField(blank=True)

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    def save(self, *args, **kwargs):
        # Автоматический расчёт ИМТ
        if self.height and self.weight:
            self.bmi = round(self.weight / ((self.height / 100) ** 2), 1)
        super().save(*args, **kwargs)

    @property
    def age(self):
        import datetime
        return int((datetime.date.today() - self.birth_date).days / 365.25)


class Endoprosthesis(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    surgeon = models.ForeignKey(Surgeon, on_delete=models.SET_NULL, null=True)
    operation_date = models.DateField(verbose_name="Дата операции")

    # Модель эндопротеза
    model_name = models.CharField(max_length=100, verbose_name="Модель эндопротеза")

    # Фактические параметры (после операции)
    cup_size = models.IntegerField(verbose_name="Чашка, мм (установленная)")
    stem_number = models.CharField(max_length=20, verbose_name="Ножка, номер (установленная)")
    head_size = models.IntegerField(verbose_name="Головка, мм (установленная)")

    # Планируемые параметры (до операции)
    planned_cup_size = models.IntegerField(verbose_name="Чашка, мм (планируемая)", null=True, blank=True)
    planned_stem_number = models.CharField(max_length=20, verbose_name="Ножка, номер (планируемая)", blank=True)
    planned_head_immersion = models.FloatField(verbose_name="Глубина погружения от центра вертлуги (мм)", null=True,
                                               blank=True)

    # Рентгенометрические параметры
    acetabular_diameter = models.FloatField(verbose_name="Диаметр вертлужной впадины (мм)", null=True, blank=True)
    head_height = models.FloatField(verbose_name="Высота головки (мм)", null=True, blank=True)
    femoral_offset = models.FloatField(verbose_name="Плечо бедренной кости (мм)", null=True, blank=True)
    acetabular_depth = models.FloatField(verbose_name="Глубина вертлужной впадины (мм)", null=True, blank=True)
    neck_shaft_angle = models.FloatField(verbose_name="Шеечно-диафизарный угол (°)", null=True, blank=True)
    vertical_angle = models.FloatField(verbose_name="Угол вертикального соответствия (°)", null=True, blank=True)
    wiberg_angle = models.FloatField(verbose_name="Угол Виберга (°)", null=True, blank=True)
    cup_inclination = models.FloatField(verbose_name="Угол наклона вертлужного компонента (°)", null=True, blank=True)
    sharp_angle = models.FloatField(verbose_name="Угол Шарпа (°)", null=True, blank=True)
    head_coverage = models.FloatField(verbose_name="Степень покрытия головки (%)", null=True, blank=True)

    notes = models.TextField(blank=True, verbose_name="Примечания")

    def __str__(self):
        return f'Эндопротез {self.model_name} у {self.patient}'