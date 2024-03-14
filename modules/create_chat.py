from openai import OpenAI
from dotenv import load_dotenv;load_dotenv()
import os

def create_chat(string: str) -> str:

  api_key = os.getenv('OPENAI_API_KEY')
  client = OpenAI(api_key=api_key)
  classification = ["農業・林業", "漁業","鉱業・採石業・砂利採取業","建設業","製造業","電気・ガス・熱供給・水道業","情報通信業","運輸業・郵便業","卸売業・小売業","金融業・保険業","不動産業・物品賃貸業","学術研究・専門・技術サービス業","宿泊業・飲食サービス業","生活関連サービス業・娯楽業","教育・学習支援業","医療・福祉","複合サービス事業","サービス業（他に分類されないもの）","公務（他に分類されるものを除く）","分類不能の産業" ]
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


  response = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    response_format={ "type": "json_object" },
    messages=[
      {"role": "system", "content": f"次の文字列から会社名、部署名、氏名、郵便番号、会社住所、電話番号、FAX番号、e-mailアドレス、会社ホームページ、職業分類を抜き出して、JSON形式で出力してください。氏名に関して、日本語と英語での表記がある場合は、日本語表記のみ抜き出してください。職業分類に関しては次の項目の中から推測してください：{classification}。JSONのスキーマは次の通りです：{schema}"},
      {"role": "user", "content": string}
    ]
  )

  return response
