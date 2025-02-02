from django.urls import path

from apps.views import FilterAPIView, CommentCreateApiView

urlpatterns = [
    path('filter', FilterAPIView.as_view(), name='filter'),
    path('comment',CommentCreateApiView.as_view(), name='comment'),
]
