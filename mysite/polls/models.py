from django.db import models
from django.contrib.auth.models import User
from datetime import date


class Venue(models.Model):
    name = models.CharField('Venue name', max_length=120)
    address = models.CharField(max_length=300)
    zip_code = models.CharField('Zip code', max_length=15)
    phone = models.CharField('Phone contact', max_length=25)
    web = models.URLField('Website address')
    email_address = models.EmailField('Email address')
    owner = models.IntegerField("Venue Owner", blank=False, default=1)
    venue_image = models.ImageField(null=True, blank=True, upload_to='images/')

    def __str__(self):
        return self.name


class SiteUser(models.Model):
    first_name = models.CharField('First name', max_length=25)
    last_name = models.CharField('Last name', max_length=25)
    email = models.EmailField('User email')

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class Event(models.Model):
    name = models.CharField('Event name', max_length=120)
    event_date = models.DateTimeField('Event date', max_length=120)
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
    manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True)
    attendees = models.ManyToManyField(SiteUser, blank=True)
    approved = models.BooleanField('Approved', default=False)

    def __str__(self):
        return self.name

    @property
    def days_till(self):
        today = date.today()
        days_till = self.event_date.date() - today
        days_till_stripped = str(days_till).split(',', 1)[0]
        return days_till_stripped

    @property
    def is_past(self):
        today = date.today()
        if self.event_date.date() > today:
            thing = True
        else:
            thing = False
        return thing
