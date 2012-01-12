from django.db import models
from django.utils.translation import ugettext as _

from domain.models import *

class Theme(models.Model):
    INACTIVE = 0 
    ACTIVE   = 1

    STATUS_CHOICES = ( 
        (ACTIVE,   'Active'), 
        (INACTIVE, 'Inactive'), 
    )

    code        = models.CharField(max_length=128)
    name        = models.CharField(max_length=255, null=True, blank=True)
    system      = models.CharField(max_length=128, choices=SYSTEM_CHOICES)
    image       = models.ImageField(upload_to='images/themes/', null=True, blank=True)
    description = models.TextField(max_length=255, null=True, blank=True)
    link        = models.TextField(max_length=255, null=True, blank=True)
    created     = models.DateField(auto_now_add=True)
    status      = models.IntegerField(default=ACTIVE, choices=STATUS_CHOICES)

    def __unicode__(self):
        return self.code
