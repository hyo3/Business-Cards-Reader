from openai import OpenAI
from dotenv import load_dotenv;load_dotenv()
import os


def create_chat(string: str) -> str:

  classification = [ "管理的職業従事者", "専門的・技術的職業従事者","専務従事者","販売従事者","サービス職業従事者","保安職業従事者","農林漁業従事者", "生産工程従事者","輸送・機械運転従事者","建設・採掘従事者","運搬・清掃・包装等従事者","分類不能の職業" ]
  schema = {
    "会社名": "string",
    "部署名": "string",
    "氏名": "string",
    "郵便番号": "string | null",
    "会社住所": "string | null",
    "電話番号": "string | null",
    "FAX番号": "string | null",
    "e-mailアドレス": "string | null",
    "会社ホームページ": "string | null",
    "職業分類": "string | null"
  }
  messages=[
      {"role": "system", "content": f"次の文字列から会社名、部署名、氏名、郵便番号、会社住所、電話番号、FAX番号、e-mailアドレス、会社ホームページ、職業分類を抜き出して、JSON形式で出力してください。氏名に関して、日本語と英語での表記がある場合は、日本語表記のみ抜き出してください。職業分類に関しては次の項目の中から推測してください：{classification}。JSONのスキーマは次の通りです：{schema}"},
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
  return response.choices[0].message.content


def chat(messages: list) -> str:

  api_key = os.getenv('OPENAI_API_KEY')
  client = OpenAI(api_key=api_key)


  response = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    response_format={ "type": "json_object" },
    messages=messages
  )

  return response

if __name__ == '__main__':
  print(create_chat("製造業　社長　テストたかし"))
  print(create_recommend_chat("製造業", ""))