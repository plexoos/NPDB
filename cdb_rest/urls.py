from django.urls import path, re_path
from django.urls import register_converter
from cdb_rest import converters
from cdb_rest import views
from cdb_rest.views import GlobalTagListCreationAPIView, GlobalTagDetailAPIView, GlobalTagStatusCreationAPIView, GlobalTagTypeCreationAPIView
from cdb_rest.views import PayloadListCreationAPIView, PayloadTypeListCreationAPIView, PayloadIOVListCreationAPIView, PayloadListDetailAPIView
from cdb_rest.views import PayloadIOVsListAPIView, PayloadIOVsRangesListAPIView, PayloadListDetailAPIView, PayloadIOVDetailAPIView
from cdb_rest.views import PayloadListAttachAPIView

#from cdb_rest.views import GlobalTagCreateAPIView
from cdb_rest.views import GlobalTagCloneAPIView

app_name = 'cdb_rest'

register_converter(converters.HexStringConverter, 'hex')

urlpatterns = [
    path('gt', GlobalTagListCreationAPIView.as_view(), name="global_tag"),
    path('gt/<int:pk>', GlobalTagDetailAPIView.as_view(), name="global_tag_detail"),
    path('gtstatus', GlobalTagStatusCreationAPIView.as_view(), name="global_tag_status"),
    path('gttype', GlobalTagTypeCreationAPIView.as_view(), name="global_tag_type"),

    #Create GT
    #path('globalTag/<gtType>', GlobalTagCreateAPIView.as_view(), name="create_global_tag"),
    #Clone GT
    path('globalTags/<int:sourceGlobalTagId>', GlobalTagCloneAPIView.as_view(), name="clone_global_tag"),


    path('pl', PayloadListCreationAPIView.as_view(), name="payload_list"),
    path('pl/<int:pk>', PayloadListDetailAPIView.as_view(), name="payload_list_detail"),
    path('pt', PayloadTypeListCreationAPIView.as_view(), name="payload_type"),

    path('piov', PayloadIOVListCreationAPIView.as_view(), name="payload_iov"),
    path('piov/<int:pk>', PayloadIOVDetailAPIView.as_view(), name="payload_iov_detail"),

    path('pl_attach', PayloadListAttachAPIView.as_view(), name="payload_list_attach"),


    #get GT PayloadIOVs
    #payloads gtName , runNumber , expNumber
    #path('payloadiovs/<globalTagId>/<majorIOV>/<minorIOV>', PayloadIOVsListAPIView.as_view(), name="payload_list"),
    path('payloadiovs/', PayloadIOVsListAPIView.as_view(), name="payloadiovs"),
    path('payloadiovsrange/', PayloadIOVsRangesListAPIView.as_view(), name="payload_ranges_list"),



################################################################################



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
