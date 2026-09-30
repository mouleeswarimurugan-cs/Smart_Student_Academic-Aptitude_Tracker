from rest_framework import serializers
from myapp.models import *





class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields="__all__"

class AssignmentSerializer(serializers.ModelSerializer):
    subject_name = serializers.SerializerMethodField()

    def get_subject_name(self, obj):
        return obj.subject.subject_name

    class Meta:
        model = Assignment
        fields="__all__"

class AptitudeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AptitudeCategory
        fields = "__all__"


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"