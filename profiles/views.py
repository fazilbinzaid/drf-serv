from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomUser, Profile
from .serializers import UserSerializer, ProfileSerializer
from .permissions import IsOwnerOrNumb
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from .authentication import CsrfExemptSessionAuthentication
from rest_framework.authentication import BasicAuthentication
from django.contrib.auth import login, logout, authenticate
import json


# Create your views here.


class UserView(APIView):
    serializer_class = UserSerializer
    # authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    lookup_field = 'email'

    def get(self, request, format=None):
        queryset = CustomUser.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    # @csrf_exempt
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            password = serializer.data['password']
            CustomUser.objects.create_user(email=email, password=password)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileListView(APIView):
    serializer_class = ProfileSerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated, )

    def get(self, request, format=None):
        queryset = Profile.objects.filter(user=self.request.user)
        serializer = ProfileSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileDetailView(APIView):
    # queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = (BasicAuthentication, )
    permission_classes = (IsAuthenticated, IsOwnerOrNumb)

    def get_object(self, pk):
        profile = Profile.objects.get(pk=pk)
        self.check_object_permissions(self.request, profile)
        return profile

    def get(self, request, pk, format=None):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, pk, format=None):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    # serializer_class = UserSerializer

    def post(self, request, format=None):
        data = json.loads(request.body.decode('utf-8'))
        email = data.get('email', None)
        password = data.get('password', None)
        account = authenticate(email=email, password=password)

        if account is not None:
            login(request, account)
            serialized = UserSerializer(account)
            return Response(serialized.data)
        else:
            return Response({
                'status': 'Unauthorized',
                'message': 'Username/password combination invalid.'
            }, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        logout(request)

        return Response({}, status=status.HTTP_204_NO_CONTENT)


