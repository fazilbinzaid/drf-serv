import pytest
from mixer.backend.django import mixer
from profiles.models import CustomUser, Profile, Skillset

pytestmark = pytest.mark.django_db

class TestCustomUser:

	def test_user_model(self):
		user = mixer.blend(CustomUser, email='testy@gmail.com', password='1234')
		assert type(user) == CustomUser
		assert user.__str__() == 'testy@gmail.com'
		assert user.get_full_name() == user.name
		assert user.get_short_name() == user.name
		assert user.get_absolute_url() == 'profiles/'
		user.save()

	def test_superuser(self):
		user = CustomUser.objects.create_superuser(email='test@gmail.com',
												   password='1234')
		assert user.is_superuser


class TestProfile:

	def test_profile_model(self):
		user = mixer.blend(CustomUser, email='test@gmail.com')
		profile = mixer.blend(Profile, name='test', user=user)
		assert type(profile) == Profile
		assert profile.__str__() == 'test'
		assert profile.get_user == user.email
		profile.save()

class TestSkillset:

	def test_skillset_model(self):
		profile = mixer.blend(Profile, name='test')
		skillset = mixer.blend(Skillset, profile=profile, skill='test')
		assert skillset.profile.name == profile.name
		assert skillset.__str__() == ' : '.join([str(profile), str(skillset.skill)])
		skillset.save()

	def test_check_unique(self):
		profile = mixer.blend(Profile, name='Test')
		skillset = mixer.blend(Skillset, profile=profile, skill='test_skill')

		try:
			Skillset.objects.check_unique_together(profile=profile, skill=skillset)
		except Exception as e:
			expected_msg = 'This profile has already listed this skill.'
			assert expected_msg in e.args