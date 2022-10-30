import pandas as pd

A_office_data = pd.read_xml('https://www.dropbox.com/s/jpeknyzx57c4jb2/A_office_data.xml?dl=1')
B_office_data = pd.read_xml('https://www.dropbox.com/s/hea0tbhir64u9t5/B_office_data.xml?dl=1')
HR_data = pd.read_xml('https://www.dropbox.com/s/u6jzqqg1byajy0s/hr_data.xml?dl=1')

HR_data.set_index('employee_id', inplace=True)

for x in A_office_data['employee_office_id']:
    A_office_data['employee_office_id'].replace({x: 'A' + str(x)}, inplace=True)

for x in B_office_data['employee_office_id']:
    B_office_data['employee_office_id'].replace({x: 'B' + str(x)}, inplace=True)

A_office_data.set_index('employee_office_id', inplace=True)
B_office_data.set_index('employee_office_id', inplace=True)

Unified_data = pd.concat([A_office_data, B_office_data])
Unified_data = Unified_data.merge(HR_data, how='inner', left_index=True, right_index=True, indicator=True)
Unified_data.drop(columns=['_merge'], inplace=True)
Unified_data.sort_index(inplace=True)

first_table = pd.pivot_table(Unified_data, index='Department', columns=['left', 'salary'],
                             values='average_monthly_hours', aggfunc='median').round(2)
first_to_dict = first_table.loc[(first_table[0].high < first_table[0].medium) &
                                (first_table[1].low < first_table[1].high)]
second_table = pd.pivot_table(Unified_data, index='time_spend_company', columns='promotion_last_5years',
                              values=['last_evaluation', 'satisfaction_level'], aggfunc=['min', 'max', 'mean']).round(2)
second_to_dict = second_table.loc[second_table['mean']['last_evaluation'][0] >
                                  second_table['mean']['last_evaluation'][1]]
print(first_to_dict.to_dict())
print(second_to_dict.to_dict())
