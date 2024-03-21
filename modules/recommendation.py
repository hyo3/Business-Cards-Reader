from recommend_person import get_recommend_candidates
from get_stein import get_stein_enb
from get_embedding import get_embedding

from dotenv import load_dotenv;load_dotenv()

def recommend(occupations: list):
  recommend_people_max = 3
    
  enbedding_datas = get_stein_enb()

  candidate_list = []
  for occupation in occupations:
    base = get_embedding(occupation)
    candidates = get_recommend_candidates(enbedding_datas, base)
    candidate_list += candidates
    
    max_people = candidate_list // len(occupations)
    
    # 母数が小さいときの人数を決めるため
  recommend_people_max = min(recommend_people_max, max_people)
    
  get_recommend_people(candidate_list, recommend_people_max)



# indexを返す
def get_recommend_people(candidates: list, recommend_people_max: int) -> list:
    
  results = sorted(candidates, key=lambda i: i['similarity'], reverse=True)
  
  num_people = recommend_people_max
  
  if len(results) < num_people:
    num_people = len(results)
  
  recommend_people = []
  num = 0
  while len(recommend_people) < num_people:
    if results['index'] in recommend_people:
      num += 1
      continue
    recommend_people.append(results[num]['index'])
    num += 1
  
  return recommend_people
    