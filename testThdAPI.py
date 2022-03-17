import requests
import pandas as pd
import sqlalchemy as db
import unittest
import logging

#Initialize Logger
logger = logging.getLogger()

file_log_handler = logging.FileHandler('logfile.log')
logger.addHandler(file_log_handler)

stderr_log_handler = logging.StreamHandler()
logger.addHandler(stderr_log_handler)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_log_handler.setFormatter(formatter)
stderr_log_handler.setFormatter(formatter)

#Initialize Database Engine and Connector
engine = db.create_engine('mysql+mysqldb://root:@localhost:3306/thd_test', echo = False)
connection = engine.connect()
metadata = db.MetaData()

#Read Excel File
print('Reading excel file...')
logger.info('Reading excel file...')
thd_data = pd.read_excel('THD_Din.xlsx', sheet_name='THD_Din', index_col='ThdID')

#Retrieve data from API
print('Retrieving API...')
logger.info('Retrieving API...')
api_url = "http://127.0.0.1:8000/api/heatmap_overall/"
r = requests.get(api_url)
thd_test = r.json()

print('API retrieved!')
logger.info('API retrieved!')


#TEST cluster_overall DATA
class TestClusterOverall(unittest.TestCase):
    def setUp(self):
        
        #Retrieve cluster_overall data from API
        cluster_test = pd.json_normalize(thd_test['cluster_overall'])
        cluster_test = cluster_test.set_index(cluster_test['cluster'])
        self.cluster_test_T = cluster_test.transpose()
        
        #Create and read database
        print('Creating Database...')
        logger.info('Creating Database...')
        thd_data.to_sql(name='thd', con=engine, if_exists = 'replace')
        self.thd_table = db.Table('thd', metadata, autoload=True, autoload_with=engine)
        print('Database created!')
        logger.info('Database created!')
        
        #Create cluster_overall from database
        query = db.select([self.thd_table])
        cluster_data = pd.read_sql(query, connection)
        cluster_data_gb = cluster_data.groupby(cluster_data['Cluster'])
        cluster = pd.DataFrame(list(cluster_data_gb.groups.keys()), columns=['cluster'])
        cluster = cluster.set_index('cluster', drop=False)
        cluster_count = pd.DataFrame(cluster_data_gb['Cluster'].agg('count'))
        cluster_count = cluster_count.rename(columns = {'Cluster':'cluster_count'})
        cluster_full_address = pd.DataFrame(cluster_data_gb['ClusterAddress'].first())
        cluster_full_address = cluster_full_address.rename(columns = {'ClusterAddress': 'cluster_full_address'})
        total_customer = pd.DataFrame(cluster_data_gb['Customer'].nunique())
        total_customer = total_customer.rename(columns={'Customer': 'total_customer'})
        total_cases = pd.DataFrame(cluster_data_gb['CaseNumber'].nunique())
        total_cases = total_cases.rename(columns={'CaseNumber': 'total_cases'})
        total_complaint_sites = pd.DataFrame(cluster_data_gb['SiteID'].nunique())
        total_complaint_sites = total_complaint_sites.rename(columns={'SiteID': 'total_complaint_sites'})
        self.cluster_data_T = pd.concat([cluster, cluster_count, cluster_full_address, total_customer, total_cases, total_complaint_sites], axis=1)
        self.cluster_data_T = self.cluster_data_T.set_index(self.cluster_data_T['cluster'])
        self.cluster_data_T = self.cluster_data_T.transpose()
        
        print(self.cluster_data_T)
        print(self.cluster_test_T)
        
    def testCluster(self):
        print('Start Testing...')
        logger.info('Start Testing...')
        logger.error('FAIL CLUSTER:')
        success = 0
        fail = 0
        for cluster in self.cluster_data_T:
            with self.subTest(line=cluster): 
                #Compare column by column between both transposed table (means compare cluster by cluster)
                compare = self.cluster_data_T[cluster].equals(self.cluster_test_T[cluster])
                if compare:
                    success+=1
                else:
                    logger.error(cluster)
                    fail+=1
                    
                self.assertTrue(compare)
        
        print(str(success) + " subtests success, " + str(fail) + " subtests fail.")
        logger.error(str(success) + " subtests success, " + str(fail) + " subtests fail.")
        
    def tearDown(self):
        self.thd_table.drop(connection)
        print('Table dropped')
        logger.info('Table dropped')
    
if __name__ == '__main__':
    unittest.main()

#sit_id_overall
#total_customer_range
#total_case_range
#total_cases_overall