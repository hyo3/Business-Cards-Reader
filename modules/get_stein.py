import json
import os
import requests
from dotenv import load_dotenv; load_dotenv()

stein_url = os.getenv('STEIN_URL') + "/"
stein_url_people = stein_url + 'sheet2'
stein_url_enbedding = stein_url + 'sheet3'

def get_stein_enb() -> list:
  enbed_data = get_stein(stein_url_enbedding)
  
  value_list = []
  for data in enbed_data:
    # dictのキーを削除
    value = [val for val in data.values()]
    value_list.append(list(map(float, value)))
  return value_list

def get_stein_people() -> list:
  return get_stein(stein_url_people)

def get_stein(stein_url: str) -> list:
  response = requests.get(
    stein_url,
  )
  
  if not response.ok:
    raise Exception(f"HTTP Error: {response.status_code} - {response.reason}")
  
  return response.json()


if __name__ == '__main__':
  print(get_stein_people())
  print(get_stein_enb())