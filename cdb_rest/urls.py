from django.urls import path
from cdb_rest.views import GlobalTagListCreationAPIView, GlobalTagDetailAPIView, GlobalTagStatusCreationAPIView, GlobalTagTypeCreationAPIView
from cdb_rest.views import GlobalTagStatusDetailAPIView
from cdb_rest.views import GlobalTagTypeDetailAPIView
from cdb_rest.views import PayloadTypeDetailAPIView
from cdb_rest.views import PayloadListDetailAPIView
from cdb_rest.views import PayloadListListCreationAPIView, PayloadTypeListCreationAPIView, PayloadIOVListCreationAPIView
from cdb_rest.views import PayloadIOVDetailAPIView
from cdb_rest.views import PayloadIOVsListAPIView, PayloadIOVsRangesListAPIView
from cdb_rest.views import PayloadListAttachAPIView


#from cdb_rest.views import GlobalTagCreateAPIView
from cdb_rest.views import GlobalTagCloneAPIView

app_name = 'cdb_rest'

urlpatterns = [
    path('gt', GlobalTagListCreationAPIView.as_view(), name="global_tag"),
    path('gt/<int:pk>', GlobalTagDetailAPIView.as_view(), name="global_tag_detail"),
    path('gtstatus', GlobalTagStatusCreationAPIView.as_view(), name="global_tag_status"),
    path('gtstatus/<int:pk>', GlobalTagStatusDetailAPIView.as_view(), name="global_tag_status_detail"),
    path('gttype', GlobalTagTypeCreationAPIView.as_view(), name="global_tag_type"),
    path('gttype/<int:pk>', GlobalTagTypeDetailAPIView.as_view(), name="global_tag_type_detail"),

    #Create GT
    #path('globalTag/<gtType>', GlobalTagCreateAPIView.as_view(), name="create_global_tag"),
    #Clone GT
    path('globalTags/<int:sourceGlobalTagId>', GlobalTagCloneAPIView.as_view(), name="clone_global_tag"),


    path('pl', PayloadListListCreationAPIView.as_view(), name="payload_list"),
    path('pl/<int:pk>', PayloadListDetailAPIView.as_view(), name="payload_list_detail"),
    path('pt', PayloadTypeListCreationAPIView.as_view(), name="payload_type"),
    path('pt/<int:pk>', PayloadTypeDetailAPIView.as_view(), name="payload_type_detail"),

    path('piov', PayloadIOVListCreationAPIView.as_view(), name="payload_iov"),
    path('piov/<int:pk>', PayloadIOVDetailAPIView.as_view(), name="payload_iov_detail"),

    path('pl_attach', PayloadListAttachAPIView.as_view(), name="payload_list_attach"),


    #get GT PayloadIOVs
    #payloads gtName , runNumber , expNumber
    #path('payloadiovs/<globalTagId>/<majorIOV>/<minorIOV>', PayloadIOVsListAPIView.as_view(), name="payload_list"),
    path('payloadiovs/', PayloadIOVsListAPIView.as_view(), name="payload_list"),
    path('payloadiovsrange/', PayloadIOVsRangesListAPIView.as_view(), name="payload_ranges_list")

]
