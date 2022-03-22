from rest_framework import serializers
from .models import Thd
from django.db.models import Count, Max, Min

class ThdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thd
        fields = '__all__'

class ClusterOverallSerializer(serializers.Serializer):
    cluster = serializers.CharField(read_only=True)
    cluster_count = serializers.IntegerField(read_only=True)
    cluster_full_address = serializers.CharField(source='clusteraddress', read_only=True)
    total_customer = serializers.IntegerField(read_only=True)
    total_cases = serializers.IntegerField(read_only=True)
    total_complaint_sites = serializers.IntegerField(read_only=True)

class SiteOverallSerializer(serializers.Serializer):
    site_id = serializers.CharField(source='siteid', read_only=True)
    cluster_count = serializers.IntegerField(read_only=True)
    cluster_full_address = serializers.CharField(source='clusteraddress', read_only=True)
    total_customer = serializers.IntegerField(read_only=True)
    total_cases = serializers.IntegerField(read_only=True)
    total_complaint_sites = serializers.IntegerField(read_only=True)
    latitude = serializers.CharField(source='sitelat', read_only=True)
    longitude = serializers.CharField(source='sitelong', read_only=True)

class TopComplainSitesSerializer(serializers.Serializer):
    site_id = serializers.CharField(source='siteid', read_only=True)
    total_cases_site_id = serializers.IntegerField(read_only=True)
    cluster = serializers.CharField(source='clusteraddress', read_only=True)
    total_customer = serializers.IntegerField(read_only=True)
    total_case = serializers.IntegerField(read_only=True)
    longitude_latitude = serializers.SerializerMethodField()

    def get_longitude_latitude(self, obj):
        return str(obj['sitelong']) + "," + str(obj['sitelat'])

class TotalCaseYearSerializer(serializers.Serializer):
    year = serializers.IntegerField(read_only=True)
    total_cases = serializers.IntegerField(read_only=True)

