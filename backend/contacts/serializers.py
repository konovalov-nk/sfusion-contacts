from contacts.models import User
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'date_of_birth')
