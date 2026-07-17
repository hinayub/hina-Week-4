from rest_framework import serializers

from .models import ResearchQuery


class ResearchQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchQuery
        fields = ["id", "query", "answer", "sources", "created_at"]
        read_only_fields = ["id", "answer", "sources", "created_at"]
