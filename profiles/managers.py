from django.contrib.auth.models import BaseUserManager
from django.db import models
from django.db.models import Q


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, password=password, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', True)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            if extra_fields.get('is_staff') is not True:
                raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class ProfileQuerySet(models.QuerySet):

    def filter_by_query_params(self, request):
      profiles = self
      profile_str = request.GET.get('query')

      if profile_str:
        profiles = profiles.filter(
            Q(name__icontains=profile_str.strip()) | Q(skills__skill__icontains=profile_str.strip())
            )

      return profiles

class SkillsetQueryset(models.QuerySet):

    def filter_by_query_params(self, request):
      skills = self
      skill_str = request.GET.get('query')

      if skill_str:
        skills = skills.filter(
            Q(skill__icontains=skill_str.strip()))

      return skills

    def check_unique_together(self, profile, skill):

      try:
        self.get(profile=profile, skill=skill)
        raise ValueError("This profile has already listed this skill.")
      except self.model.DoesNotExist:
        return True
