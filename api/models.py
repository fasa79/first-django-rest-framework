# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Thd(models.Model):
    thdid = models.BigIntegerField(primary_key=True, db_column='ThdID')  # Field name made lowercase.
    thdcd = models.DateTimeField(db_column='ThdCD')  # Field name made lowercase.
    uniqueid = models.BigIntegerField(db_column='uniqueID')  # Field name made lowercase.
    casenumber = models.CharField(db_column='CaseNumber', max_length=255)  # Field name made lowercase.
    customer = models.CharField(db_column='Customer', max_length=255, blank=True, null=True)  # Field name made lowercase.
    createdon = models.DateTimeField(db_column='CreatedOn')  # Field name made lowercase.
    businessunit = models.CharField(db_column='BusinessUnit', max_length=255)  # Field name made lowercase.
    packagename = models.CharField(db_column='PackageName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    subarea = models.CharField(db_column='SubArea', max_length=255)  # Field name made lowercase.
    serviceid = models.BigIntegerField(db_column='ServiceID', blank=True, null=True)  # Field name made lowercase.
    networktype = models.CharField(db_column='NetworkType', max_length=255, blank=True, null=True)  # Field name made lowercase.
    transceiverid = models.CharField(db_column='TransceiverID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    complaintaddress = models.TextField(db_column='ComplaintAddress', blank=True, null=True)  # Field name made lowercase.
    rootcause1 = models.CharField(db_column='RootCause1', max_length=255)  # Field name made lowercase.
    rootcause2 = models.CharField(db_column='RootCause2', max_length=255)  # Field name made lowercase.
    complaintlocationlatitude = models.CharField(db_column='ComplaintLocationLatitude', max_length=255, blank=True, null=True)  # Field name made lowercase.
    complaintlocationlongitude = models.FloatField(db_column='ComplaintLocationLongitude', blank=True, null=True)  # Field name made lowercase.
    region = models.CharField(db_column='Region', max_length=255, blank=True, null=True)  # Field name made lowercase.
    siteid = models.CharField(db_column='SiteID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    packagetype = models.CharField(db_column='Packagetype', max_length=255)  # Field name made lowercase.
    casetype = models.CharField(db_column='CaseType', max_length=255)  # Field name made lowercase.
    week = models.IntegerField(db_column='Week')  # Field name made lowercase.
    month = models.IntegerField(db_column='Month')  # Field name made lowercase.
    year = models.IntegerField(db_column='Year')  # Field name made lowercase.
    caseaging = models.IntegerField(db_column='CaseAging')  # Field name made lowercase.
    marphology = models.CharField(db_column='Marphology', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cluster = models.CharField(db_column='Cluster', max_length=255, blank=True, null=True)  # Field name made lowercase.
    statesite = models.CharField(db_column='StateSite', max_length=255, blank=True, null=True)  # Field name made lowercase.
    casecategory = models.CharField(db_column='CaseCategory', max_length=255)  # Field name made lowercase.
    rootcausesummarize = models.CharField(db_column='RootCauseSummarize', max_length=255)  # Field name made lowercase.
    projectsiteid = models.CharField(db_column='ProjectSiteID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    projecttype = models.CharField(db_column='Projecttype', max_length=255, blank=True, null=True)  # Field name made lowercase.
    projectstatus = models.CharField(db_column='Projectstatus', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cpmplanner = models.CharField(db_column='CPMPlanner', max_length=255, blank=True, null=True)  # Field name made lowercase.
    rfsdate = models.CharField(db_column='RFSdate', max_length=255, blank=True, null=True)  # Field name made lowercase.
    resolvedaging = models.IntegerField(db_column='ResolvedAging', blank=True, null=True)  # Field name made lowercase.
    nonrfs = models.CharField(db_column='NONRFS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    rfs = models.CharField(db_column='RFS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    aging = models.CharField(db_column='Aging', max_length=255, blank=True, null=True)  # Field name made lowercase.
    vendor = models.CharField(db_column='Vendor', max_length=255, blank=True, null=True)  # Field name made lowercase.
    siteidplanner = models.CharField(db_column='SiteIDPlanner', max_length=255, blank=True, null=True)  # Field name made lowercase.
    clusteraddress = models.TextField(db_column='ClusterAddress', blank=True, null=True)  # Field name made lowercase.
    sitelat = models.CharField(db_column='SiteLat', max_length=255, blank=True, null=True)  # Field name made lowercase.
    sitelong = models.FloatField(db_column='SiteLong', blank=True, null=True)  # Field name made lowercase.
    faultylocationlatlong = models.CharField(db_column='FaultyLocationLatlong', max_length=255, blank=True, null=True)  # Field name made lowercase.

