from modules.vision_api import detect_text
from modules.create_chat import create_chat, categorize_chat
from modules.post_stein import post_stein_api, post_stein_enb
from modules.recommendation import recommend
from modules.get_embedding import get_embedding

import json
import os
import sys

from dotenv import load_dotenv;load_dotenv()
import httpx

from linebot.v3.webhook import WebhookParser
from linebot.v3.messaging import (
  AsyncApiClient,
  AsyncMessagingApi,
  Configuration,
  PushMessageRequest,
  ReplyMessageRequest,
  TextMessage,
  FlexMessage,
)
from linebot.v3.exceptions import (
  InvalidSignatureError,
)
from linebot.v3.webhooks import (
  MessageEvent,
  TextMessageContent,
  ImageMessageContent,
)
from starlette.exceptions import HTTPException
from linebot.models import TextSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackAction

from modules.message import back_massage,category_massage,chapter_name_message


channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
  print('Specify LINE_CHANNEL_SECRET as environment variable.')
  sys.exit(1)
if channel_access_token is None:
  print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
  sys.exit(1)

configuration = Configuration(
  access_token=channel_access_token
)
async_api_client = AsyncApiClient(configuration)
line_bot_api = AsyncMessagingApi(async_api_client)
parser = WebhookParser(channel_secret)

#状態管理
states = ["waiting_for_front_image", "waiting_for_back_image", "waiting_for_category", "waiting_for_chapter_name"]
message_example = {"waiting_for_back_image": back_massage,
           "waiting_for_category": category_massage,
           "waiting_for_chapter_name": chapter_name_message}
user_states_num = {}
user_states = {}
user_texts = {}
user_category = {}
user_chapter_name = {}
## =========== エクスポートしている関数 ==========

def handle_signature(body, signature):
  try:
    events = parser.parse(body, signature)
    return events
  except InvalidSignatureError:
    raise HTTPException(status_code=400, detail="Invalid signature")
  
async def events_handler(events):
  global user_states_num
  for event in events: 
    user_id = event.source.user_id
    if user_id not in user_states_num:
        user_states_num[user_id] = 0
        user_states[user_id] = states[0]
        user_category[user_id] = ""
        user_chapter_name[user_id] = ""

    if not isinstance(event, MessageEvent):
      continue
    if isinstance(event.message, ImageMessageContent):
      if user_states.get(user_id) == "waiting_for_back_image":
        await reply_sender(event.reply_token, [TextMessage(text='裏面の画像を受け付けました')])
        await process_back_image(user_id, event.message.id)
        await push_button_sender(user_id, [message_example[user_states[user_id]]])
        return 'OK'
      elif user_states.get(user_id) == "waiting_for_front_image":
        await reply_sender(event.reply_token, [TextMessage(text='画像を受け付けました')]) 
        await process_front_image(user_id, event.message.id)
        return 'OK'
      elif user_states.get(user_id) == "waiting_for_category":
        await reply_button_sender(event.reply_token, [message_example[user_states[user_id]]]) 
        return 'OK'
      else:
        await reply_button_sender(event.reply_token, [message_example[user_states[user_id]]])
        await reply_sender(event.reply_token, [TextMessage(text="チャプター名を入力してください")])
        return 'OK'
        
    if isinstance(event.message, TextMessageContent):
      if event.message.text == "スキップ" and user_states_num.get(user_id) != 0:
        if user_states_num.get(user_id)  == 3:
          user_states_num[user_id] = 0
          user_states[user_id] = states[0]
          user_chapter_name[user_id] = ""
          await reply_sender(event.reply_token, [TextMessage(text='処理中です。しばらくお待ちください。')])     
          await image_handler(event.source.user_id, user_texts[user_id]['detected_text'], user_category[user_id], user_chapter_name[user_id]) 
          user_texts[user_id] = {}       
          user_category[user_id] = ""
          user_chapter_name[user_id] = ""
          return 'OK'
        else:
          user_states_num[user_id] += 1
          user_states[user_id] = states[user_states_num[user_id]]
          await reply_button_sender(event.reply_token, [message_example[user_states[user_id]]])
      elif event.message.text == "中止":
        user_states_num[user_id] = 0
        user_states[user_id] = states[0]
        user_texts[user_id] = {}
        user_category[user_id] = ""
        user_chapter_name[user_id] = ""
        await reply_sender(event.reply_token, [TextMessage(text='中止しました。名刺のアップロードからやり直してください。')])
      elif user_states.get(user_id) == "waiting_for_category":
        user_category[user_id] = event.message.text
        user_states_num[user_id] += 1
        user_states[user_id] = states[user_states_num[user_id]]
        await reply_button_sender(event.reply_token, [message_example[user_states[user_id]]])        
        return 'OK'
      elif user_states.get(user_id) == "waiting_for_chapter_name":        
        user_chapter_name[user_id] = event.message.text
        await reply_sender(event.reply_token, [TextMessage(text='処理中です。しばらくお待ちください。')])        
        await image_handler(event.source.user_id, user_texts[user_id]['detected_text'],user_category[user_id], user_chapter_name[user_id])
        user_texts[user_id] = {}
        user_category[user_id] = ""
        user_chapter_name[user_id] = ""
      else:
        await reply_sender(event.reply_token, [TextMessage(text="画像をアップロードしてください")])
        # メッセージの送信



        # await push_button_sender(user_id, [back_massage])


        return 'OK'
    else:
      continue

  
## ========== 以下ヘルパー関数 ==========

async def reply_sender(reply_token: str, messages: list[str]):
  await line_bot_api.reply_message(
    ReplyMessageRequest(
      reply_token=reply_token,
      messages=messages
    )
  )

async def push_sender(user_id: str, messages: list[str]):
  await line_bot_api.push_message(
    PushMessageRequest(
      to=user_id,
      messages=messages
    )
  )

async def reply_button_sender(reply_token: str, messages: list[dict]):
  await line_bot_api.reply_message_with_http_info(
    ReplyMessageRequest.from_dict(
      {"replyToken" : reply_token,
      "messages" : messages}
    ), _return_http_data_only=False
  )

async def push_button_sender(user_id: str, messages: list[dict]):
  await line_bot_api.push_message_with_http_info(
    PushMessageRequest.from_dict(
      {"to" : user_id,
      "messages" : messages}
    ), _return_http_data_only=False
  )

async def process_front_image(user_id: str, message_id: str): 
  """表面の画像のOCRを実行"""
  global user_states_num  
  image_content = await get_image_content(message_id=message_id)
  try: 
    res_text = detect_text(content=image_content)


    user_states_num[user_id] += 1
    user_states[user_id] = states[user_states_num[user_id]]
    user_texts[user_id] = {'detected_text': res_text}
    return await push_button_sender(user_id, [message_example[user_states[user_id]]])

  except Exception as e:
    print(e)
    await push_sender(user_id, [TextMessage(text='OCRに失敗しました')])

async def process_back_image(user_id: str, message_id: str):
  """裏面の画像のOCRを実行"""
  global user_states_num  
  image_content = await get_image_content(message_id=message_id)
  try: 
    res_text = detect_text(content=image_content)
    user_states_num[user_id] += 1
    user_states[user_id] = states[user_states_num[user_id]]
    user_texts[user_id]['detected_text'] += res_text
    return "OK"

  except Exception as e:
    print(e)
    states_num = 0
    user_states[user_id] = states[states_num]
    await push_sender(user_id, [TextMessage(text='裏面のOCRに失敗しました。表面のアップロードからやり直してください。')])  
  
async def image_handler(user_id: str, text: str, category: str = None, chapter_name: str = None):
  global user_states_num
  user_states_num[user_id] = 0
  user_states[user_id] = states[0]

  try:
    name_card_text = create_chat(text)
    res_gpt = json.loads(name_card_text.choices[0].message.content)
    res_gpt["職業分類"] = categorize_chat(res_gpt["職業分類"])

  except Exception as e:
    print(e)
    return await push_sender(user_id, [TextMessage(text='テキスト解析に失敗しました')])
  try:
    
    # occupation = res_gpt["職業分類"]
    # people = recommend(occupation, category)
    # if len(people) > 0:
    #   text = "おすすめの人は"
    #   for name in people:
    #     text += f"、{name}様"
    #   text += "です"
    #   await push_sender(user_id, [TextMessage(text=text)])
    
    # post_stein_enb(get_embedding(occupation, category))
    res_gpt["カテゴリ"] = category
    res_gpt["チャプター名"] = chapter_name
    res = post_stein_api(res_gpt)
    print(res.status_code)
    
    if res.status_code == 200:
      return await push_sender(user_id, [TextMessage(text='データのアップロードに成功しました')])
    else:
      return await push_sender(user_id, [TextMessage(text='データのアップロードに失敗しました')])
    
  except Exception as e:
    print(e)
    return await push_sender(user_id, [TextMessage(text='データのアップロードに失敗しました')])
  
async def get_image_content(message_id: str):
  url = f"https://api-data.line.me/v2/bot/message/{message_id}/content"
  headers = {"Authorization": f"Bearer {channel_access_token}"}
  async with httpx.AsyncClient() as client:
    response = await client.get(url, headers=headers)
  if response.status_code == 200:
    return response.content
  else:
    raise HTTPException(status_code=response.status_code, detail="Failed to get image content")