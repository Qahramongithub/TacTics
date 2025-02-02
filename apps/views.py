from drf_spectacular.utils import extend_schema
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from apps.models import Trainer, Comment
from apps.serializers import TrainerSerializer, CommentModelSerializer


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






