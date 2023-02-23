from rest_framework import serializers
from .models import Image
from django.conf import settings
from easy_thumbnails.files import get_thumbnailer



class ImageSerializer(serializers.ModelSerializer):
    thumbnails = serializers.SerializerMethodField()
    expiring_link_generator = serializers.SerializerMethodField()
    image_link = serializers.SerializerMethodField()
    image = serializers.ImageField(write_only=True)

    class Meta:
        model = Image
        fields = ['thumbnails', 'image_link', 'image', 'expiring_link_generator']


    def __init__(self, *args, **kwargs):
        self.request = kwargs['context']['request']
        super().__init__(*args, **kwargs)


    def create(self, validated_data):
        account = self.request.user.user_account
        validated_data.update({'account': account})
        obj = Image.objects.create(**validated_data)
        return obj

    def get_image_link(self, obj):
        if obj.account.account_tier.has_image_link:
            return settings.BASE_URL + f'{obj.image.url}'
        return 'Not available.'

    def get_expiring_link_generator(self, obj):
        if obj.account.account_tier.has_expiring_links:
            return settings.BASE_URL + f'/links/{obj.id}'
        return 'Not available.'


    def get_thumbnails(self, obj):
        thumbnails = {}
        sizes = obj.account.account_tier.thumbnail_sizes
        thumbnailer = get_thumbnailer(obj.image).open()
        for size in sizes:
            thumbnail = thumbnailer.get_thumbnail(thumbnail_options={'size': (0, size), 'upscale': True})
            thumbnail_url = settings.BASE_URL + thumbnail.url
            thumbnails[f'thumbnail_{size}'] = thumbnail_url

        return thumbnails


