from rest_framework import serializers
from .models import *


class ImageSerializer(serializers.ModelSerializer):
    thumbnail = serializers.SerializerMethodField()
    medium = serializers.SerializerMethodField()
    large = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs['request']
            del kwargs['request']
        else:
            self.request = None
        super(ImageSerializer, self).__init__(*args, **kwargs)

    @staticmethod
    def build_url(self, url):
        if self.request:
            return self.request.build_absolute_uri(url)
        elif 'request' in self.context:
            return self.context['request'].build_absolute_uri(url)
        elif 'view' in self.context:
            return self.context['view'].request.build_absolute_uri(url)
        return url

    def get_thumbnail(self, obj):
        if obj.file:
            return self.build_url(self, obj.file.thumbnail.url)

    def get_medium(self, obj):
        if obj.file:
            return self.build_url(self, obj.file.medium.url)

    def get_large(self, obj):
        if obj.file:
            return self.build_url(self, obj.file.large.url)

    def get_file(self, obj):
        return self.build_url(self, obj.file.url)

    class Meta:
        model = Image
        fields = ['id', 'name', 'file', 'large', 'medium', 'thumbnail']


class FileSerializer(serializers.Serializer):
    file = serializers.FileField()

    class Meta:
        model = File
        fields = ['id', 'file', 'name']
