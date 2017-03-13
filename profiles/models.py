from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .managers import UserManager, ProfileQuerySet

# Create your models here.

CHOICES = (('Project Manager', 'Project Manager'), ('Developer', 'Developer'), ('Tester', 'Tester'),
           ('Technical Lead', 'Technical Lead'), ('Hybrid', 'Hybrid'), ('DevOps', 'DevOps'),
           ('Fresher', 'Fresher'), ('Project Coordinator', 'Project Coordinator'),( 'UI/UX Designer', 'UI/UX Designer'),
           ('UI/UX Developer', 'UI/UX Developer'), ('HTML Developer', 'HTML Developer'),)

AVAIL = (('Immediate', 'IM'), ('One Week', 'ONE'), ('Two Weeks', 'TWO'))

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_short_name(self):
        return self.name

    def get_full_name(self):
        return self.name

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return "profiles/"




class Profile(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='profiles')
    name = models.CharField(max_length=40)
    email = models.EmailField()
    designation = models.CharField(max_length=20, choices=CHOICES,)
    location = models.CharField(max_length=20,)
    current_ctc = models.DecimalField(max_digits=3, decimal_places=2,)
    expected_ctc = models.DecimalField(max_digits=3, decimal_places=2,)
    notice_period = models.IntegerField(default=30)
    # availibility = models.CharField(max_length=5, choices=AVAIL)
    resume = models.FileField(upload_to='docs/', blank=True)
    recording = models.FileField(upload_to='media/', blank=True)
    recording_optional = models.FileField(blank=True)

    objects = ProfileQuerySet.as_manager()


    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return "/profiles/%i/" % self.id


class Skillset(models.Model):
    profile = models.ForeignKey(Profile, related_name='skills')
    skill = models.CharField(max_length=10)
    exp = models.IntegerField()

    class Meta:
        unique_together = ('profile', 'skill',)

    def __str__(self):
        return ' : '.join([str(self.profile), (self.skill)])
