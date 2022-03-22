from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Min, Max, Sum
from .models import Thd
from .serializers import *

class Thd_list(generics.ListAPIView):
    queryset = Thd.objects.all()
    serializer_class = ThdSerializer

class Thd_detail(generics.RetrieveAPIView):
    queryset = Thd.objects.all()
    serializer_class = ThdSerializer

class OverallTopComplaintSites(APIView):
    """
    Overall Top Complain Sites
    """
    def get(self, request, format=None):
        top_sites_cases = Thd.objects.exclude(siteid__isnull=True).values('siteid').alias(total_cases=Count('siteid')).order_by('-total_cases')[:10]
        top_complain_sites = [site['siteid'] for site in top_sites_cases]

        top_complain_sites_list = Thd.objects.values('siteid', 'clusteraddress', 'sitelong', 'sitelat').annotate(
            total_case = Count('casenumber', distinct=True)).annotate(
                total_cases_site_id = Count('casenumber')).annotate(
                    total_customer = Count('customer', distinct=True)).filter(
                        siteid__in=top_complain_sites).order_by('siteid')
        top_complain_sites_serializer = TopComplainSitesSerializer(top_complain_sites_list, many=True)
        
        total_cases_by_year = Thd.objects.values('year').annotate(total_cases=Count('casenumber'))
        total_cases_by_year_serializer = TotalCaseYearSerializer(total_cases_by_year, many=True)

        all_complaint_year = Thd.objects.values('casecategory', 'year').annotate(total_cases= Count('year'))
        complaint_source = Thd.objects.values('casecategory').distinct().order_by('casecategory')
        total_complaint_source = []

        for source in complaint_source:
            complaints = all_complaint_year.filter(casecategory=source['casecategory']).order_by('year')
            data = {'source': source['casecategory']}
            for complaint in complaints:
                data[str(complaint['year'])] = complaint['total_cases']
            
            total_complaint_source.append(data)

        total_cases_overall = total_cases_by_year.aggregate(Sum('total_cases'))

        response = {'status': True,
                    'top_complain_sites': top_complain_sites,
                    'top_complain_sites_list': top_complain_sites_serializer.data,
                    'total_cases_by_year': total_cases_by_year_serializer.data,
                    'total_complaint_source': total_complaint_source,
                    'total_cases_overall': total_cases_overall,
                    }

        return Response(response)

class HeatMapOverall(APIView):
    """
    List all heatmap.
    """
    def get(self, request, format=None):
        
        cluster = Thd.objects.exclude(cluster__isnull=True).values(
                    'cluster', 'clusteraddress').annotate(
                    cluster_count = Count('cluster')).annotate(
                    total_cases=Count('casenumber', distinct=True)).annotate(
                    total_complaint_sites = Count('siteid', distinct=True)).annotate(
                    total_customer = Count('customer', distinct=True)
                    ).order_by('cluster')

        cluster_serializer = ClusterOverallSerializer(cluster, many=True)
        
        site = Thd.objects.exclude(cluster__isnull=True).values(
                'siteid', 'clusteraddress', 'sitelat', 'sitelong').annotate(
                total_cases=Count('casenumber', distinct=True)).annotate(
                cluster_count=Count('cluster')).annotate(
                total_customer=Count('customer', distinct=True)).annotate(
                total_complaint_sites=Count('siteid', distinct=True)).order_by('siteid')

        site_serializer = SiteOverallSerializer(site, many=True)

        groupby_cluster = Thd.objects.exclude(cluster__isnull=True).values('cluster').annotate(total_case=Count('cluster'))
        min_total_case = groupby_cluster.aggregate(Min('total_case'))['total_case__min']
        max_total_case = groupby_cluster.aggregate(Max('total_case'))['total_case__max']
        total_case_overall = groupby_cluster.aggregate(Sum('total_case'))['total_case__sum']

        groupby_cluscus = Thd.objects.exclude(cluster__isnull=True).values('cluster').annotate(total_customer = Count('customer', distinct=True))
        min_total_customer = groupby_cluscus.aggregate(Min('total_customer'))['total_customer__min']
        max_total_customer = groupby_cluscus.aggregate(Max('total_customer'))['total_customer__max']

        response = {'status': True,
                    'cluster_overall': cluster_serializer.data,
                    'site_id_overall': site_serializer.data,
                    'total_case_range': {
                        'min': min_total_case,
                        'max': max_total_case,
                    },
                    'total_customer_range': {
                        'min': min_total_customer,
                        'max': max_total_customer,
                    },
                    'total_cases_overall': total_case_overall,
                    }

        return Response(response)
