import json
import os
import requests
from dotenv import load_dotenv; load_dotenv()

stein_url = os.getenv('STEIN_URL')
stein_url_enbedding = os.getenv('STEIN_URL_EMB')
def post_stein_api(data: dict):
  return post_stein(data, stein_url)

def post_stein_enb(data: list):
  dict_data = {}
  for i in range(len(data)):
    dict_data[i+1] = data[i] # 1-index
    
  return post_stein(dict_data, stein_url_enbedding)

def post_stein(data: dict, stein_url: str):
  data_str = json.dumps(data)
  response = requests.post(
    stein_url,
    data=f'[{data_str}]',
    headers={"Content-Type": "application/json"},
  )
  
  if not response.ok:
    raise Exception(f"HTTP Error: {response.status_code} - {response.reason}")
  
  return response

if __name__ == '__main__':
  
  test_json = {
    "会社名": "test株式会社",
    "部署名": "test本部 test戦略部 test構築グループ",
    "氏名": "test man",
    "郵便番号":"",
    "会社住所": "",
    "電話番号": "090-1234-5678",
    "FAX番号": "012-345-6789",
    "e-mailアドレス": "test@test.jp",
    "会社ホームページ": "demo.com",
    "職業分類": "製造業",
    "カテゴリ": "test",
    "チャプター名": "test"

  }

  test = [
    0,
    220,
    0.34,
    0.55,
    0.55,
    0.55,
    0.55,
    0.55,
    0.55,
    0.55,
  ]
  res = post_stein_api(test_json)
  # res = post_stein_enb(test)
  print(res.text)
  print(res.status_code)