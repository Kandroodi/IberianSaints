from django.db import models
from django.contrib.gis.db import models
import datetime


# Create your models here.
from django.db.models import ForeignKey


class InstitutionType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Bibliography(models.Model):
    short_title = models.CharField(max_length=250, blank=False)
    author = models.CharField(max_length=50, blank=False)
    year = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.short_title


class Location(models.Model):
    coordinates = models.PointField(srid=4326, blank=True)


class Church(models.Model):
    name = models.CharField(max_length=100, blank=False)
    start_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField(default=datetime.date.today)
    # coordinates = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, default='')  # type: ForeignKey
    institution_type = models.ForeignKey(InstitutionType, on_delete=models.CASCADE, blank=True, default='')
    political_region = models.CharField(max_length=100, blank=True)
    ecclesiastical_region = models.CharField(max_length=100, blank=True)
    TEXTUAL = (
        ('Y', 'Yes'),
        ('N', 'No'),
    )
    textual_evidence = models.CharField(max_length=1, choices=TEXTUAL, default='Y')
    MATERIAL = (
        ('Y', 'Yes'),
        ('N', 'No'),
    )
    material_evidence = models.CharField(max_length=1, choices=MATERIAL, default='Y')
    external_link = models.URLField(max_length=128, default='', blank=True)
    bibliography = models.ForeignKey(Bibliography, on_delete=models.CASCADE, blank=True, default='')
    description = models.TextField(default='', blank=True)


class Inscription(models.Model):
    # coordinates = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, default='')
    date = models.DateField()
    institution_type = models.ForeignKey(InstitutionType, on_delete=models.CASCADE, blank=True, default='')
    text = models.TextField(max_length=256)
    description = models.TextField(default='', blank=True)
    reference = models.CharField(max_length=50)
    external_link = models.URLField(max_length=128, default='', blank=True)
    bibliography = models.ForeignKey(Bibliography, on_delete=models.CASCADE, blank=True, default='')


class SaintType(models.Model):
    name = models.CharField(max_length=100) # Just Man, Confessor, Virgin, Virgin Confessor, Apostle, etc

    def __str__(self):
        return self.name


class Saint(models.Model):
    name = models.CharField(max_length=256)
    death_date = models.DateField()
    death_place = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, default='')
    type = models.ForeignKey(SaintType, related_name='saints', on_delete=models.CASCADE, blank=True, default='')
    description = models.TextField(default='', blank=True)


class ObjectType(models.Model):
    name = models.CharField(max_length=100)  #

    def __str__(self):
        return self.name


