from rest_framework import serializers


class ExchangeTokenInputSerializer(serializers.Serializer):
    subject_token = serializers.CharField()


class ExchangeTokenResponseSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    expires_in = serializers.IntegerField()
    refresh_expires_in = serializers.IntegerField()
    refresh_token = serializers.CharField()
    token_type = serializers.CharField()
    id_token = serializers.CharField()
    not_before_policy = serializers.IntegerField()
    session_state = serializers.CharField()
    scope = serializers.CharField()
