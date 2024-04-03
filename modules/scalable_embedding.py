from get_stein import get_stein_enb, get_stein_people
from post_stein import post_stein_enb
from get_embedding import get_embedding



import json
from dotenv import load_dotenv;load_dotenv()

def scalable_embedding():
    matching_people = get_stein_people()
    matching_people_num = len(matching_people)
    print(matching_people)
    embedding_data = get_stein_enb()
    embedding_data_num = len(embedding_data)
    
    data_diff = matching_people_num - embedding_data_num
    if data_diff > 0:
        for i in range(matching_people_num - data_diff, matching_people_num):
            person = matching_people[i]
            category = person['登録カテゴリー']
            emb_data = get_embedding(category, category)
            post_stein_enb(emb_data)
            

if __name__ == '__main__':
    scalable_embedding()
            