from rest_framework import serializers, viewsets

from main import models

# class OptionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Option
#         fields = ['name']

# class QuestionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Question
#         fields = ['title']

# class QuizSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Quiz
#         fields = ['title']

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Option
        fields = ['name']

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = models.Question
        fields = ['title', 'options']

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = models.Quiz
        fields = ['title', 'questions']