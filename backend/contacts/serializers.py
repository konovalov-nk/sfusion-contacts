from contacts.models import User, UserPhone, UserEmail
from rest_framework import serializers


class UserPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPhone
        fields = ('id', 'user', 'phone', 'created_at', 'updated_at')
        extra_kwargs = {
            'created_at': {'write_only': True},
            'user': {'write_only': True},
        }


class UserEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserEmail
        fields = ('id', 'user', 'email', 'created_at', 'updated_at')
        extra_kwargs = {
            'created_at': {'write_only': True},
            'user': {'write_only': True},
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'phones', 'emails', 'date_of_birth', 'updated_at', '_url')

    _url = serializers.HyperlinkedIdentityField(view_name='user-details', read_only=True)
    phones = UserPhoneSerializer(many=True, read_only=True)
    emails = UserEmailSerializer(many=True, read_only=True)

    def to_representation(self, instance):
        """
        Customizing the representation according to our specifications.
        """

        ret = super().to_representation(instance)
        ret['link'] = {
            'rel': 'self',
            'href': ret['_url'],
        }
        del ret['_url']

        return ret

    # phones = serializers.PrimaryKeyRelatedField(
    #     many=True,
    #     read_only=True,
    #     # allow_null=True,
    #     # view_name='phone-detail'
    # )
    #
    # emails = serializers.PrimaryKeyRelatedField(
    #     many=True,
    #     read_only=True,
    #     # allow_null=True,
    #     # view_name='phone-detail'
    # )
    #

