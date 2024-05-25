import requests
from pprint import pprint
import json

app_id = 'A11223037-7ef51687-e1de-4a73'
app_key = '0eb09902-b21d-474b-a18a-0c6012550afe'

auth_url="https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"
api_url = "https://tdx.transportdata.tw/api/basic/v2/Bus/EstimatedTimeOfArrival/City/NantouCounty/3?%24top=30&%24format=JSON"

class Auth():
     def __init__(self, app_id, app_key):
         self.app_id = app_id
         self.app_key = app_key

     def get_auth_header(self):
         return {
             'Content-Type': 'application/x-www-form-urlencoded',
             'grant_type': 'client_credentials',
             'client_id': self.app_id,
             'client_secret': self.app_key
         }

class Data():
     def __init__(self, auth_token):
         self.auth_token = auth_token

     def get_data_header(self):
         return {
             'Authorization': f'Bearer {self.auth_token}',
             'Accept-Encoding': 'gzip'
         }

     def get_bus_data_for_stops(self, url):
         headers = self.get_data_header()
         response = requests.get(url, headers=headers)
         response.raise_for_status()
         data = response.json()

         # 過濾特定站點的資料
         stops_of_interest = ['中興', '中學路', '中興國中']
         filtered_data = []
         for item in data:
             if item['StopName']['Zh_tw'] in stops_of_interest:
                 stop_info = {
                     '車站名字': item['StopName']['Zh_tw'],
                     '車牌號碼': item.get('PlateNumb', 'N/A'),
                     '行駛方向': '去程' if item.get('Direction') == 1 else '回程',
                     '預估時間': item.get('EstimateTime', 'N/A'),
                     '是否末班車': item.get('IsLastBus', False)
                 }
                 filtered_data.append(stop_info)
         return filtered_data

def get_auth_token(app_id, app_key):
     try:
         response = requests.post(auth_url, data=Auth(app_id, app_key).get_auth_header())
         response.raise_for_status()
         return response.json().get('access_token')
     except Exception as e:
         print(f"取得授權令牌失敗: {e}")
         return None

def main():
     auth_token = get_auth_token(app_id, app_key)
     if auth_token:
         data_instance = Data(auth_token)
         bus_data = data_instance.get_bus_data_for_stops(api_url)
         if bus_data:
             print(json.dumps(bus_data, ensure_ascii=False, indent=4))
             with open('filtered_bus_data.json', 'w', encoding='utf-8') as f:
                 json.dump(bus_data, f, ensure_ascii=False, indent=4)
         else:
             print("無法取得數據，授權失敗或資料取得失敗。")
     else:
         print("無法取得授權令牌。")

if __name__ == '__main__':
     main()