from django.urls import path, re_path
from django.urls import register_converter
from cdb_rest import converters
from cdb_rest import views

register_converter(converters.HexStringConverter, 'hex')

urlpatterns = [
    path('gtstatus/<int:pk>', views.GlobalTagStatusDetailAPIView.as_view(), name="global_tag_status_detail"),
    path('gttype/<int:pk>', views.GlobalTagTypeDetailAPIView.as_view(), name="global_tag_type_detail"),
    path('pt/<int:pk>', views.PayloadTypeDetailAPIView.as_view(), name="payload_type_detail"),

    re_path('^pils(?:/(?P<domain>\w+))?(?:/(?P<tag>\w+))?/?$', views.PayloadIntervalListAPIView.as_view()),
    path('pil', views.PayloadIntervalCreateAPIView.as_view()),
    path('pil/<hex:hexhash>', views.PayloadIntervalRetrieveAPIView.as_view()),

    path('tags', views.TagListAPIView.as_view()),
    path('tag', views.TagCreateAPIView.as_view()),
    path('tag/<str:name>', views.TagRetrieveAPIView.as_view()),
]
