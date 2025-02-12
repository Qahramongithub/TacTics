
from rest_framework import serializers
from rest_framework.serializers import IntegerField,BooleanField
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer
from apps.models import Trainer, Comment, Student, Lesson


class TrainerSerializer(serializers.Serializer):
    position = PrimaryKeyRelatedField(
        queryset=Trainer.objects.all(),
        many=True,
    )
    experience_start = IntegerField()
    experience_end = IntegerField()
    price_start = IntegerField()
    price_end = IntegerField()
    online = BooleanField(default = False)

class CommentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'



class TrenirModelSerializer(ModelSerializer):
    class Meta:
        model = Trainer
        fields='__all__'


class StudentModelSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields='__all__'

class LessonModelSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['trainer','student', 'video', 'represenative', 'role']