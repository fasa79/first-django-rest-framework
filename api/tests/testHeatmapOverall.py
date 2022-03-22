from django.test import TestCase
from django.urls import reverse
from api.models import Thd
from api.serializers import SiteOverallSerializer
from django.db.models import Count, Min, Max, Sum
import pandas as pd

class TestHeatmapOverall(TestCase):
    fixtures = ['Thd.json']

    def setUp(self):
        self.response = self.client.get(reverse('thd-overall-heat-map'))

    def testClusterOverall(self):
        cluster = ['Alur Merah', 'Batu Pahat', 'Karak', 'Kelana Jaya', 'Pasir Gudang']
        cluster_overall = Thd.objects.exclude(cluster__isnull=True).values(
                            'cluster', 'clusteraddress').annotate(
                            cluster_count = Count('cluster')).annotate(
                            total_cases=Count('casenumber', distinct=True)).annotate(
                            total_complaint_sites = Count('siteid', distinct=True)).annotate(
                            total_customer = Count('customer', distinct=True)
                            ).filter(cluster__in=cluster)
        cluster_overall = pd.DataFrame(list(cluster_overall))
        cluster_overall = cluster_overall.set_index(cluster_overall.cluster)
        cluster_overall = cluster_overall.rename(columns={'clusteraddress': 'cluster_full_address'})
        cluster_overall = cluster_overall.transpose()

        cluster_overall_test = pd.DataFrame(self.response.data['cluster_overall'])
        cluster_overall_test = cluster_overall_test.set_index(cluster_overall_test['cluster'])
        cluster_overall_test = cluster_overall_test.transpose()
        cluster_overall_test = cluster_overall_test[cluster]

        for cluster in cluster_overall:
            for field in list(cluster_overall.index):
                with self.subTest(item=cluster+ " : " +field):
                    self.assertEqual(cluster_overall[cluster].loc[field], cluster_overall_test[cluster].loc[field])

    def testSiteOverall(self):
        siteid = ['SWLKC5013', 'BL2465', 'SJ2084', 'KDLPT4023', 'CB2234', 'BS2026', 'CB4620']

        site = Thd.objects.exclude(cluster__isnull=True).values(
                'siteid', 'clusteraddress', 'sitelat', 'sitelong').annotate(
                total_cases=Count('casenumber', distinct=True)).annotate(
                cluster_count=Count('cluster')).annotate(
                total_customer=Count('customer', distinct=True)).annotate(
                total_complaint_sites=Count('siteid', distinct=True)).filter(siteid__in=siteid)
        site_serializer = SiteOverallSerializer(site, many=True)
        site_overall = pd.DataFrame(site_serializer.data)
        site_overall = site_overall.set_index(site_overall['site_id'])
        site_overall = site_overall.transpose()

        site_overall_test = pd.DataFrame(self.response.data['site_id_overall'])
        site_overall_test = site_overall_test.set_index(site_overall_test['site_id'])
        site_overall_test = site_overall_test.transpose()

        for site_id in site_overall:
            for field in list(site_overall.index):
                with self.subTest(item=site_id+ ' : ' +field):
                    self.assertEqual(site_overall[site_id].loc[field], site_overall_test[site_id].loc[field])

    def testCustomerRange(self):
        groupby_cluscus = Thd.objects.exclude(cluster__isnull=True).values('cluster').annotate(total_customer = Count('customer', distinct=True))
        min_total_customer = groupby_cluscus.aggregate(Min('total_customer'))['total_customer__min']
        max_total_customer = groupby_cluscus.aggregate(Max('total_customer'))['total_customer__max']
        self.assertEqual(min_total_customer, self.response.data['total_customer_range']['min'])
        self.assertEqual(max_total_customer, self.response.data['total_customer_range']['max'])

    def testTotalCases(self):
        groupby_cluster = Thd.objects.exclude(cluster__isnull=True).values('cluster').annotate(total_case=Count('cluster'))
        min_total_case = groupby_cluster.aggregate(Min('total_case'))['total_case__min']
        max_total_case = groupby_cluster.aggregate(Max('total_case'))['total_case__max']
        total_case_overall = groupby_cluster.aggregate(Sum('total_case'))['total_case__sum']
        self.assertEqual(min_total_case, self.response.data['total_case_range']['min'])
        self.assertEqual(max_total_case, self.response.data['total_case_range']['max'])
        self.assertEqual(total_case_overall, self.response.data['total_cases_overall'])