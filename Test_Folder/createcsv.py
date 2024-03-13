import requests
from pprint import pformat

station_id = "44t"
param = "PM25,O3,WS,TEMP,RH,WD"
data_type = "hr"
start_date = "2023-12-01"
end_date = "2024-03-04"
start_time = "00"
end_time = "23"
url = f"http://air4thai.com/forweb/getHistoryData.php?stationID={station_id}&param={param}&type={data_type}&sdate={start_date}&edate={end_date}&stime={start_time}&etime={end_time}"
response = requests.get(url)
response_json = response.json()
#print(pformat(response_json))

import pandas as pd

pd_from_dict = pd.DataFrame.from_dict(response_json["stations"][0]["data"])

#cleaning data
pd_from_dict.loc[pd_from_dict['TEMP'] == 0, 'TEMP'] = pd_from_dict['TEMP'].mean()
pd_from_dict.loc[pd_from_dict['TEMP'] > 40, 'TEMP'] = pd_from_dict['TEMP'].mean()
pd_from_dict.loc[pd_from_dict['TEMP'].isnull(), 'TEMP'] = pd_from_dict['TEMP'].mean()
pd_from_dict.loc[pd_from_dict['PM25'] == 0, 'PM25'] = pd_from_dict['PM25'].mean()
pd_from_dict.loc[pd_from_dict['PM25'] > 1000, 'PM25'] = pd_from_dict['PM25'].mean()
pd_from_dict.loc[pd_from_dict['PM25'] < 0, 'PM25'] = pd_from_dict['PM25'].mean()
pd_from_dict.loc[pd_from_dict['PM25'].isnull(), 'PM25'] = pd_from_dict['PM25'].mean()
pd_from_dict.loc[pd_from_dict['O3'] == 0, 'O3'] = pd_from_dict['O3'].mean()
pd_from_dict.loc[pd_from_dict['O3'] > 200, 'O3'] = pd_from_dict['O3'].mean()
pd_from_dict.loc[pd_from_dict['O3'].isnull(), 'O3'] = pd_from_dict['O3'].mean()
pd_from_dict.loc[pd_from_dict['WS'] == 0, 'WS'] = pd_from_dict['WS'].mean()
pd_from_dict['WS'] = pd_from_dict['WS'].astype(int)
pd_from_dict.loc[pd_from_dict['RH'] == 0, 'RH'] = pd_from_dict['RH'].mean()
pd_from_dict.loc[pd_from_dict['RH'] > 100, 'RH'] = pd_from_dict['RH'].mean()
pd_from_dict.loc[pd_from_dict['RH'].isnull(), 'RH'] = pd_from_dict['RH'].mean()
pd_from_dict.loc[pd_from_dict['WD'] == 0, 'WD'] = pd_from_dict['WD'].mean()
pd_from_dict.loc[pd_from_dict['WD'] > 360, 'WD'] = pd_from_dict['WD'].mean()
pd_from_dict.loc[pd_from_dict['WD'].isnull(), 'WD'] = pd_from_dict['WD'].mean()
pd_from_dict['DATETIMEDATA'] = pd.to_datetime(pd_from_dict['DATETIMEDATA'])
#drop DATETIMEDATA
pd_from_dict = pd_from_dict.drop(columns=['DATETIMEDATA'])
#rename columns



#save to csv
pd_from_dict.to_csv(f"train.csv",index=False)
print(pformat(pd_from_dict))
