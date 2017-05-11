import pytest, json
from mixer.backend.django import mixer
from rest_framework.test import APIClient, APITestCase
from django.core.urlresolvers import reverse
from profiles.models import CustomUser, Profile, Skillset
from profiles.views import UserView

pytestmark = pytest.mark.django_db

class TestUserView(APITestCase):

	def test_list(self):
		user = mixer.blend(CustomUser)
		client = APIClient()
		url = reverse('profiles:users' + '-list')
		response = client.get(url)
		assert response.status_code == 200, 'user listing must happen correctly.'

		response.render()
		data = response.data
		user_letter = data[0]['email']
		assert user.email == user_letter

	def test_post(self):
		url = reverse('profiles:users' + '-list')
		data = {
			'email': 'test@gmail.com',
			'password': '1234'
		}
		client = APIClient()
		response = client.post(url, data=data, format=None)
		assert response.status_code == 201

class TestProfileListView(APITestCase):

	def setUp(self):
		self.user = mixer.blend(CustomUser)
		self.fake_user = mixer.blend(CustomUser)
		self.url = reverse('profiles:profiles' + '-list')
		self.client = APIClient()

	def test_list(self):
		profile = mixer.blend(Profile, user=self.user)
		client = self.client
		url = self.url
		client.force_authenticate(self.user)
		response = client.get(url)
		assert response.status_code == 200

		response.render()
		data = response.data
		instance_name = data[0]['name']
		assert profile.name == instance_name

	def test_post(self):
		client = self.client
		url = self.url
		data = {
			'name': 'test',
			'email': 'test@gmail.com',
			'designation': 'DevOps',
			'location': 'Kochi',
			'current_ctc': 1,
			'expected_ctc': 2,
			'notice_period': 30
		}
		client.force_authenticate(self.user)
		response = client.post(url, data, format=None)
		assert response.status_code == 201

	def test_check_incomplete_post_data(self):
		client = self.client
		url = self.url
		data = {
			'name': 'test',
			'location': 'Kochi',
			'current_ctc': 1,
		}
		client.force_authenticate(self.user)
		response = client.post(url, data, format=None)
		assert response.status_code == 400

	def test_check_multiple_user_profile_access(self):
		# Add a profile with a user.
		profile = mixer.blend(Profile, user=self.user)
		client = self.client
		url = self.url
		# login with another user
		client.force_authenticate(self.fake_user)
		# try to get the profile list
		response = client.get(url)
		# get request is legit and complete.
		assert response.status_code == 200

		response.render()
		data = response.data
		assert data == []

class TestProfileDetailView(APITestCase):

	def setUp(self):
		self.user = mixer.blend(CustomUser)
		self.namespace = 'profiles'
		self.url_name = 'profiles'
		self.client = APIClient()
		

	def test_retrieve(self):
		profile = mixer.blend(Profile, user=self.user)
		url_base = '%s:%s' % (self.namespace, self.url_name)
		url = reverse(url_base + '-detail', kwargs={'pk': profile.pk})
		client = self.client
		client.force_authenticate(self.user)
		response = client.get(url)
		assert response.status_code == 201, 'Already existing object is retrieved.'

	def test_update(self):
		profile = mixer.blend(Profile, user=self.user)
		url_base = '%s:%s' % (self.namespace, self.url_name)
		url = reverse(url_base + '-detail', kwargs={'pk': profile.pk})
		client = self.client

		update_data = {
			'id': profile.id,
			'name': 'update'
		}

		client.force_authenticate(self.user)
		response = client.put(url, update_data, format=None)
		assert response.status_code == 200

		data_fragment = response.data['name']
		assert data_fragment == 'update'

		response = client.get(url)
		response.render()
		assert response.data['name'] == data_fragment, 'get the profile once more to ensure the update.'

	def test_no_data_no_update(self):
		profile = mixer.blend(Profile, user=self.user)
		url_base = '%s:%s' % (self.namespace, self.url_name)
		url = reverse(url_base + '-detail', kwargs={'pk': profile.pk})
		client = self.client

		update_data = {
			'id': profile.id,
			'name': 'update',
			'designation': 23
		}

		client.force_authenticate(self.user)
		response = client.put(url, update_data, format=None)
		assert response.status_code == 400


	def test_delete(self):
		profile = mixer.blend(Profile, user=self.user)
		url_base = '%s:%s' % (self.namespace, self.url_name)
		url = reverse(url_base + '-detail', kwargs={'pk': profile.pk})
		client = self.client
		client.force_authenticate(self.user)
		response = client.delete(url)
		assert response.status_code == 200

		recheck_response = client.get(url)
		assert recheck_response.status_code == 404
		assert recheck_response.data['detail'] == 'Not found.'

class TestLoginView(APITestCase):

	def setUp(self):
		self.user = CustomUser.objects.create_user(email='test@gmail.com', password="1234")
		self.namespace = 'profiles'
		self.url_name = 'login'
		self.client = APIClient()
		

	def test_post(self):
		url_base = '%s:%s' % (self.namespace, self.url_name)
		url = reverse(url_base)
		post_data = {
			"email": "test@gmail.com",
			"password": "1234"
		}
		response = self.client.post(url, post_data, format='json')
		print(response.data)
		assert response.status_code == 200

	def test_no_login(self):
		url_base = '%s:%s' % (self.namespace, self.url_name)
		url = reverse(url_base)
		post_data = {
			"email": "fake@gmail.com",
			"password": "1234"
		}
		response = self.client.post(url, post_data, format='json')
		assert response.status_code == 401
		response.render()
		assert response.data['message'] == 'Username/password combination invalid.'

class TestLogoutView(APITestCase):

	def setUp(self):
		self.user = mixer.blend(CustomUser)
		self.namespace = 'profiles'
		self.url_name = 'logout'
		self.client = APIClient()

	def test_logout(self):
		url_base = '%s:%s' % (self.namespace, self.url_name)
		url = reverse(url_base)
		self.client.force_authenticate(self.user)
		response = self.client.post(url)
		assert response.status_code == 204