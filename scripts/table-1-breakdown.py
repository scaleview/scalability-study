import pandas as pd
import numpy as np

def get_bug_ids_with_tag(df, tag):
    return df[df['Tags'].apply(lambda x: tag in x)]['ID'].tolist()

empirical_data = pd.read_csv('pattern-study/scalability-bugs.csv')

systems = ['CASSANDRA', 'HADOOP', 'HBASE', 'HDFS', 'IGNITE', 'KAFKA', 'MAPREDUCE', 'SPARK', 'STORM', 'YARN']
dimensions = ['sc-load', 'sc-data', 'sc-clus', 'sc-fail']
dimension_system_table = {'sc-clus': {}, 'sc-fail': {}, 'sc-load': {}, 'sc-data': {}}

for dimension in dimensions:
    for system in systems:
        bugs_in_system = get_bug_ids_with_tag(empirical_data[empirical_data['System'] == system], dimension)
        dimension_system_table[dimension][system] = len(bugs_in_system)

dimension_breakdown = pd.DataFrame(dimension_system_table).T
dimension_breakdown['Total'] = dimension_breakdown.sum(axis=1)

print(dimension_breakdown)




