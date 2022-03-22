import requests
import pandas as pd
import sqlalchemy as db
import unittest

#Initialize Database Engine and Connector
engine = db.create_engine('mysql+mysqldb://root:@localhost:3306/thd_test', echo = False)
connection = engine.connect()
metadata = db.MetaData()

#Read Excel File
print('Reading excel file...')
thd_data = pd.read_excel('THD_Din.xlsx', sheet_name='THD_Din', index_col='ThdID')

#Retrieve data from API
print('Retrieving API...')
api_url = "http://127.0.0.1:8000/api/heatmap_overall/"
r = requests.get(api_url)
thd_test = r.json()

#Retrieve API data from txt file to reduce waiting time
# import json
# print('Retrieving API...')
# f = open("api.txt", "r")
# raw = f.read()
# thd_test = json.loads(raw)

print('API retrieved!')

#TEST cluster_overall DATA
class TestClusterOverall(unittest.TestCase):
    def setUp(self):
        
        #Retrieve cluster_overall data from API
        cluster_test = pd.json_normalize(thd_test['cluster_overall'])
        cluster_test = cluster_test.set_index(cluster_test['cluster_full_address'])
        self.cluster_test_T = cluster_test.transpose()
        
        #Create and read database
        print('Creating Database...')
        thd_data.to_sql(name='thd', con=engine, if_exists = 'replace')
        self.thd_table = db.Table('thd', metadata, autoload=True, autoload_with=engine)
        print('Database created!')
        
        #Create cluster_overall from database
        query = db.select([self.thd_table])
        cluster_data = pd.read_sql(query, connection)
        cluster_data_gb = cluster_data.groupby(cluster_data['ClusterAddress'])
        cluster_full_address = pd.DataFrame(list(cluster_data_gb.groups.keys()), columns=['cluster_full_address'])
        cluster_full_address = cluster_full_address.set_index('cluster_full_address', drop=False)
        cluster_count = pd.DataFrame(cluster_data_gb['Cluster'].agg('count'))
        cluster_count = cluster_count.rename(columns = {'Cluster':'cluster_count'})
        cluster = pd.DataFrame(cluster_data_gb['Cluster'].first())
        cluster = cluster.rename(columns = {'Cluster': 'cluster'})
        total_customer = pd.DataFrame(cluster_data_gb['Customer'].nunique())
        total_customer = total_customer.rename(columns={'Customer': 'total_customer'})
        total_cases = pd.DataFrame(cluster_data_gb['CaseNumber'].nunique())
        total_cases = total_cases.rename(columns={'CaseNumber': 'total_cases'})
        total_complaint_sites = pd.DataFrame(cluster_data_gb['SiteID'].nunique())
        total_complaint_sites = total_complaint_sites.rename(columns={'SiteID': 'total_complaint_sites'})
        self.cluster_data_T = pd.concat([cluster, cluster_count, cluster_full_address, total_customer, total_cases, total_complaint_sites], axis=1)
        self.cluster_data_T = self.cluster_data_T.set_index(self.cluster_data_T['cluster_full_address'])
        self.cluster_data_T = self.cluster_data_T.transpose()
        
    def testCluster(self):
        print('Start Testing...')
        
        for cluster in self.cluster_data_T:
            for index in list(self.cluster_data_T.index):
                with self.subTest(item=cluster+ " : " +index):
                    self.assertEqual(self.cluster_data_T[cluster].loc[index], self.cluster_test_T[cluster].loc[index])            
        
    def tearDown(self):
        self.thd_table.drop(connection)
        print('Table dropped')

#TEST site_id_overall DATA
class TestSiteOverall(unittest.TestCase):
    def setUp(self):
        
        #Retrieve site_id_overall data from API
        site_test = pd.json_normalize(thd_test['site_id_overall'])
        site_test = site_test.set_index(site_test['site_id'])
        self.site_test_T = site_test.transpose()
        
        #Create and read database
        print('Creating Database...')
        thd_data.to_sql(name='thd', con=engine, if_exists = 'replace')
        self.thd_table = db.Table('thd', metadata, autoload=True, autoload_with=engine)
        print('Database created!')
        
        #Create site_id_overall from database
        query = db.select([self.thd_table])
        site_data = pd.read_sql(query, connection)
        site_gb = site_data.groupby(site_data['SiteID'])
        site = pd.DataFrame(list(site_gb.groups.keys()), columns=['site_id'])
        site = site.set_index('site_id', drop=False)
        total_cases = pd.DataFrame(site_gb['SiteID'].agg('count'))
        total_cases = total_cases.rename(columns = {'SiteID':'total_cases'})
        cluster_count = pd.DataFrame(site_gb['Cluster'].agg('count'))
        cluster_count = cluster_count.rename(columns = {'Cluster':'cluster_count'})
        total_customer = pd.DataFrame(site_gb['Customer'].nunique())
        total_customer = total_customer.rename(columns={'Customer': 'total_customer'})
        total_complaint_sites = pd.DataFrame(site_gb['SiteID'].nunique())
        total_complaint_sites = total_complaint_sites.rename(columns={'SiteID': 'total_complaint_sites'})
        cluster_full_address = pd.DataFrame(site_gb.ClusterAddress.first())
        cluster_full_address = cluster_full_address.rename(columns = {'ClusterAddress': 'cluster_full_address'})
        latitude = pd.DataFrame(site_gb.SiteLat.first())
        latitude = latitude.rename(columns = {'SiteLat': 'latitude'})
        longitude = pd.DataFrame(site_gb.SiteLong.first())
        longitude = longitude.rename(columns = {'SiteLong': 'longitude'})
        longitude = longitude.astype({'longitude': str})
        self.site_data_T = pd.concat([site, cluster_count, cluster_full_address, total_customer, total_cases, total_complaint_sites, latitude, longitude], axis=1)
        self.site_data_T = self.site_data_T.set_index(self.site_data_T['site_id'])
        self.site_data_T = self.site_data_T.transpose()
    
    def testSite(self):
        print('Start Testing...')
        
        for site in self.site_data_T:
                for index in list(self.site_data_T.index):
                    with self.subTest(item=site+ " : " +index):
                        self.assertEqual(self.site_data_T[site].loc[index], self.site_test_T[site].loc[index]) 
    
    def tearDown(self):
        self.thd_table.drop(connection)
        print('Table dropped')

#TEST total_customer_range
class TestCustomerRange(unittest.TestCase):
    def setUp(self):
        #Create and read database
        print('Creating Database...')
        thd_data.to_sql(name='thd', con=engine, if_exists = 'replace')
        self.thd_table = db.Table('thd', metadata, autoload=True, autoload_with=engine)
        print('Database created!')
        
        #Create total_customer from database
        query = db.select([self.thd_table])
        customer_data = pd.read_sql(query, connection)
        customer_gb = customer_data.groupby(customer_data['Cluster'])
        self.total_customer = pd.DataFrame(customer_gb['Customer'].nunique())
        
    def testMinCustomer(self):
        #retrieve data from API and database
        min_test = thd_test['total_customer_range']['min']
        min_data = self.total_customer.min().Customer
        self.assertEqual(min_data, min_test)
    
    def testMaxCustomer(self):
        #retrieve data from API and database
        max_test = thd_test['total_customer_range']['max']
        max_data = self.total_customer.max().Customer
        self.assertEqual(max_data, max_test)
    
    def tearDown(self):
        self.thd_table.drop(connection)
        print('Table dropped')


#TEST total_case_range
#TEST total_cases_overall
class TestCasesOverall(unittest.TestCase):
    def setUp(self):
        #Create and read database
        print('Creating Database...')
        thd_data.to_sql(name='thd', con=engine, if_exists = 'replace')
        self.thd_table = db.Table('thd', metadata, autoload=True, autoload_with=engine)
        print('Database created!')
        
        #Create total_customer from database
        query = db.select([self.thd_table])
        case_data = pd.read_sql(query, connection)
        case_gb = case_data.groupby(case_data['Cluster'])
        self.total_cases = pd.DataFrame(case_gb['CaseNumber'].nunique())
        
    def testMinCases(self):
        #retrieve data from API and database
        min_test = thd_test['total_case_range']['min']
        min_data = self.total_cases.min().CaseNumber
        self.assertEqual(min_data, min_test)
    
    def testMaxCases(self):
        #retrieve data from API and database
        max_test = thd_test['total_case_range']['max']
        max_data = self.total_cases.max().CaseNumber
        self.assertEqual(max_data, max_test)
        
    def testSumCases(self):
        sum_test = thd_test['total_cases_overall']
        sum_data = self.total_cases.sum().CaseNumber
        self.assertEqual(sum_data, sum_test)

    def tearDown(self):
        self.thd_table.drop(connection)
        print('Table dropped')
        

def run_tests():
    # Run only the tests in the specified classes

    test_classes_to_run = [TestClusterOverall, TestSiteOverall, TestCustomerRange, TestCasesOverall]

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)
        
    big_suite = unittest.TestSuite(suites_list)
    f = open('testThdAPI.log', "w")
    runner = unittest.TextTestRunner(f)
    results = runner.run(big_suite)

if __name__ == '__main__':
    run_tests()
    