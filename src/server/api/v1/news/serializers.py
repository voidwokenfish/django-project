from rest_framework import serializers

from server.apps.news.models import News, NewsImage


class NewsImageSerializer(serializers.ModelSerializer):

    class Meta:

        model = NewsImage
        fields = ["image"]


class NewsSerializer(serializers.ModelSerializer):

    class Meta:

        model = News
        fields = "__all__"


class NewsWriteSerializer(serializers.ModelSerializer):

    class Meta:

        model = News
        fields = ["title", "content", "preview", "notification_status", "pub_date", "is_published"]