from modules.recommend_person import get_recommend_candidates
from modules.get_stein import get_stein_enb, get_stein_people
from modules.get_embedding import get_embedding
from modules.create_chat import create_recommend_chat



import json
from dotenv import load_dotenv;load_dotenv()


def recommend(occupation: str, occupation_task: str):

	gpt_occupations = create_recommend_chat(occupation, occupation_task)
	occupation_dict = json.loads(gpt_occupations)
	occupations = []
	for occupation_list in occupation_dict.values():
		occupations += occupation_list
	
	embedding_datas = get_stein_enb()
	recommend_people_index = get_recommend_people(occupations, embedding_datas)
	people_datas = get_stein_people()
	recommend_people = []

	for index in recommend_people_index:
		recommend_people.append(people_datas[index-1])
	return recommend_people


	
def get_recommend_people(occupations: list, embedding_datas: list):
	recommend_people_max = 3
	
	candidate_list = []
	for occupation in occupations:
		base = get_embedding(occupation, occupation)
		candidates = get_recommend_candidates(embedding_datas, base)
		candidate_list += candidates
  
	if len(occupations) == 0:
		max_people = 0
	else:
		max_people = len(candidate_list) // len(occupations)
		
	# 母数が小さいときの人数を決めるため
	recommend_people_max = min(recommend_people_max, max_people)

	return narrow_down_reccomend_people(candidate_list, recommend_people_max)



# indexを返す
def narrow_down_reccomend_people(candidates: list, recommend_people_max: int) -> list:
		
	results = sorted(candidates, key=lambda i: i['similarity'], reverse=True)
	
	recommend_people = []
	num = 0
	while len(recommend_people) < recommend_people_max:
		person = results[num]['index']
		if person in recommend_people:
			num += 1
			continue
		recommend_people.append(person)
		num += 1
	return recommend_people

if __name__ == '__main__':
  recommend('社長', 'ペットショップのオーナー')