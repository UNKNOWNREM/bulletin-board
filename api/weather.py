import requests
import pandas as pd
import json

# API URL
url = 'https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-D0047-023?Authorization=CWA-C357D1A4-AF79-4761-9F1D-7926DA705E31&format=JSON&loName=% 97%E6%8A%95%E5%B8%82&#39';

# 金鑰
authorization_token = 'CWA-C357D1A4-AF79-4761-9F1D-7926DA705E31'

# 請求參數
params = {
     'Authorization': authorization_token,
     'format': 'JSON',
     'locationName': '南投市', # 根據需要修改地點
     'sort': 'time'
}

# 發送HTTP GET請求
response = requests.get(url, params=params)

if response.status_code == 200:
     data_json = response.json()

if 'records' in data_json and 'locations' in data_json['records'] and len(data_json['records']['locations']) > 0:
     # 取得第一個位置的天氣預報數據
     location_data = data_json['records']['locations'][0]['location'][0]
    
     # 假設 WeatherDescription 是 weatherElement 陣列中的某個元素
     weather_description_element = location_data['weatherElement'][10]
     times = weather_description_element['time']
    
     # 檔案名，這將保存在目前工作目錄中
     filename = 'weather_forecast.txt'
    
     with open(filename, 'w', encoding='utf-8') as file:
         # 遍歷每個時段
         for time in times:
             start_time = time['startTime']
             end_time = time['endTime']
             # 提取描述文本，這裡假設您想要的描述是elementValue數組中的第一個元素
             forecast_description = time['elementValue'][0]['value']
            
             # 將天氣預報寫入文字文件
             file.write(f'時間從 {start_time} 到 {end_time} 的天氣預報綜合描述: {forecast_description}\n')
else:
     print('JSON資料格式不符合預期，無法寫入天氣資料。')

print(f'天氣資料已成功寫入到目前目錄下的 {filename} 檔案。')