from django.urls import path

from apps.views import FilterAPIView, CommentCreateApiView, TrenirListAPIView, TrenirCreateAPIView, TrenirUpdateAPIView, \
    TrenirDeleteAPIView, TrenirListPkAPIView, StudentListAPIView, StudentCreateAPIView, StudentUpdateAPIView, \
    StudentDeleteAPIView, StudentListPkAPIView, VideoUploadAPIView, VideoStreamAPIView

urlpatterns = [
    path('filter', FilterAPIView.as_view(), name='filter'),
    path('comment',CommentCreateApiView.as_view(), name='comment'),
]

urlpatterns += [
    path('trenir/list', TrenirListAPIView.as_view(), name='trenir-list'),
    path('trenir/create', TrenirCreateAPIView.as_view(), name='trenir-create '),
    path('trenir/update/<int:pk>', TrenirUpdateAPIView.as_view(), name='trenir-update '),
    path('trenir/delete/<int:pk>', TrenirDeleteAPIView.as_view(), name='trenir-delete '),
    path('trenir/list/<int:pk>', TrenirListPkAPIView.as_view(), name='trenir-listpk '),
]

urlpatterns += [
    path('student/list', StudentListAPIView.as_view(), name='student-list'),
    path('student/create', StudentCreateAPIView.as_view(), name='student-create '),
    path('student/update/<int:pk>', StudentUpdateAPIView.as_view(), name='student-update '),
    path('student/delete/<int:pk>', StudentDeleteAPIView.as_view(), name='student-delete '),
    path('student/list/<int:pk>', StudentListPkAPIView.as_view(), name='student-listpk '),
]


urlpatterns += [
    path('ap/v1/trenir/upload-video/', VideoUploadAPIView.as_view(), name='upload-video'),
    path('ap/v1/trenir/video/<int:pk>/', VideoStreamAPIView.as_view(), name='stream-video'),
]
