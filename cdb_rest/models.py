from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import smart_text as smart_unicode

class GlobalTagStatus(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=80, db_column='name', unique=True)
    description = models.CharField(max_length=255, db_column='description', null=True)
    created = models.DateTimeField(auto_now_add=True, db_column='created')

    class Meta:
        db_table = u'GlobalTagStatus'

    def __str__(self):
        return smart_unicode(self.name)

    def __unicode__(self):
        return smart_unicode(self.name)

class GlobalTagType(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=80, db_column='name', unique=True)
    description = models.CharField(max_length=255, db_column='description', null=True)
    created = models.DateTimeField(auto_now_add=True, db_column='created')

    class Meta:
        db_table = u'GlobalTagType'

    def __str__(self):
        return smart_unicode(self.name)

    def __unicode__(self):
        return smart_unicode(self.name)

class GlobalTag(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=80, db_column='name', unique=True)
    description = models.CharField(max_length=255, db_column='description', null=True)
    status = models.ForeignKey(GlobalTagStatus, on_delete=models.CASCADE)
    type = models.ForeignKey(GlobalTagType, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_column='created')
    updated = models.DateTimeField(auto_now=True, db_column='updated')

    class Meta:
        db_table = u'GlobalTag'

    def __str__(self):
        return smart_unicode(self.name)

    def __unicode__(self):
        return smart_unicode(self.name)

class PayloadType(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=80, db_column='name', unique=True)
    description = models.CharField(max_length=255, db_column='description', null=True)
    created = models.DateTimeField(auto_now_add=True, db_column='created')

    class Meta:
        db_table = u'PayloadType'

    def __str__(self):
        return smart_unicode(self.name)

    def __unicode__(self):
        return smart_unicode(self.name)

class PayloadListIdSequence(models.Model):
    id = models.BigAutoField(primary_key=True)

    class Meta:
        db_table = u'PayloadListIdSequence'

    def __int__(self):
        return self.id
    def __str__(self):
        return smart_unicode(self.id)
    def __unicode__(self):
        return smart_unicode(self.id)


class PayloadList(models.Model):
    id  = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, db_column='name', unique=True)
    description = models.CharField(max_length=255, db_column='description', null=True)
    global_tag = models.ForeignKey(GlobalTag, related_name='payload_lists', on_delete=models.CASCADE)
    payload_type = models.ForeignKey(PayloadType, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_column='created')
    updated = models.DateTimeField(auto_now=True, db_column='updated')

    class Meta:
        db_table = u'PayloadList'

    def __str__(self):
        return smart_unicode(self.name)

    def __unicode__(self):
        return smart_unicode(self.name)


class PayloadIOV(models.Model):
    id = models.BigAutoField(primary_key=True)
    payload_url = models.CharField(max_length=255, db_column='payload_url')
    major_iov = models.BigIntegerField(db_column='major_iov', default=0)
    minor_iov = models.BigIntegerField(db_column='minor_iov', default=0)
    payload_list = models.ForeignKey(PayloadList, related_name='payload_iov', on_delete=models.CASCADE)
    description = models.CharField(max_length=255, db_column='description', null=True)
    created = models.DateTimeField(auto_now_add=True, db_column='created')
    updated = models.DateTimeField(auto_now=True, db_column='updated')

    class Meta:
        db_table = u'PayloadIOV'

    def __str__(self):
        return smart_unicode(self.payload_url)

    def __unicode__(self):
        return smart_unicode(self.payload_url)



