import os
from openai import OpenAI
from dotenv import load_dotenv;load_dotenv()

def get_embedding(occupation: str, occupation_task: str) -> list:

  if occupation_task == "":
    occupation_task = occupation

  api_key = os.getenv('OPENAI_API_KEY')
  client = OpenAI(api_key=api_key)
  
  response = client.embeddings.create(
    model="text-embedding-3-small",
    input=f"職業：{occupation}, 職務内容：{occupation_task}",
    dimensions=10
  )
  
  return response.data[0].embedding


if __name__ == '__main__':
  occupation = "製造業"
  occupation_task = ""
  embedding = get_embedding(occupation, occupation_task)
  print(embedding)