from rest_framework import serializers
from .models import Project, ProjectImage
class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ("image", "caption", "order")
class ProjectSerializer(serializers.ModelSerializer):
    images = ProjectImageSerializer(many=True, read_only=True)
    class Meta:
        model = Project
        fields = ("title", "slug", "short_description", "description", "completed_work", "features", "result", "location", "year", "cover_image", "featured", "images")

