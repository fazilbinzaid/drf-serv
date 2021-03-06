from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers
from profiles import views


urlpatterns = [
    # Examples:
    # url(r'^$', 'Darwin.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('profiles.urls', namespace='profiles')),
    url(r'^api/auth/', include('rest_framework.urls', namespace='rest_framework')),

]
