from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.utils.translation import ugettext as _

import datetime, random, hashlib

SYSTEM_CHOICES = (('drupal', 'Drupal'), ('wordpress', 'Wordpress'), ('joomla', 'Joomla'))

class UserProfile(models.Model):
    user           = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40)
    key_expires    = models.DateTimeField()

    def __unicode__(self):
        return self.user.username

class Package(models.Model):
    code        = models.CharField(max_length=128)
    system      = models.CharField(max_length=128, choices=SYSTEM_CHOICES)
    name        = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(max_length=255, null=True, blank=True)
    link        = models.TextField(max_length=255, null=True, blank=True)
    image       = models.ImageField(upload_to='images/packages/', null=True, blank=True)

    def __unicode__(self):
        return self.code

class Site(models.Model):
    # Constants 
    EXPIRED   = -3
    QUEUE     = -2
    BUILDING  = -1
    INITIAL   = 0
    ACTIVATED = 1

    STATUS_CHOICES = (
        (EXPIRED,   'Expired'), 
        (QUEUE,     'Queue'), 
        (BUILDING,  'Building'), 
        (INITIAL,   'Initial'), 
        (ACTIVATED, 'Activated')
    )

    # Fields
    name            = models.CharField(max_length=128)
    system          = models.CharField(max_length=128, choices=SYSTEM_CHOICES)
    status          = models.IntegerField(default=QUEUE, choices=STATUS_CHOICES)
    package         = models.ForeignKey(Package)
    user            = models.ForeignKey(User)
    created         = models.DateField(auto_now_add=True)
    percent         = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Build the activation key for their account
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        activation_key = hashlib.sha1(salt + instance.username).hexdigest()
        key_expires = datetime.datetime.today() + datetime.timedelta(2)
            
        # Create and save their profile
        UserProfile.objects.create(user=instance, activation_key=activation_key, key_expires=key_expires)
            
        # Send an email with the confirmation link
        '''
        email_subject = _('Your new example.com account confirmation')
        email_body = _("Hello, %s, and thanks for signing up for an \
example.com account!\n\nTo activate your account, click this link within 48 \
hours:\n\nhttp://example.com/accounts/confirm/%s") % (instance.username, activation_key)
        send_mail(email_subject, email_body, 'openweb.in.th@gmail.com', [instance.email])
        '''

post_save.connect(create_user_profile, sender=User)
