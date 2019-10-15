import pandas as pd
import numpy as np
from itertools import chain
from sklearn.decomposition import PCA

class DataPrep:
    def __init__(self, df):
        self.raw_df = df
    
    def seperate_frame(self):
        new_diagnosis_col = ['New diagnosis - CPD',
                         'New diagnosis - Hypertension', 
                         'New diagnosis - Top 5', 
                         'New diagnosis - CAD', 
                         'New diagnosis - CHF', 
                         'New diagnosis - Diabetes']

        call_col = ['Inbound Call by Prov',
                    'Inbound Call by Mbr',
                    'Inbound Call by Other']

        non_rx_claim_col = ['Surgery',
                            'Fully Paid Claim']

        rx_claim_col = ['RX Claim - New Drug',
                        'RX Claim - First Time Mail Order']
        
        self.new_diagnosis = self.raw_df[self.raw_df['event_descr'].isin(new_diagnosis_col)]

        self.new_diagnosis = self.new_diagnosis.drop(['event_attr6',
                                                      'event_attr7',
                                                      'event_attr8',
                                                      'event_attr9',
                                                      'event_attr10',
                                                      'PAY_DAY_SUPPLY_CNT',
                                                      'PAYABLE_QTY',
                                                      'MME',
                                                      'DRUG_TYPE',
                                                      'Specialty',
                                                      'Specialty2',
                                                      'Specialty3'],
                                                       axis = 1)

        self.new_diagnosis.columns = ['id',
                                 'event_descr',
                                 'diagnosis',
                                 'place_of_treatment',
                                 'charge_amount',
                                 'net_paid_amount',
                                 'member_responsible_amount',
                                 'Days']
        
        self.call = self.raw_df[self.raw_df['event_descr'].isin(call_col)]

        self.call = self.call.drop(['event_attr6',
                          'event_attr7',
                          'event_attr8',
                          'event_attr9',
                          'event_attr10',
                          'PAY_DAY_SUPPLY_CNT',
                          'PAYABLE_QTY',
                          'MME',
                          'DRUG_TYPE',
                          'Specialty',
                          'Specialty2',
                          'Specialty3'],
                           axis = 1)

        self.call.columns = ['id',
                        'event_descr',
                        'call_category',
                        'inquiry_reason_description',
                        'disposition_description',
                        'origin',
                        'location',
                        'Days']
        
        self.non_rx_claim = self.raw_df[self.raw_df['event_descr'].isin(non_rx_claim_col)]

        self.non_rx_claim = self.non_rx_claim.drop(['event_attr6',
                                          'event_attr7',
                                          'event_attr8',
                                          'event_attr9',
                                          'event_attr10',
                                          'PAY_DAY_SUPPLY_CNT',
                                          'PAYABLE_QTY',
                                          'MME',
                                          'DRUG_TYPE',
                                          'Specialty',
                                          'Specialty2',
                                          'Specialty3'],
                                           axis = 1)

        self.non_rx_claim.columns = ['id',
                                'event_descr',
                                'diagnosis',
                                'place_of_treatment',
                                'charge_amount',
                                'net_paid_amount',
                                'member_responsible_amount',
                                'Days']
        
        self.new_provider = self.raw_df[self.raw_df['event_descr']=='New provider']
        self.new_provider = self.new_provider.iloc[:,:2]
        
        self.rx_claim = self.raw_df[self.raw_df['event_descr'].isin(rx_claim_col)]

        self.rx_claim = self.rx_claim.drop(['event_attr6',
                          'event_attr7'],
                           axis = 1)

        self.rx_claim.columns = ['id',
                            'event_descr',
                            'gpi_drug_group6_id',
                            'gpi_drug_class_description',
                            'brand_name',
                            'drug_group_id',
                            'generic_name',
                            'drug_group_description',
                            'member_responsible_amount',
                            'gpi_drug_group8_id',
                            'Days',
                            'PAY_DAY_SUPPLY_CNT',
                            'PAYABLE_QTY',
                            'MME',
                            'DRUG_TYPE',
                            'Specialty',
                            'Specialty2',
                            'Specialty3']
        
        self.rx_paid = self.raw_df[self.raw_df['event_descr']=='RX Claim - Paid']

        self.rx_paid = self.rx_paid.drop(['event_attr2',
                                'event_attr7'],
                                 axis = 1)

        self.rx_paid.columns = ['id',
                           'event_descr',
                           'gpi_drug_class_description',
                           'rx_cost',
                           'net_paid_amount',
                           'brand_name',
                           'drug_group_description',
                           'generic_name',
                           'member_responsible_amount',
                           'gpi_drug_group8_id',
                           'Days',
                           'PAY_DAY_SUPPLY_CNT',
                           'PAYABLE_QTY',
                           'MME',
                           'DRUG_TYPE',
                           'Specialty',
                           'Specialty2',
                           'Specialty3']
        
        self.rx_reject = self.raw_df[self.raw_df['event_descr']=='RX Claim - Rejected']

        self.rx_reject = self.rx_reject.drop(['PAY_DAY_SUPPLY_CNT',
                                    'PAYABLE_QTY',
                                    'MME',
                                    'DRUG_TYPE',
                                    'Specialty',
                                    'Specialty2',
                                    'Specialty3'],
                                     axis =1)

        self.rx_reject.columns = ['id',
                             'event_descr',
                             'status_code',
                             'diagnosis',
                             'cob',
                             'claim_tier',
                             'brand_name',
                             'generic_name',
                             'ndc_id',
                             'pay_day_supply_count',
                             'member_responsible_amount',
                             'gpi_drug_group8_id',
                             'Days']
        
    def get_opioid_data(self):
        self.opioid_data = self.raw_df[self.raw_df['PAY_DAY_SUPPLY_CNT'].notnull()]
        self.opioid_data_grouped = self.opioid_data.groupby(by='id')
        
    def LTOT(self):
        
        def get_LTOT(ID):
            try:
                group = self.opioid_data_grouped.get_group(ID)
                frame = group[['Days', 'PAY_DAY_SUPPLY_CNT']].drop_duplicates()
                frame = frame[frame['Days']>=0]
                frame['drugs until'] = (frame['Days'] + frame['PAY_DAY_SUPPLY_CNT']).astype(int)
                frame['range'] = frame.apply(lambda x : range(x['Days'].astype(int),x['drugs until'].astype(int)),1)

                concat = concatenated = chain(*list(frame['range']))
                concat = set(concat)

                day_frame = pd.DataFrame(columns = ['Days', 'Has Drug?'])
                day_frame['Days'] = range(max(concat)+1)
                day_frame['Has Drug?'] = (day_frame['Days'].isin(concat))

                for n in range(180,len(day_frame)+1):
                    frame_slice = day_frame.iloc[n-180:n]
                    drug_days = np.sum(frame_slice['Has Drug?'])

                    if drug_days >= 162:
                        return (True, n-180, n)

                return (False, np.nan, np.nan)
            except:
                return (np.nan, np.nan, np.nan)
        
        id_list = self.raw_df['id'].drop_duplicates().values
        
        response_variable = pd.DataFrame(id_list, columns = ['id'])
        response_variable['LTOT'] = response_variable['id'].map(get_LTOT)
        
        response_variable[['LTOT', 'Begining Date', 'End Date']] = \
        pd.DataFrame(response_variable['LTOT'].tolist(), index = response_variable.index)
        
        self.response_variable = response_variable.set_index('id')
    
    
    def main_feature_extraction(self): 
        opioid_all_time = self.rx_paid[self.rx_paid['PAY_DAY_SUPPLY_CNT'].notnull()]['generic_name'].value_counts()
        mask = self.rx_paid['generic_name'].map(lambda x: x in opioid_all_time.index.values)
        true_opioid = self.rx_paid[mask]
        
        true_opioid['PAY_DAY_SUPPLY_CNT'].fillna(true_opioid['PAY_DAY_SUPPLY_CNT'].mode(), inplace=True)
        true_opioid['PAYABLE_QTY'].fillna(true_opioid['PAYABLE_QTY'].mean(), inplace=True)
        true_opioid['MME'].fillna(true_opioid['MME'].mode(), inplace=True)
        
        opioid_grouped = true_opioid.groupby(by=['id'])

        idtestlist = true_opioid['id'].drop_duplicates()
        features3 = pd.DataFrame()

        for ID in idtestlist:
            tmp = opioid_grouped.get_group(ID)

            # MME (per day) on day 0
            # Suuply_CNT on day 0
            on_day0 = tmp[tmp['Days'] == 0] 
            if not on_day0.empty:
                MME0 = on_day0['MME'].values[0]
                SC0 = on_day0['PAY_DAY_SUPPLY_CNT'].values[0]
                PQ0 = on_day0['PAYABLE_QTY'].values[0]
                RX0 = on_day0['rx_cost'].values[0]
                NP0 = on_day0['net_paid_amount'].values[0]
            else:
                MME0 = 0
                SC0 = 0
                PQ0 = 0
                RX0 = 0
                NP0 = 0

            # max MME (per day) prior to day 0
            # average MME (per day) prior to day 0
            # Total Supply_CNT prior to day 0
            prior_day0 = tmp[tmp['Days'] < 0]
            if not prior_day0.empty:
                maxMME = np.nanmax(prior_day0['MME'].values)
                avgMME = np.nanmean(prior_day0['MME'].values)
                totalSC = np.nansum(prior_day0['PAY_DAY_SUPPLY_CNT'].values)
                totalPQ = np.nansum(prior_day0['PAYABLE_QTY'].values)
            else:
                maxMME = 0
                avgMME = 0
                totalSC = 0
                totalPQ = 0

            output = pd.DataFrame({'MME_on_day0': MME0, 
                                 'SUPPLY_CNT_on_day0': SC0,
                                   'PAYABLE_QTY_on_day0': PQ0,
                                 'max_MME_prior': maxMME,
                                 'avg_MME_prior': avgMME,
                                 'total_SUPPLY_CNT_prior': totalSC,
                                  'total_PAYABLE_QTY_prior': totalPQ,
                                  'opioid_cost_on_day_0': RX0,
                                  'opioid_net_payment_on_day_0':NP0},
                                  index = [ID])

            features3 = features3.append(output, sort=False)

        # MME_on_day0, max_MME_prior, avg_MME_prior has some missing value, fill with medians
        features3['MME_on_day0'] = features3['MME_on_day0'].fillna(np.nanmedian(features3['MME_on_day0']))
        features3['max_MME_prior'] = features3['max_MME_prior'].fillna(np.nanmedian(features3['max_MME_prior']))
        features3['avg_MME_prior'] = features3['avg_MME_prior'].fillna(np.nanmedian(features3['avg_MME_prior']))

        # add one more feature: supply_times
        supply_times = true_opioid[true_opioid['Days']<=0].groupby(by=['id'])['PAY_DAY_SUPPLY_CNT'].count()
        supply_times = pd.DataFrame(supply_times)
        supply_times.columns = ['supply_times']
        features3 = features3.merge(supply_times, left_on=features3.index.values, right_on=supply_times.index.values)
        features3 = features3.set_index('key_0')
        
        self.rx_paid['rx_cost'] = self.rx_paid['rx_cost'].map(float)
        self.rx_paid['net_paid_amount'] = self.rx_paid['net_paid_amount'].map(float)

        # add total costs features
        total_costs_on_day_0 = self.rx_paid[self.rx_paid['Days']==0].groupby(by=['id'])['rx_cost'].agg(np.sum)
        total_net_payment_on_day_0 = self.rx_paid[self.rx_paid['Days']==0].groupby(by=['id'])['net_paid_amount'].agg(np.sum)

        features3['total_costs_on_day_0'] = total_costs_on_day_0
        features3['total_net_payment_on_day_0'] = total_net_payment_on_day_0
        features3['net_payment_portion_on_day_0'] = total_net_payment_on_day_0/total_costs_on_day_0
        features3['opioid_cost_portion_on_day_0'] = features3['opioid_cost_on_day_0'].astype(float)/features3['total_costs_on_day_0'].astype(float)

        # add some interaction
        features3['MME_times_SUPPLY_day_0'] = features3['MME_on_day0']*features3['SUPPLY_CNT_on_day0']
        features3['total_cost_divide_SUPPLY_day_0'] = features3['total_costs_on_day_0']/features3['SUPPLY_CNT_on_day0']
        features3['total_net_payment_divide_on_day_0'] = features3['total_net_payment_on_day_0']/features3['SUPPLY_CNT_on_day0']
        features3['np_portion_divide_SUPPLY_day_0'] = features3['net_payment_portion_on_day_0']/features3['SUPPLY_CNT_on_day0']
        features3['oc_portion_divide_SUPPLY_day_0'] = features3['opioid_cost_portion_on_day_0']/features3['SUPPLY_CNT_on_day0']

        features3['max_MME_prior_divide_SUPPLY_day_0'] = features3['max_MME_prior']/features3['SUPPLY_CNT_on_day0']
        features3['avg_MME_prior_divide_SUPPLY_day_0'] = features3['avg_MME_prior']/features3['SUPPLY_CNT_on_day0']
        features3['tsc_prior_divide_SUPPLY_day_0'] = features3['total_SUPPLY_CNT_prior']/features3['SUPPLY_CNT_on_day0']
        features3['tpa_prior_divide_SUPPLY_day_0'] = features3['total_PAYABLE_QTY_prior']/features3['SUPPLY_CNT_on_day0']
        features3['oc_day_0_divide_SUPPLY_day_0'] = features3['opioid_cost_on_day_0'].astype(float)/features3['SUPPLY_CNT_on_day0']
        features3['np_day_0_divide_SUPPLY_day_0'] = features3['opioid_net_payment_on_day_0'].astype(float)/features3['SUPPLY_CNT_on_day0']
        
        self.main_features = features3
        
    def generic_feature_extraction(self):
        opioid_all_time = self.rx_paid[self.rx_paid['PAY_DAY_SUPPLY_CNT'].notnull()]['generic_name'].value_counts()
        mask = self.rx_paid['generic_name'].map(lambda x: x in opioid_all_time.index.values)
        true_opioid = self.rx_paid[mask] 
        
        opioid2_grouped = true_opioid[true_opioid['Days'] == 0].groupby(by=['id'])

        idtestlist = true_opioid[true_opioid['Days'] == 0]['id'].drop_duplicates()

        ## those commented-out codes are used to get other entry values
        # def product_sum(df):
        #     return(df['MME'].values.dot(df['PAY_DAY_SUPPLY_CNT']e.values))

        features = pd.DataFrame()
        for ID in idtestlist:
            tmp = opioid2_grouped.get_group(ID)
            output = pd.DataFrame(tmp.groupby(by='generic_name')['PAY_DAY_SUPPLY_CNT'].agg(np.nansum)).T
        #     output = output.iloc[0:1,:]
            output.index = [ID]
            # features = pd.concat([output, features], axis=1, sort=False)
            features = features.append(output, sort=False)

        features = features.fillna(0)
        
        pca = PCA(n_components = 10) 
        X10D = pca.fit_transform(features)
        
        features_matthew_generic = pd.DataFrame(X10D, index=features.index.values)
        features_matthew_generic.columns = ['generic_pc{}'.format(x) for x in features_matthew_generic.columns]
        
        self.generic_features = features_matthew_generic
        
    def get_features(self, derive_response = False):
        if derive_response:
            self.seperate_frame()
            self.get_opioid_data()
            self.LTOT()
            self.main_feature_extraction()
            self.generic_feature_extraction()
            
            self.feature_frame = pd.concat([self.response_variable[['LTOT']], 
                                           self.main_features, 
                                           self.generic_features], 
                                           axis=1, join = 'inner').dropna()
            
            self.feature_frame = self.feature_frame.apply(pd.to_numeric, errors='coerce')
            
        else:
            self.seperate_frame()
            self.main_feature_extraction()
            self.generic_feature_extraction()
            
            #changed from inner
            self.feature_frame = pd.concat([self.main_features, 
                                           self.generic_features], 
                                           axis=1, join = 'outer')
            
            self.feature_frame = self.feature_frame.apply(pd.to_numeric, errors='coerce')