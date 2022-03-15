from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers

from django.db import transaction
from django.db.models import Q

from cdb_rest.models import GlobalTag, GlobalTagStatus, GlobalTagType, PayloadList, PayloadType, PayloadIOV, PayloadListIdSequence
from cdb_rest.serializers import GlobalTagStatusSerializer, GlobalTagTypeSerializer
from cdb_rest.serializers import PayloadListReadSerializer, PayloadTypeSerializer
from cdb_rest.serializers import PayloadIOVSerializer
from cdb_rest.serializers import PayloadListSerializer

import xpload.serializers as xpl


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


class PayloadListListCreationAPIView(ListCreateAPIView):

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



################################################################################



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


class PayloadIntervalListAPIView(ListAPIView):

    serializer_class = xpl.PayloadIntervalListSerializer

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

    serializer_class = xpl.PayloadIntervalListSerializer

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

    serializer_class = xpl.PayloadIntervalListSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            pl = PayloadList.objects.get(hexhash__istartswith=kwargs['hexhash'])
        except BaseException as e:
            return Response({"detail": f"{e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(xpl.PayloadIntervalListSerializer(pl).data)


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

        return Response(xpl.TagSerializer(pls, many=True).data)

    @transaction.atomic
    def create_entry(self, entry):
        serializer = xpl.TagSerializer(data=entry)
        serializer.is_valid(raise_exception=True)

        tag, tag_created = GlobalTag.objects.get_or_create(name=serializer.data['tag'])

        qq = functools.reduce(operator.or_, [Q(hexhash__istartswith=p['hexhash']) & Q(payload_type__name=p['domain']) for p in serializer.data['pils']])
        # TODO sort by id before distinct in order to pick latest for each domain
        pils = PayloadList.objects.filter(qq).distinct('payload_type__name').update(global_tag=tag.pk)

        return tag


class TagRetrieveAPIView(RetrieveAPIView):

    serializer_class = xpl.TagSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            inst = GlobalTag.objects.get(name=kwargs['name'])
        except BaseException as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(xpl.TagSerializer(inst).data)


import json
import numpy as np
import redis
from django.conf import settings

r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

class PayloadIOVsListAPIView(ListAPIView):

    def list(self, request):
        reqtime = int(self.request.GET.get('minorIOV'))
        b = np.array(r.lrange("b", 0, 1000)).astype(int)
        e = np.array(r.lrange("e", 0, 1000)).astype(int)
        ivals = np.column_stack((b,e))
        selected = (ivals[:, 0] <= reqtime) & (reqtime < ivals[:, 1])
        ival = ivals[selected][-1]
        return Response(json.dumps(ival.tolist()))
