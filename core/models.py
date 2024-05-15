from django.db import models
from django.utils import timezone
# Create your models here.

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


class RentU(AbstractUser):
    """ Пользователи """
    USERNAME_FIELD = 'email'
    email = models.EmailField(_('Email address'), unique=True)
    REQUIRED_FIELDS = []  # removes email from REQUIRED_FIELDS
    #ToDo подумать над языками
    CATEGORY_CHOICES = (
        ('RU', 'Русский'),
        ('EN', 'English'),)
    lang = models.CharField(_('User language'), max_length=5, blank=True, choices=CATEGORY_CHOICES,
                            default='RU',
                            null=False)


class Cars(models.Model):
    """ Автомобили """
    name_car_en = models.CharField(max_length=200, verbose_name=u"Название машины (ENG)", blank=True, null=True)
    foto = models.FileField(upload_to='foto/', verbose_name=u"фото машины", null=True, blank=True)
    born_year = models.PositiveIntegerField(verbose_name=u"Год выпуска",
                                            validators=[MinValueValidator(1900), MaxValueValidator(2999)], blank=False)
    date_create = models.DateField(verbose_name=u"Дата добавления", blank=True, null=True,
                                   default=timezone.now(), help_text='Дата добавления машины в систему')

    class Meta:
        ordering = ['name_car_en']
        verbose_name = u'Автомобиль'
        verbose_name_plural = u'Автомобили'

    def __str__(self):  # Python 3: def __str__(self):
        return self.name_car_en


class Orders(models.Model):
    """ Аренда (заказы) автомобилей"""
    renter = models.ForeignKey(RentU, null=True, verbose_name=u"Арендатор", on_delete=models.SET_NULL,
                               related_name="order")
    rented_car = models.ForeignKey(Cars, null=True, verbose_name=u"Арендованая машина", on_delete=models.SET_NULL)
    date_begin = models.DateField(verbose_name=u"Дата начала аренды", blank=True, null=True)
    date_end = models.DateField(verbose_name=u"Дата окончания аренды", blank=True, null=True)
    active = models.BooleanField(verbose_name=u"Активная аренда", default=True)

    class Meta:
        ordering = ['date_begin']
        verbose_name = u'Аренду'
        verbose_name_plural = u'Аренды автомобилей'

    def __str__(self):  # Python 3: def __str__(self):
        return self.rented_car.name_car_en + self.renter.email
