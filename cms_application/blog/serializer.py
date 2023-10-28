import timeago

from datetime import datetime

from rest_framework import serializers

from django.contrib.auth.models import User
from django.utils import timezone

from blog.models import *

class BlobListSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    created_at = serializers.SerializerMethodField()

    def get_created_at(self, instance):
        return timeago.format(instance.created_at.date(), datetime.today().date())
    # comments = serializers.SerializerMethodField()

    # def get_comments(self, instance):
    #     return CommentListSerializer(instance.blog_comment.filter(is_deleted=False), many=True).data

    class Meta:
        model = Blog
        name = "blog"
        fields = (
            "id",
            "title",
            "image",
            "content",
            "created_at"
        )

class BlobSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    title = serializers.CharField(required=True)
    content = serializers.CharField(required=True)
    author = serializers.CharField(required=True)
    created_by_id = serializers.CharField(required=False)

    class Meta:
        model = Blog
        fields = (
            "id",
            "title",
            "content",
            "author",
            "created_by_id"
        )

class CommentListSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    commenter_name = serializers.CharField()
    created_at = serializers.SerializerMethodField()

    def get_created_at(self, instance):
        return timeago.format(instance.created_at.date(), datetime.today().date())
    
    class Meta:
        model = Comment
        fields = ("id", "content", "commenter_name", "created_at")

class CommentSerializer(serializers.ModelSerializer):
    content = serializers.CharField()
    commenter_name = serializers.CharField()
    blog_id = serializers.IntegerField()
    created_by_id = serializers.IntegerField()

    class Meta:
        model = Comment
        fields = ("id", "content","commenter_name", "blog_id", "created_by_id")
