""" This script combines HateCrimes_json.json, HateCrimes_csv.csv and
hatecrimes.db. Combined Data is written as CSV. In addition the combined 
data frame is used to explore the crime by agency type, quarter, ethnic groups
and disability

@author: Aruna Kumaraswamy (akumaras@umail.iu.edu)
"""
import pandas as pd
import numpy as np
import sqlite3

if __name__ == "__main__":
    hate_crime_json_df = pd.read_json('../data/HateCrimes_json.json')
    hate_crime_csv_df = pd.read_csv('../data/HateCrimes_csv.csv')
    con = sqlite3.connect("../data/hatecrimes.db")
    hate_crime_sql_df = pd.read_sql_query("SELECT state as State, agtype as Agency_type, agName as Agency_name,vRace,vRel,vSexOr from crimes", con)

    #Q1. Combine the data from the three  and write the output to a CSV.
    hate_crime_merged = pd.merge(hate_crime_csv_df,hate_crime_json_df,how='left')
    # SQL does not have certain Agencies. So an outer join is done
    hate_crime_merged = pd.merge(hate_crime_merged,hate_crime_sql_df,how='left')
    hate_crime_merged.to_csv('../data/HateCrimes_Combined.csv')
    
    con.close()
    
    #GroupBy Agency Type and Aggregate sum of each quarter
    hate_crime_by_agency_type = hate_crime_merged.groupby('Agency_type').agg({'quarter_1':np.sum,'quarter_2':np.sum,'quarter_3':np.sum,'quarter_4':np.sum})  
    
    #Q2 -B - Maximum Crimes in Quarter?
    print 'Total crimes in quarter1',hate_crime_merged['quarter_1'].sum()
    print 'Total crimes in quarter2',hate_crime_merged['quarter_2'].sum()
    print 'Total crimes in quarter3',hate_crime_merged['quarter_3'].sum()
    print 'Total crimes in quarter4',hate_crime_merged['quarter_4'].sum()
    
    print('--------------------------------------------------')
    print('2013 - Quarterly summary of crimes by Agency Type')
    print('--------------------------------------------------')
    print(hate_crime_by_agency_type)
    
    #Q2-C Maximum crimes in which agency type
    print('\n--------------------------------------------------')
    print('2013 - Agency Type with maximum reported crimes')
    print('--------------------------------------------------')
    agency_type = ''
    reported_crimes = 0;
    for row in hate_crime_by_agency_type.itertuples():
        total_crimes = row[1]+row[2]+row[4]+row[3]
        if total_crimes > reported_crimes:
            reported_crimes = total_crimes
            agency_type = row[0]
    print agency_type,' has more reported crimes: ',reported_crimes   
    
    
    #Q2 - A: percentage of the Annual crime happened in each of the four Quarters 
    #when aggregated at Agency type level?
    total_crime_all_quarters = hate_crime_merged['quarter_1'].sum()+hate_crime_merged['quarter_2'].sum()+hate_crime_merged['quarter_3'].sum()+hate_crime_merged['quarter_4'].sum()
    hate_crime_by_agency_type['quarter_1'] = (hate_crime_by_agency_type['quarter_1']/total_crime_all_quarters)*100
    hate_crime_by_agency_type['quarter_2'] = (hate_crime_by_agency_type['quarter_2']/total_crime_all_quarters)*100
    hate_crime_by_agency_type['quarter_3'] = (hate_crime_by_agency_type['quarter_3']/total_crime_all_quarters)*100
    hate_crime_by_agency_type['quarter_4'] = (hate_crime_by_agency_type['quarter_4']/total_crime_all_quarters)*100
    
    print('\n')
    print('--------------------------------------------------');
    print('2013 - Quarterly Percentage of crimes by Agency Type')
    print('--------------------------------------------------');
    print(hate_crime_by_agency_type.round(2))
    
    # Q3: Crimes reported by State and order by the States where more ethnic groups are reported.
    print('\n--------------------------------------------------');
    print('2013 - Crimes reported by State-Ethnicity')
    print('--------------------------------------------------');
    hate_crime_by_state = hate_crime_merged.groupby('State')['Ethnicity'].nunique()
    hate_crime_by_state = hate_crime_by_state.sort_values(ascending=False)
    print(hate_crime_by_state)
    
    #Q4: Find the percentage of crimes committed against disabled and non-disabled groups in each of the four quarters.
    print('\n--------------------------------------------------');
    print('2013 - Crimes reported by Quarter - Disability')
    print('--------------------------------------------------');
    
    hate_crime_merged.loc[hate_crime_merged.Disability > 0, 'Disability'] = 'Disabled'
    hate_crime_merged.loc[hate_crime_merged.Disability == 0, 'Disability'] = 'Non-Disabled'
    
    hate_crime_disability_by_qtr = hate_crime_merged.groupby('Disability').agg({'quarter_1':np.sum,'quarter_2':np.sum,'quarter_3':np.sum,'quarter_4':np.sum})
    hate_crime_disability_by_qtr['quarter_1'] = (hate_crime_disability_by_qtr['quarter_1']/total_crime_all_quarters)*100
    hate_crime_disability_by_qtr['quarter_2'] = (hate_crime_disability_by_qtr['quarter_2']/total_crime_all_quarters)*100
    hate_crime_disability_by_qtr['quarter_3'] = (hate_crime_disability_by_qtr['quarter_3']/total_crime_all_quarters)*100
    hate_crime_disability_by_qtr['quarter_4'] = (hate_crime_disability_by_qtr['quarter_4']/total_crime_all_quarters)*100
    
    print(hate_crime_disability_by_qtr.round(2) )