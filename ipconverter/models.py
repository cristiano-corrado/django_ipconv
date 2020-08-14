from django.db import models

class IPChaos(models.Model):
    string = models.CharField(max_length=16)
    type = models.CharField(max_length=50,blank=True)

    def __unicode__(self):
        return "{0} {1}".format(self.string, self.type)

class IPUnpacked(models.Model):
    ipunpack = models.CharField(max_length=50)

    def __unicode__(self):
        return "{0}".format(self.ipunpack)
