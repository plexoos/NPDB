from rest_framework import serializers
import cdb_rest.models as model


class PayloadIntervalSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="payload_url")
    start = serializers.IntegerField(source="minor_iov")

    class Meta:
        model = model.PayloadIOV
        fields = ("name", "start")

class PayloadIntervalListSerializer(serializers.ModelSerializer):
    domain = serializers.CharField(source="payload_type.name")
    payloads = PayloadIntervalSerializer(source="payload_iov", many=True)

    class Meta:
        model = model.PayloadList
        fields = ("domain", "hexhash", "payloads")
        extra_kwargs = {'hexhash': {'required': False}}

    def calc_hash(self):
        import hashlib
        m = hashlib.sha1()
        m.update(self.data['domain'].encode())

        for d in self.data['payloads']:
            for v in d.values():
                m.update(str(v).encode())

        return m.hexdigest()

class PayloadIntervalsSerializer(serializers.ModelSerializer):
    domain = serializers.CharField(source="payload_type.name")

    class Meta:
        model = model.PayloadList
        fields = ("domain", "hexhash")

class TagSerializer(serializers.ModelSerializer):
    tag = serializers.CharField(source="name")
    pils = PayloadIntervalsSerializer(source="payload_lists", many=True)

    class Meta:
        model = model.GlobalTag
        fields = ("tag", "pils")
