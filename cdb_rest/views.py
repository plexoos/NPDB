from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework import serializers

from django.core import exceptions

from django.db import transaction
from django.db.models import Prefetch
from django.db.models import QuerySet
from django.db.models import Q

from cdb_rest.models import GlobalTag, GlobalTagStatus, GlobalTagType, PayloadList, PayloadType, PayloadIOV, PayloadListIdSequence
from cdb_rest.serializers import GlobalTagCreateSerializer, GlobalTagReadSerializer, GlobalTagStatusSerializer, GlobalTagTypeSerializer
from cdb_rest.serializers import PayloadListCreateSerializer, PayloadListReadSerializer, PayloadTypeSerializer
from cdb_rest.serializers import PayloadIOVSerializer
from cdb_rest.serializers import PayloadListSerializer
from cdb_rest.serializers import PayloadIntervalListSerializer
from cdb_rest.serializers import TagSerializer


class GlobalTagDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = GlobalTagReadSerializer
    queryset = GlobalTag.objects.all()

class GlobalTagStatusDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = GlobalTagStatusSerializer
    queryset = GlobalTagStatus.objects.all()

class GlobalTagTypeDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = GlobalTagTypeSerializer
    queryset = GlobalTagType.objects.all()

class PayloadTypeDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = PayloadTypeSerializer
    queryset = PayloadType.objects.all()

class PayloadListDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = PayloadListReadSerializer
    queryset = PayloadList.objects.all()

class PayloadIOVDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = PayloadIOVSerializer
    queryset = PayloadList.objects.all()

class GlobalTagListCreationAPIView(ListCreateAPIView):

    serializer_class = GlobalTagCreateSerializer

    def get_queryset(self):
        return GlobalTag.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = GlobalTagReadSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data)


class GlobalTagStatusCreationAPIView(ListCreateAPIView):

    serializer_class = GlobalTagStatusSerializer
    lookup_field = 'name'

    def get_queryset(self):
        return GlobalTagStatus.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = GlobalTagStatusSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            return Response(e.detail)

        obj, created = GlobalTagStatus.objects.get_or_create(name=serializer.data['name'])

        return Response(GlobalTagStatusSerializer(obj).data)


class GlobalTagTypeCreationAPIView(ListCreateAPIView):

    serializer_class = GlobalTagTypeSerializer

    def get_queryset(self):
        return GlobalTagType.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = GlobalTagTypeSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            return Response(e.detail)

        obj, created = GlobalTagType.objects.get_or_create(name=serializer.data['name'])

        return Response(GlobalTagTypeSerializer(obj).data)


class PayloadListCreationAPIView(ListCreateAPIView):

    serializer_class = PayloadListSerializer

    def get_next_id(self):
        return PayloadListIdSequence.objects.create()

    def get_queryset(self):
        return PayloadList.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = PayloadListReadSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            return Response(e.detail)

        pt = PayloadType.objects.get(pk=serializer.data['payload_type'])
        gt = GlobalTag.objects.get(pk=serializer.data['global_tag'])

        obj, created = PayloadList.objects.get_or_create(global_tag=gt, payload_type=pt, defaults={'name': f'{gt.name}_{pt.name}'})

        return Response(PayloadListSerializer(obj).data)


class PayloadTypeListCreationAPIView(ListCreateAPIView):

    serializer_class = PayloadTypeSerializer

    def get_queryset(self):
        return PayloadType.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = PayloadTypeSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            return Response(e.detail)

        obj, created = PayloadType.objects.get_or_create(name=serializer.data['name'])

        return Response(PayloadTypeSerializer(obj).data)


class PayloadIOVListCreationAPIView(ListCreateAPIView):

    serializer_class = PayloadIOVSerializer

    def get_queryset(self):
        return PayloadIOV.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = PayloadIOVSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data
        pList = PayloadList.objects.get(pk=data['payload_list'])

        #Check if PL is attached and unlocked
        if pList.global_tag:
            if pList.global_tag.status_id == 'locked':
                return Response({"detail": "Global Tag is locked."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = self.get_serializer(data=data)

        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            return Response(e.detail)

        defaults = {'minor_iov': serializer.data['minor_iov']}
        obj, created = PayloadIOV.objects.get_or_create(payload_url=serializer.data['payload_url'], payload_list=pList, defaults=defaults)

        return Response(PayloadIOVSerializer(obj).data)


class PayloadIntervalListAPIView(ListAPIView):

    serializer_class = PayloadIntervalListSerializer

    def get_queryset(self, **kwargs):
        # Define an always-true Q object
        qq = ~Q(pk__in=[])

        if 'domain' in self.kwargs and self.kwargs['domain'] != "_":
            qq = Q(payload_type__name=self.kwargs['domain'])

        if 'tag' in self.kwargs:
            qq = qq & Q(global_tag__name=self.kwargs['tag'])

        if qq:
            return PayloadList.objects.filter(qq)
        else:
            return PayloadList.objects.all()


class PayloadIntervalCreateAPIView(CreateAPIView):

    serializer_class = PayloadIntervalListSerializer

    def get_queryset(self):
        return PayloadList.objects.all()

    def create(self, request, *args, **kwargs):
        # Transform to a list
        entries = request.data if isinstance(request.data, list) else [request.data]

        pls = []
        for entry in entries:
            try:
                pl = self.create_entry(entry)
            except serializers.ValidationError as e:
                return Response(e.detail)

            pls.append(pl)

        if len(pls) > 10: pls = pls[0:10]

        return Response(PayloadListSerializer(pls, many=True).data)

    @transaction.atomic
    def create_entry(self, entry):
        serializer = self.get_serializer(data=entry)

        serializer.is_valid(raise_exception=True)

        pt, pt_created = PayloadType.objects.get_or_create(name=serializer.data['domain'])
        pl, pl_created = PayloadList.objects.get_or_create(hexhash=serializer.calc_hash(), defaults=dict(payload_type=pt))

        if pl_created:
            payloads = [PayloadIOV(**p, payload_list=pl) for p in serializer.validated_data['payload_iov']]
            PayloadIOV.objects.bulk_create(payloads)

        return pl


class PayloadIntervalRetrieveAPIView(RetrieveAPIView):

    serializer_class = PayloadIntervalListSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            pl = PayloadList.objects.get(hexhash__istartswith=kwargs['hexhash'])
        except BaseException as e:
            return Response({"detail": f"{e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(PayloadIntervalListSerializer(pl).data)


class TagListAPIView(ListAPIView):

    def list(self, request):
        return Response(GlobalTag.objects.values_list('name', flat=True))


import operator
import functools

class TagCreateAPIView(CreateAPIView):

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        # Transform to a list
        entries = request.data if isinstance(request.data, list) else [request.data]

        pls = []
        for entry in entries:
            try:
                pl = self.create_entry(entry)
            except serializers.ValidationError as e:
                return Response(e.detail)

            pls.append(pl)

        if len(pls) > 10: pls = pls[0:10]

        return Response(TagSerializer(pls, many=True).data)

    @transaction.atomic
    def create_entry(self, entry):
        serializer = TagSerializer(data=entry)
        serializer.is_valid(raise_exception=True)

        tag, tag_created = GlobalTag.objects.get_or_create(name=serializer.data['tag'])

        qq = functools.reduce(operator.or_, [Q(hexhash__istartswith=p['hexhash']) & Q(payload_type__name=p['domain']) for p in serializer.data['pils']])
        # TODO sort by id before distinct in order to pick latest for each domain
        pils = PayloadList.objects.filter(qq).distinct('payload_type__name').update(global_tag=tag.pk)

        return tag


class TagRetrieveAPIView(RetrieveAPIView):

    serializer_class = TagSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            inst = GlobalTag.objects.get(name=kwargs['name'])
        except BaseException as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(TagSerializer(inst).data)


#API to create GT. GT provided as JSON body
#class GlobalTagCreateAPIView(CreateAPIView):
#
#    serializer_class = GlobalTagCreateSerializer
#
#    def create(self, request, *args, **kwargs):
#        serializer = self.get_serializer(data=request.data)
#        serializer.is_valid(raise_exception=True)
#
#        #TODO name check
#
#        self.perform_create(serializer)
#
#        return Response(serializer.data)


#GT deep copy endpoint

class GlobalTagCloneAPIView(CreateAPIView):

    serializer_class = GlobalTagReadSerializer

    def get_globalTag(self):
        sourceGlobalTagId = self.kwargs.get('sourceGlobalTagId')
        return GlobalTag.objects.get(pk = sourceGlobalTagId)

    def get_payloadLists(self, globalTag):
        return PayloadList.objects.filter(global_tag=globalTag)

    def get_payloadIOVs(self, payloadList):
        return PayloadIOV.objects.filter(payload_list=payloadList)

    @transaction.atomic
    def create(self, request, sourceGlobalTagId):
        globalTag = self.get_globalTag()
        payloadLists = self.get_payloadLists(globalTag)

        globalTag.id = None
        globalTag.name = 'COPY_OF_'+ globalTag.name
        self.perform_create(globalTag)

        for pList in payloadLists:
            payloadIOVs = self.get_payloadIOVs(pList)
            pList.id = None
            pList.global_tag = globalTag
            self.perform_create(pList)
            rp = []
            for payload in payloadIOVs:
                payload.id = None
                payload.payload_list = pList
                rp.append(payload)

            PayloadIOV.objects.bulk_create(rp)

        serializer = GlobalTagReadSerializer(globalTag)

        return Response(serializer.data)


#Interface to take list of PayloadIOVs groupped by PayloadLists for a given GT and IOVs
class PayloadIOVsListAPIView(ListAPIView):

        def get_queryset(self):

            gtName = self.request.GET.get('gtName')
            majorIOV = self.request.GET.get('majorIOV')
            minorIOV = self.request.GET.get('minorIOV')

            #return PayloadIOV.objects.filter(payload_list__global_tag__name=gtName, major_iov__lte = majorIOV,minor_iov__lte=minorIOV).order_by('payload_list_id','-major_iov','-minor_iov').distinct('payload_list_id')
            piovs = PayloadIOV.objects.filter(payload_list__global_tag__name=gtName, major_iov__lte = majorIOV,minor_iov__lte=minorIOV).order_by('payload_list_id','-major_iov','-minor_iov').distinct('payload_list_id').values_list('id',flat=True)
            piov_ids = list(piovs)
            piov_querset = PayloadIOV.objects.filter(id__in=piov_ids)

            return PayloadList.objects.filter(global_tag__name=gtName).prefetch_related(Prefetch(
                  'payload_iov',
                  queryset=piov_querset
                  )).filter(payload_iov__in=piov_querset).distinct()

        def list(self, request):

            queryset = self.get_queryset()
            serializer = PayloadIntervalListSerializer(queryset, many=True)
            return Response(serializer.data)


#Interface to take list of PayloadIOVs ranges groupped by PayloadLists for a given GT and IOVs
class PayloadIOVsRangesListAPIView(ListAPIView):

        def get_queryset(self):

            gtName = self.request.GET.get('gtName')
            startMajorIOV = self.request.GET.get('startMajorIOV')
            startMinorIOV = self.request.GET.get('startMinorIOV')
            endMajorIOV = self.request.GET.get('endMajorIOV')
            endMinorIOV = self.request.GET.get('endMinorIOV')

            #TODO:handle endIOVs -1 -1
            q = {'major_iov__gte': startMajorIOV, 'minor_iov__gte': startMinorIOV}
            if endMajorIOV != '-1':
                q.update({'major_iov__lte': endMajorIOV})
            if endMinorIOV != '-1':
                q.update({'minor_iov__lte': endMinorIOV})

            #plists = PayloadList.objects.filter(global_tag__id=globalTagId)
            plists = PayloadList.objects.filter(global_tag__name=gtName)
            piov_ids = []
            for pl in plists:

                #piovs = PayloadIOV.objects.filter(payload_list = pl, major_iov__lte = endMajorIOV,minor_iov__lte=endMinorIOV,
                #                                  major_iov__gte = startMajorIOV,minor_iov__gte=startMinorIOV).values_list('id', flat=True)
                q.update({'payload_list': pl})
                piovs = PayloadIOV.objects.filter(**q).values_list('id', flat=True)

                if piovs:
                    piov_ids.extend(piovs)

            piov_querset = PayloadIOV.objects.filter(id__in=piov_ids)

            return PayloadList.objects.filter(global_tag__name=gtName).prefetch_related(Prefetch(
                  'payload_iov',
                  queryset=piov_querset
                  )).filter(payload_iov__in=piov_querset).distinct()


        def list(self, request):

            queryset = self.get_queryset()
            serializer = PayloadListReadSerializer(queryset, many=True)
            return Response(serializer.data)


class PayloadListAttachAPIView(UpdateAPIView):

    serializer_class = PayloadListCreateSerializer

    @transaction.atomic
    def put(self, request, *args, **kwargs):

        data = request.data

        try:
            pList = PayloadList.objects.get(name=data['payload_list'])
        except:
            return Response({"detail": "PayloadList not found."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        try:
            gTag = GlobalTag.objects.get(name=data['global_tag'])
        except:
            return Response({"detail": "GlobalTag not found."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        try:
            plType = PayloadType.objects.get(name=data['payload_type'])
        except:
            return Response({"detail": "PayloadListType not found."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        #check if GT is unlocked
        if gTag.status_id == 'locked' :
            return Response({"detail": "Global Tag is locked."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        #check if the PayloadList of the same type is already attached. If yes then detach
        PayloadList.objects.filter(global_tag=gTag, payload_type=plType).update(global_tag=None)
        #gTag = GlobalTag.objects.get(name=data['global_tag'])
        pList.global_tag = gTag

        #print(serializer)
        #serializer.is_valid(raise_exception=True)
        self.perform_update(pList)

        #Update time for the GT
        self.perform_update(gTag)

        serializer = PayloadListSerializer(pList)
        #print(serializer.data['global_tag'])
        #json = JSONRenderer().render(serializer.data)
        ret = serializer.data
        ret['global_tag'] = gTag.name

        #serializer.data['global_tag'] = gTag.name
        return Response(ret)
