from apps.models import Trainer, Comment, Lesson
import os
import re

from django.http import FileResponse
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import CreateAPIView
from rest_framework.generics import ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.models import Student
from apps.models import Trainer, Comment, Lesson
from apps.serializers import TrainerSerializer, CommentModelSerializer, LessonModelSerializer
from apps.serializers import TrenirModelSerializer, StudentModelSerializer


@extend_schema(
    request=TrainerSerializer,
    tags=['filter']
)
class FilterAPIView(APIView):
    def post(self, request):
        online = request.data['online']
        price_start = request.data['price_start']
        price_end = request.data['price_end']
        experience_start = request.data['experience_start']
        experience_end = request.data['experience_end']
        from django.db.models import Q
        trainer = Trainer.objects.filter(
            Q(price__gte=price_start) & Q(price__lte=price_end) &
            Q(experience__gte=experience_start) & Q(experience__lte=experience_end) &
            Q(online=online)
        ).all()
        serializer = TrainerSerializer(trainer, many=True)
        return Response(serializer.data)
@extend_schema(
    tags=['comment']
)
class CommentCreateApiView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentModelSerializer


# ========================================================================================================


@extend_schema(tags=['trenir'])
class TrenirListAPIView(ListAPIView):
    queryset = Trainer.objects.all()
    serializer_class = TrenirModelSerializer

@extend_schema(tags=['trenir'])
class TrenirCreateAPIView(CreateAPIView):
    queryset = Trainer.objects.all()
    serializer_class = TrenirModelSerializer


@extend_schema(tags=['trenir'])
class TrenirUpdateAPIView(UpdateAPIView):
    queryset = Trainer.objects.all()
    serializer_class = TrenirModelSerializer
    lookup_field = 'pk'


@extend_schema(tags=['trenir'])
class TrenirDeleteAPIView(DestroyAPIView):
    queryset = Trainer.objects.all()
    serializer_class = TrenirModelSerializer
    lookup_field = 'pk'


@extend_schema(tags=['trenir'])
class TrenirListPkAPIView(ListAPIView):
    queryset = Trainer.objects.all()
    serializer_class = TrenirModelSerializer

    def get_queryset(self):
        pk=self.kwargs.get('pk')
        return super().get_queryset().filter(pk=pk)



# ==================================================
@extend_schema(tags=['student'])
class StudentListAPIView(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

@extend_schema(tags=['student'])
class StudentCreateAPIView(CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer


@extend_schema(tags=['student'])
class StudentUpdateAPIView(UpdateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer
    lookup_field = 'pk'


@extend_schema(tags=['student'])
class StudentDeleteAPIView(DestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer
    lookup_field = 'pk'


@extend_schema(tags=['student'])
class StudentListPkAPIView(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    def get_queryset(self):
        pk=self.kwargs.get('pk')
        return super().get_queryset().filter(pk=pk)


# =========================================================================================================


class VideoUploadAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonModelSerializer
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VideoStreamAPIView(APIView):
    def get(self, request, pk):
        try:
            video = Lesson.objects.get(id=pk)
        except Lesson.DoesNotExist:
            raise NotFound("Video topilmadi.")

        range_header = request.headers.get('Range', None)
        video_path = video.video.path  # Agar bu `FileField` bo‘lsa, `video.path` ishlating

        if not os.path.exists(video_path):
            raise NotFound("Video fayli topilmadi.")

        if range_header:
            range_match = re.match(r"bytes=(\d+)-(\d*)", range_header)
            if range_match:
                start = int(range_match.group(1))
                end = range_match.group(2)
                end = int(end) if end else os.path.getsize(video_path) - 1

                with open(video_path, 'rb') as f:
                    f.seek(start)
                    data = f.read(end - start + 1)

                response = FileResponse(data, status=206, content_type='video/mp4')
                response['Content-Range'] = f"bytes {start}-{end}/{os.path.getsize(video_path)}"
                return response

        return FileResponse(open(video_path, 'rb'), content_type='video/mp4')


