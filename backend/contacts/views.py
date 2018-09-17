from django.db import transaction, IntegrityError
from rest_framework.decorators import action

from contacts.common.api_response import api_error, api_response, api_paginated_response
from contacts.models import User
from rest_framework import viewsets, status
from contacts.serializers import UserSerializer, UserPhoneSerializer, UserEmailSerializer


class UsersViewSet(viewsets.GenericViewSet):
    """
    API endpoint that allows users to be created, viewed, edited, removed.
    """
    queryset = User.objects.all().order_by('-id')
    serializer_class = UserSerializer

    def create(self, request):
        try:
            with transaction.atomic():
                return _create_user(request)
        except IntegrityError as error:
            return api_error(message='User could not be created with received data.', errors=error.args[0])

    def destroy(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return api_error(message='User does not exist', http_code=status.HTTP_404_NOT_FOUND)

        User.delete(user)

        return api_response(message='User successfully deleted')

    @action(methods=['get'], detail=True, url_path='details', url_name='details')
    def retrieve_details(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return api_error(message='User does not exist', http_code=status.HTTP_404_NOT_FOUND)

        return api_response(data=UserSerializer(user, context={'request': request}).data)

    @action(methods=['put'], detail=True, url_path='details', url_name='details')
    def update_details(self, request, pk=None):
        """
        PUT /users/{pk}/details { phones: [{ id: 1, phone: '+12025550160' }, { id: 2, phone: '+12025550162' }] }
        """
        try:
            print('update_details')
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return api_error(message='User does not exist', http_code=status.HTTP_404_NOT_FOUND)

        return api_response(data=UserSerializer(user, context={'request': request}).data)

    def update(self, request, pk=None):
        """
        PUT /users/{pk} { first_name: 'John', last_name: 'Smith', date_of_birth: '1989-11-27Z' }
        """
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return api_error(message='User does not exist', http_code=status.HTTP_404_NOT_FOUND)

        return api_response(data=UserSerializer(user, context={'request': request}).data)

    def list(self, request):
        queryset = User.objects.all()

        return api_paginated_response(request, queryset, UserSerializer)

    def retrieve(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return api_error(message='User does not exist', http_code=status.HTTP_404_NOT_FOUND)

        return api_response(data=UserSerializer(user, context={'request': request}).data)


def _create_user(request):
    user_serializer = UserSerializer(data=request.data, context={'request': request})
    if not user_serializer.is_valid():
        return api_error(errors=user_serializer.errors, http_code=status.HTTP_400_BAD_REQUEST)

    user = user_serializer.save()
    user_phone_serializer = UserPhoneSerializer(data={
        'user': user.id,
        'phone': request.data['phone']
    })

    if not user_phone_serializer.is_valid():
        raise IntegrityError(user_phone_serializer.errors)

    user_phone_serializer.save()

    user_email_serializer = UserEmailSerializer(data={
        'user': user.id,
        'email': request.data['email']
    })

    if not user_email_serializer.is_valid():
        raise IntegrityError(user_email_serializer.errors)

    user_email_serializer.save()

    return api_response(
        message='User successfully created.',
        data=user_serializer.data,
        http_code=status.HTTP_201_CREATED
    )
