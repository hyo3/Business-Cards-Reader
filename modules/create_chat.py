from openai import OpenAI
from dotenv import load_dotenv;load_dotenv()
import os
import json

from modules.category import major_categories, subcategory, subclassification

def create_chat(string: str) -> str:

  schema = {
    "会社名": "string",
    "部署名": "string",
    "役職" : "string | null",
    "氏名": "string",
    "郵便番号": "string | null",
    "会社住所": "string | null",
    "電話番号": "string | null",
    "FAX番号": "string | null",
    "e-mailアドレス": "string | null",
    "会社ホームページ": "string | null",
    "職業分類": "string"
  }

  messages=[
      {"role": "system", "content": f"次の文字列から会社名、部署名、役職、氏名、郵便番号、会社住所、電話番号、FAX番号、e-mailアドレス、会社ホームページ、職業分類を抜き出して、JSON形式で出力してください。氏名に関して、日本語と英語での表記がある場合は、日本語表記のみ抜き出してください。JSONのスキーマは次の通りです：{schema}"},
      {"role": "user", "content": string}
  ]

  response = chat(messages)
  
  return response


def create_recommend_chat(occupation: str, occupation_task :str) -> str:
  if occupation_task == "":
    occupation_task = occupation

  schema = {
    "partners" : "list",
    "customers": "list",
    "suppliers": "list"
  }
  
  
  messages=[
    {"role": "system", "content": f"職業が{occupation}、業務内容が{occupation_task}である人の、協業者（同業者）、顧客候補や、仕入れ先候補となる職業をPythonのlistに変換して出力してください。JSONのスキーマは次の通りです：{schema}"}
  ]

  response = chat(messages)
  return get_chat_responsed_content(response)

def categorize_chat(occupation: str) -> str:
  # occupationがnullまたは、不定のときの処理が必要かも
  
  global major_categories
  global subcategory
  global subclacification
  
  schema_categorize = {
    "職業分類": "int"
  }
  
  schema_occupation = {
    "職業分類": "string"
  }
  
  major_category = major_categories
  
  major_categorize_messages = [
    {"role": "system", "content": f"職業に関する情報が与えられます。職業分類を次の項目の中から推測し、対応する数値を出力してください。：{major_category}JSONのスキーマは次の通りです：{schema_categorize}"},
      {"role": "user", "content": occupation}
  ]
  
  major_response = chat(major_categorize_messages)
  subcategorize_index = get_chat_responsed_dict(major_response)["職業分類"]
  
  sub_category = subcategory[int(subcategorize_index)]
  
  sub_categorize_messages = [
    {"role": "system", "content": f"職業に関する情報が与えられます。職業分類を次の項目の中から推測し、対応する数値を出力してください。：{sub_category}JSONのスキーマは次の通りです：{schema_categorize}"},
      {"role": "user", "content": occupation}
  ]
  sub_response = chat(sub_categorize_messages)
  subclassify_index = get_chat_responsed_dict(sub_response)["職業分類"]
  
  
  subclass = subclassification[subclassify_index]
  sub_clasify_messages = [
    {"role": "system", "content": f"職業に関する情報が与えられます。職業分類を次の項目の中から推測して出力してください。：{subclass}JSONのスキーマは次の通りです：{schema_occupation}"},
      {"role": "user", "content": occupation}
  ]
  classify_response = chat(sub_clasify_messages)
  occupation = get_chat_responsed_dict(classify_response)["職業分類"]
  
  return occupation

def chat(messages: list) -> str:

  api_key = os.getenv('OPENAI_API_KEY')
  client = OpenAI(api_key=api_key)


  response = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    response_format={ "type": "json_object" },
    messages=messages
  )

  return response

def get_chat_responsed_content(response):
  return response.choices[0].message.content

def get_chat_responsed_dict(response):
  content = get_chat_responsed_content(response)
  return json.loads(content)

if __name__ == '__main__':
  # print(create_chat("製造業　社長　テストたかし"))
  # print(create_recommend_chat("製造業", ""))
  jobs = ['医師', '教師', '弁護士', 'エンジニア', '会計士', '芸術家', '警察官', '介護福祉士', 'プログラマー', '農業従事者']
  additional_jobs = [
  '税理士',
  '経営コンサルタント',
  ]
  for job in additional_jobs:
    print(categorize_chat(job))