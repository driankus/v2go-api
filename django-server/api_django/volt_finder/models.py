import datetime
import hashlib 

# from django.db import models
from django.contrib.gis.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import AbstractUser
from django.contrib.gis.geos import GEOSGeometry, fromstr

class User(AbstractUser):
    pass

class ChargingStation(models.Model):
    """ Charging station data model """
    #TODO move const declaratios  (status, charge_level) to a dif file
    AVAILABLE       = 'AVAILABLE'
    RESERVED        = 'RESERVED'
    UNAVAILABLE     = 'UNAVAILABLE'
    OUTOFSERVICE    = 'OUT_OF_SERVICE'
    LEVEL_1         = 'LEVEL_1'
    LEVEL_2         = 'LEVEL_2'
    FASTDC          = 'FAST_DC'

    STATUSES = (
        (AVAILABLE, AVAILABLE),
        (RESERVED, RESERVED),
        (UNAVAILABLE, UNAVAILABLE),
        (OUTOFSERVICE, OUTOFSERVICE),
    )

    nk           = models.CharField(max_length=32, unique=True, db_index=True)
    name         = models.CharField(max_length=255, blank=True)
    external_id  = models.CharField(max_length=100, blank=True)
    CHARGE_LEVEL = (
        (LEVEL_1, LEVEL_1),
        (LEVEL_2, LEVEL_2),
        (FASTDC, FASTDC),
    )
    charge_level = models.CharField(max_length=32, choices=CHARGE_LEVEL, default=LEVEL_2)
    tarif_text   = models.CharField(max_length=100, blank=True)

    #TODO: this should be a foreign key to link with cs_owner model
    # manager_id   = models.IntegerField()

    address      = models.CharField(max_length=150) 
    location     = models.CharField(max_length=150, default='') 
    city         = models.CharField(max_length=50, blank=True)
    province     = models.CharField(max_length=50, blank=True)
    country      = models.CharField(max_length=50, blank=True)
    postal_code  = models.CharField(max_length=10, blank=True)

    #TODO: lat,lng should be mandatory (blank=False) before pushing to production
    lat          = models.FloatField(null=True, blank=True) 
    lng          = models.FloatField(null=True, blank=True) 
    
    #TODO create geo_Location from lat lng using method
    geo_location = models.PointField()    #null=True, blank=True

    created      = models.DateTimeField(auto_now_add=True)
    updated      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nk

    def get_absolute_url(self):
        return reverse('cStation:cStation_detail', kwargs={'cStation_nk': self.nk})
    
    def create_geo_location(self):
        self.geo_location = fromstr(f'POINT({self.lng} {self.lat})', srid=4326)

    def save(self, **kwargs):
        if not self.nk:
            now = datetime.datetime.now()
            secure_hash = hashlib.md5()
            secure_hash.update(
                #TODO  add :{self.owner} OR owner_nk OR owner foreign key
                f'{now}:{self.address}'.encode(
                    'utf-8'))
            self.nk = secure_hash.hexdigest()
        if not self.geo_location:
            self.create_geo_location()
        super().save(**kwargs)
    
