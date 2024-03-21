import json
import os
import requests
from dotenv import load_dotenv; load_dotenv()

stein_url = os.getenv('STEIN_URL')
stein_url_enbedding = os.getenv('STEIN_URL_EMB')

def get_stein_enb() -> list:
  enbed_data = get_stein(stein_url_enbedding)
  
  value_list = []
  for data in enbed_data:
    # dictのキーを削除
    value = [val for val in data.values()]
    value_list.append(value)


def get_stein(stein_url: str) -> list:
  response = requests.get(
    stein_url,
  )
  
  if not response.ok:
    raise Exception(f"HTTP Error: {response.status_code} - {response.reason}")
  
  return response.json()


if __name__ == '__main__':
  value_list = []
  datas = get_stein(stein_url)
  for data in datas:
    value = [value for value in data.values()]
    value_list.append(value)
  
  print(value_list)