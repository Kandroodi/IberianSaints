from django.db import models
import datetime
from partial_date import PartialDateField

# Create your models here.
from django.db.models import ForeignKey


class InstitutionType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Bibliography(models.Model):
    short_title = models.CharField(max_length=250, blank=True, null=True)
    author = models.CharField(max_length=50, blank=True, null=True)
    year = PartialDateField(blank=True, null=True)

    def __str__(self):
        return self.short_title


class Location(models.Model):
    #     coordinates = models.PointField(srid=4326, blank=True)
    # coordinates = models.CharField(max_length=50, blank=True,
    #                                null=True)  # this is a placeholder and it will change to point field
    latitude = models.DecimalField(max_digits=9, decimal_places=7, null=True, blank=True, default='0.0')
    longitude = models.DecimalField(max_digits=9, decimal_places=7, null=True, blank=True, default='0.0')

    # def __str__(self):
    #     return 'Latitude: ' + str(round(self.latitude,7)) + ' | Longitude: ' + str(round(self.longitude,7))


class ExternalLink(models.Model):
    link = models.URLField(max_length=256, default='', blank=True)

    def __str__(self):
        return self.link


class Church(models.Model):
    name = models.CharField(max_length=100, blank=False)
    start_date = PartialDateField(blank=True, null=True)
    end_date = PartialDateField(blank=True, null=True)
    coordinates = models.ForeignKey(Location, on_delete=models.CASCADE, default='', blank=True,
                                    null=True)  # type: ForeignKey
    institution_type = models.ForeignKey(InstitutionType, on_delete=models.CASCADE, blank=True, default='', null=True)
    TEXTUAL = (
        ('Y', 'Yes'),
        ('N', 'No'),
    )
    textual_evidence = models.CharField(max_length=1, choices=TEXTUAL, default='Y', blank=True, null=True)
    MATERIAL = (
        ('Y', 'Yes'),
        ('N', 'No'),
    )
    material_evidence = models.CharField(max_length=1, choices=MATERIAL, default='Y', blank=True, null=True)
    external_link = models.ForeignKey(ExternalLink, on_delete=models.CASCADE, blank=True, default='', null=True)
    bibliography = models.ForeignKey(Bibliography, on_delete=models.CASCADE, blank=True, default='', null=True)
    description = models.TextField(default='', blank=True)

    def __str__(self):
        return self.name


class Inscription(models.Model):
    reference_no = models.CharField(max_length=100, blank=True, null=True)
    original_location = models.ForeignKey(Church, on_delete=models.SET_NULL, blank=True, default='', null=True)
    date = PartialDateField(blank=True, null=True)
    external_link = models.ForeignKey(ExternalLink, on_delete=models.SET_NULL, blank=True, default='', null=True)
    bibliography = models.ForeignKey(Bibliography, on_delete=models.SET_NULL, blank=True, default='', null=True)
    text = models.TextField(max_length=256, blank=True, null=True)
    description = models.TextField(default='', blank=True, null=True)

    def __str__(self):
        return self.reference_no


class SaintType(models.Model):
    name = models.CharField(max_length=100)  # Just Man, Confessor, Virgin, Virgin Confessor, Apostle, etc

    def __str__(self):
        return self.name


class Saint(models.Model):
    name = models.CharField(max_length=256)
    feast_day = PartialDateField(blank=True, null=True)
    death_date = PartialDateField(blank=True, null=True)
    death_place = models.CharField(max_length=256, blank=True, null=True)
    type = models.ForeignKey(SaintType, related_name='saints', on_delete=models.CASCADE, blank=True, default='',
                             null=True)
    external_link = models.ForeignKey(ExternalLink, on_delete=models.CASCADE, blank=True, default='', null=True)
    description = models.TextField(default='', blank=True, null=True)


class ObjectType(models.Model):
    name = models.CharField(max_length=100)  #

    def __str__(self):
        return self.name


class Object(models.Model):
    name = models.CharField(max_length=256)
    date = PartialDateField(blank=True, null=True)
    original_location = models.ForeignKey(Church, related_name='originallocations', on_delete=models.CASCADE,
                                          blank=True, default='', null=True)
    current_location = models.ForeignKey(Church, on_delete=models.CASCADE, blank=True, default='', null=True)
    type = models.ForeignKey(ObjectType, on_delete=models.CASCADE, blank=True, default='', null=True)
    TEXTUAL = (
        ('Y', 'Yes'),
        ('N', 'No'),
    )
    textual_evidence = models.CharField(max_length=1, choices=TEXTUAL, default='Y', blank=True, null=True)
    MATERIAL = (
        ('Y', 'Yes'),
        ('N', 'No'),
    )
    material_evidence = models.CharField(max_length=1, choices=MATERIAL, default='Y', blank=True, null=True)
    external_link = models.ForeignKey(ExternalLink, on_delete=models.CASCADE, blank=True, default='', null=True)
    bibliography = models.ForeignKey(Bibliography, on_delete=models.CASCADE, blank=True, default='', null=True)
    description = models.TextField(default='', blank=True, null=True)

    def __str__(self):
        return self.name


class ManuscriptType(models.Model):
    name = models.CharField(max_length=100)  # calendar, commicus, antiphoner, misticus, liber canticorum, etc

    def __str__(self):
        return self.name


class Rite(models.Model):
    name = models.CharField(max_length=100)  # old Hispanic, Roman

    def __str__(self):
        return self.name


class Feast(models.Model):
    name = models.CharField(max_length=100)  #
    date = PartialDateField(blank=True, null=True)

    def __str__(self):
        return self.name


class LiturgicalManuscript(models.Model):
    shelf_no = models.CharField(max_length=100)
    rite = models.ForeignKey(Rite, on_delete=models.SET_NULL, blank=True, default='', null=True)
    type = models.ForeignKey(ManuscriptType, on_delete=models.SET_NULL, blank=True, default='', null=True)
    date = PartialDateField(blank=True, null=True)
    provenance = models.ForeignKey(Church, on_delete=models.SET_NULL, blank=True, default='', null=True)
    feast = models.ForeignKey(Feast, on_delete=models.SET_NULL, blank=True, default='', null=True)
    external_link = models.ForeignKey(ExternalLink, on_delete=models.SET_NULL, blank=True, default='', null=True)
    bibliography = models.ForeignKey(Bibliography, on_delete=models.SET_NULL, blank=True, default='', null=True)
    description = models.TextField(default='', blank=True, null=True)

    # def __str__(self):
    #     return self.shelf_no


# RELATIONS
class ObjectChurchRelation(models.Model):
    object = models.ForeignKey(Object, on_delete=models.CASCADE, blank=True)
    church = models.ForeignKey(Church, on_delete=models.CASCADE, blank=True)
    start_date = PartialDateField(blank=True, null=True)
    end_date = PartialDateField(blank=True, null=True)

    def __str__(self):
        message = self.object + "and" + self.church
        return message


class LitManuscriptChurchRelation(models.Model):
    liturgical_manuscript = models.ForeignKey(LiturgicalManuscript, on_delete=models.CASCADE, blank=True, null=True)
    church = models.ForeignKey(Church, on_delete=models.CASCADE, blank=True)
    start_date = PartialDateField(blank=True, null=True)
    end_date = PartialDateField(blank=True, null=True)

    def __str__(self):
        message = self.liturgical_manuscript + "and" + self.church
        return message


class SaintChurchRelation(models.Model):
    saint = models.ForeignKey(Saint, on_delete=models.CASCADE, blank=True)
    church = models.ForeignKey(Church, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        message = self.saint + "and" + self.church
        return message


class SaintInscriptionRelation(models.Model):
    saint = models.ForeignKey(Saint, on_delete=models.CASCADE, blank=True)
    inscription = models.ForeignKey(Inscription, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        message = self.saint + "and" + self.church
        return message


class SaintObjectRelation(models.Model):
    saint = models.ForeignKey(Saint, on_delete=models.CASCADE, blank=True)
    object = models.ForeignKey(Object, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        message = self.saint + "and" + self.object
        return message


class SaintLitManuscriptRelation(models.Model):
    saint = models.ForeignKey(Saint, on_delete=models.CASCADE, blank=True)
    liturgical_manuscript = models.ForeignKey(LiturgicalManuscript, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        message = self.saint + "and" + self.liturgical_manuscript
        return message
