from openai import OpenAI
from dotenv import load_dotenv;load_dotenv()
import os

def create_chat(string: str) -> str:

  api_key = os.getenv('OPENAI_API_KEY')
  client = OpenAI(api_key=api_key)
  schema = {
    "会社名": "string",
    "部署名": "string",
    "氏名": "string",
    "会社住所": "string | null",
    "電話番号": "string | null",
    "e-mailアドレス": "string | null",
  }

  response = client.chat.completions.create(
    model="gpt-3-turbo",
    response_format={ "type": "json_object" },
    messages=[
      {"role": "system", "content": f"次の文字列から会社名、部署名、氏名、会社住所、電話番号、e-mailアドレスを抜き出して、JSON形式で出力してください。JSONのスキーマは次の通りです：{schema}"},
      {"role": "user", "content": string}
    ]
  )

  return response
