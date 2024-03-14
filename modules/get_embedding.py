import os
from openai import OpenAI
from dotenv import load_dotenv;load_dotenv()

def get_embedding(occupation: str) -> list:

  api_key = os.getenv('OPENAI_API_KEY')
  client = OpenAI(api_key=api_key)
  
  response = client.embeddings.create(
    model="text-embedding-3-small",
    input=occupation,
    dimensions=10
  )
  
  return response.data[0].embedding


if __name__ == '__main__':
  occupation = "教授"
  embedding = get_embedding(occupation)
  print(embedding)