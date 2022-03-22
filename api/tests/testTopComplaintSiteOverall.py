from django.test import TestCase
from django.urls import reverse
from api.models import Thd
from api.serializers import TopComplainSitesSerializer, TotalCaseYearSerializer
from django.db.models import Count, Sum
import pandas as pd

class TestTopComplaintSitesOverall(TestCase):
    fixtures = ['Thd.json']

    def setUp(self):
        self.response = self.client.get(reverse('thd-overall-top-complaint-site'))
        top_sites_cases = Thd.objects.exclude(siteid__isnull=True).values('siteid').alias(total_cases=Count('siteid')).order_by('-total_cases')[:10]
        self.top_complain_sites = [site['siteid'] for site in top_sites_cases]

    def testTopComplaintSites(self):     
        self.assertCountEqual(self.top_complain_sites, self.response.data['top_complain_sites'])
    
    def testTopComplaintSiteList(self):
        top_complain_sites_list = Thd.objects.values('siteid', 'clusteraddress', 'sitelong', 'sitelat').annotate(
            total_case = Count('casenumber', distinct=True)).annotate(
                total_cases_site_id = Count('casenumber')).annotate(
                    total_customer = Count('customer', distinct=True)).filter(
                        siteid__in=self.top_complain_sites).order_by('siteid')
        top_complain_sites_serializer = TopComplainSitesSerializer(top_complain_sites_list, many=True)
        
        top_complain_sites_list = pd.DataFrame(top_complain_sites_serializer.data)
        top_complain_sites_list = top_complain_sites_list.set_index(top_complain_sites_list['site_id'])
        top_complain_sites_list = top_complain_sites_list.transpose()

        top_complain_sites_list_test = pd.DataFrame(self.response.data['top_complain_sites_list'])
        top_complain_sites_list_test = top_complain_sites_list_test.set_index(top_complain_sites_list_test['site_id'])
        top_complain_sites_list_test = top_complain_sites_list_test.transpose()

        for site_id in top_complain_sites_list:
            for field in list(top_complain_sites_list.index):
                with self.subTest(item=site_id+ ' : ' +field):
                    self.assertEqual(top_complain_sites_list[site_id].loc[field], top_complain_sites_list_test[site_id].loc[field])

    def testTotalCasesByYear(self):
        total_cases_by_year = Thd.objects.values('year').annotate(total_cases=Count('casenumber'))
        total_cases_by_year_serializer = TotalCaseYearSerializer(total_cases_by_year, many=True)
        total_cases_by_year = pd.DataFrame(total_cases_by_year_serializer.data)
        total_cases_by_year = total_cases_by_year.set_index('year')
        total_cases_by_year = total_cases_by_year.transpose()

        total_cases_by_year_test = pd.DataFrame(self.response.data['total_cases_by_year'])
        total_cases_by_year_test = total_cases_by_year_test.set_index('year')
        total_cases_by_year_test = total_cases_by_year_test.transpose()

        for year in total_cases_by_year:
            with self.subTest(item=year):
                self.assertEqual(total_cases_by_year[year].loc['total_cases'], total_cases_by_year_test[year].loc['total_cases'])
    
    def testTotalComplaintSource(self):
        all_complaint_year = Thd.objects.values('casecategory', 'year').annotate(total_cases= Count('year'))
        complaint_source = Thd.objects.values('casecategory').distinct().order_by('casecategory')
        total_complaint_source = []

        for source in complaint_source:
            complaints = all_complaint_year.filter(casecategory=source['casecategory']).order_by('year')
            data = {'source': source['casecategory']}
            for complaint in complaints:
                data[str(complaint['year'])] = complaint['total_cases']
            
            total_complaint_source.append(data)

        total_complaint_source = pd.DataFrame(total_complaint_source)
        total_complaint_source = total_complaint_source.set_index(total_complaint_source['source'])
        total_complaint_source = total_complaint_source.transpose()

        total_complaint_source_test = pd.DataFrame(self.response.data['total_complaint_source'])
        total_complaint_source_test = total_complaint_source_test.set_index(total_complaint_source_test['source'])
        total_complaint_source_test = total_complaint_source_test.transpose()

        for source in total_complaint_source:
            for year in list(total_complaint_source.index):
                with self.subTest(item=source+ " : " +year):
                    self.assertEqual(total_complaint_source[source].loc[year], total_complaint_source_test[source].loc[year])

    def testTotalCasesOverall(self):
        total_cases_overall = Thd.objects.values('year').annotate(total_cases=Count('casenumber')).aggregate(Sum('total_cases'))
        self.assertEqual(total_cases_overall, self.response.data['total_cases_overall'])