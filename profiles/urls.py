from django.conf.urls import include, url
from.views import (UserView,
                   ProfileListView,
                   ProfileDetailView,
                   LoginView,
                   LogoutView,
                   )


urlpatterns = [

    url(r'^accounts/user/$', UserView.as_view(), name='users-list'),
    url(r'^accounts/profiles/$', ProfileListView.as_view(), name='profiles-list'),
    url(r'^accounts/profiles/(?P<pk>[0-9]*)/$', ProfileDetailView.as_view(), name='profiles-detail'),
    url(r'^accounts/login/$', LoginView.as_view(), name='login'),
    url(r'^accounts/logout/$', LogoutView.as_view(), name='logout'),
    url(r'^api-token-auth/', 'rest_framework_jwt.views.obtain_jwt_token'),
    url(r'^api-token-refresh/', 'rest_framework_jwt.views.refresh_jwt_token'),

]
