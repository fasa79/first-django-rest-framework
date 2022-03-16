from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count, Min, Max, Sum
from .models import Thd
from .serializers import SiteOverallSerializer, ThdSerializer, ClusterOverallSerializer#, TotalCaseRangeSerializer

class Thd_list(generics.ListAPIView):
    queryset = Thd.objects.all()
    serializer_class = ThdSerializer

class Thd_detail(generics.RetrieveAPIView):
    queryset = Thd.objects.all()
    serializer_class = ThdSerializer

# class HeatMapOverallView(generics.ListAPIView):
#     queryset = Thd.objects.all()
#     serializer_class = ClusterOverallSerializer

#     def get_queryset(self):
#         print('start')

#         result = Thd.objects.exclude(cluster__isnull=True).values('cluster', 'clusteraddress').annotate(
#                 cluster_count = Count('cluster')
#             ).annotate(
#                 total_cases=Count('cluster')
#             ).annotate(
#                 total_complaint_sites = Count('siteid', distinct=True)
#             ).annotate(
#                 total_customer = Count('customer', distinct=True)
#             ).order_by('cluster')

#         print('end')
        
#         return result

class HeatMapOverallList(APIView):
    """
    List all heatmap.
    """
    def get(self, request, format=None):
        
        cluster = Thd.objects.exclude(cluster__isnull=True).values(
                'cluster', 'clusteraddress').annotate(
                cluster_count = Count('cluster')).annotate(
                total_cases=Count('cluster')).annotate(
                total_complaint_sites = Count('siteid', distinct=True)).annotate(
                total_customer = Count('customer', distinct=True)
            ).order_by('cluster')

        cluster_serializer = ClusterOverallSerializer(cluster, many=True)
        
        site = Thd.objects.exclude(cluster__isnull=True).values(
                'siteid', 'clusteraddress', 'sitelat', 'sitelong').annotate(
                total_cases=Count('siteid')).annotate(
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
