from django.db import models
from mandatelife.users.models import User
from .definitions import US_STATES_CHOICES


class City(models.Model):
    name = models.CharField("City Name", max_length=60)
    state = models.CharField("State", max_length=2, choices=US_STATES_CHOICES)


class ListingCategory(models.Model):
    name = models.CharField("Category", max_length=60)


class Vendor(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField()
    address = models.CharField(max_length=60)
    city = models.ForeignKey(City)
    zipcode = models.CharField(max_length=6)
    state = models.CharField(max_length=25, choices=US_STATES_CHOICES)

    phone = models.CharField(max_length=25)
    contact = models.CharField(max_length=50, blank=True, help_text="Advertising contact")
    email = models.EmailField(blank=True, help_text="Email address of contact")


class Listing (models.Model):
    category = models.CharField("Category", max_length=60)
    title = models.CharField("Title", max_length=256)
    vendor = models.ForeignKey('Vendor', help_text="Deal's offer", verbose_name="Advertiser")
    description = models.TextField()
    fine_print = models.TextField()
    city = models.ForeignKey(City)

    category = models.ForeignKey(ListingCategory)
    publish_date = models.DateTimeField()
    end_date = models.DateTimeField()

    retail_price = models.DecimalField(default=0, decimal_places=2, max_digits=6, help_text='Full price')
    deal_price = models.DecimalField(default=0, decimal_places=2, max_digits=6, help_text='Deal (real) Price')
    # store multiple num of thresholds instead of single deal value
    # (vendor sets the limit of the ‘sliding scale/tier system’)

    is_deal_active = models.BooleanField(default=False)

    latitude = models.DecimalField("Latitude (decimal)", max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField("Longitude (decimal)", max_digits=9, decimal_places=6, blank=True, null=True)

    entry_date = models.DateTimeField(blank=True, editable=False, null=True, auto_now_add=True)
    last_modified = models.DateTimeField(blank=True, editable=False, null=True, auto_now=True)
    deleted_date = models.DateTimeField(blank=True, editable=False, null=True)


class Mandate(models.Model):
    users = models.ManyToManyField(User)
    listing = models.ForeignKey(Listing)
    status = models.BooleanField(default=False)
    mandated_date = models.DateTimeField(blank=True, editable=False, null=True, auto_now_add=True)

    # Conversation field foreign field (comment model)

    entry_date = models.DateTimeField(blank=True, editable=False, null=True, auto_now_add=True)
    last_mod = models.DateTimeField(blank=True, editable=False, null=True, auto_now=True)
    deleted_date = models.DateTimeField(blank=True, editable=False, null=True)

# TODO: internal purchase model


class Profile(models.Model):
    user = models.OneToOneField(User)
    # profile image

    mandates = models.ManyToManyField(Mandate)
