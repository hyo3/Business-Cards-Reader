from modules.vision_api import detect_text
from modules.create_chat import create_chat, categorize_chat
from modules.post_stein import post_stein_api, post_stein_enb
from modules.recommendation import recommend
from modules.get_embedding import get_embedding
from modules.message import text_message, image_message, back_massage,category_massage,chapter_name_message
from modules.extract_file_id import extract_file_id
from modules.google_drive import get_drive

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

class UserState:
    def __init__(self, user_id):
        self.user_id = user_id
        self.state_num = 0
        self.state = states[0]
        self.text = {}
        self.category = ""
        self.chapter_name = ""

    def reset(self):
        self.state_num = 0
        self.state = states[0]
        self.text = {}
        self.category = ""
        self.chapter_name = ""

    def next_state(self):
        self.state_num += 1
        self.state = states[self.state_num]

user_states = {}
image_map = {}

## =========== エクスポートしている関数 ==========

def handle_signature(body, signature):
  try:
    events = parser.parse(body, signature)
    return events
  except InvalidSignatureError:
    raise HTTPException(status_code=400, detail="Invalid signature")

async def events_handler(events):
  for event in events:
    print(user_states)
    user_id = event.source.user_id
    if user_id not in user_states:
        user_states[user_id] = UserState(user_id)

    user_state = user_states[user_id]
    print(user_state.state)
    print(user_state.text)
    if not isinstance(event, MessageEvent):
      continue
    if isinstance(event.message, ImageMessageContent):
      if user_state.state == "waiting_for_back_image":
        await reply_sender(event.reply_token, [text_message("裏面の画像を受け付けました")])
        await process_back_image(user_state, event.message.id)
        await push_sender(user_id, [message_example[user_state.state]])
        return 'OK'
      elif user_state.state == "waiting_for_front_image":
        await reply_sender(event.reply_token, [text_message("画像を受け付けました")])
        await process_front_image(user_state, event.message.id)
        return 'OK'
      elif user_state.state == "waiting_for_category":
        await reply_sender(event.reply_token, [message_example[user_state.state]])
        return 'OK'
      else:
        await reply_sender(event.reply_token, [message_example[user_state.state]])
        await reply_sender(event.reply_token, [text_message("チャプター名を入力してください")])
        return 'OK'

    if isinstance(event.message, TextMessageContent):
      if event.message.text == "スキップ" and user_state.state_num != 0:
        if user_state.state_num == 3:
          await reply_sender(event.reply_token, [text_message("処理中です。しばらくお待ちください。")])
          await image_handler(user_state)
          user_state.reset()
          return 'OK'
        else:
          user_state.next_state()
          await reply_sender(event.reply_token, [message_example[user_state.state]])
      elif event.message.text == "中止":
        user_state.reset()
        await reply_sender(event.reply_token, [text_message("中止しました。名刺のアップロードからやり直してください。")])
      elif user_state.state == "waiting_for_category":
        user_state.category = event.message.text
        user_state.next_state()
        await reply_sender(event.reply_token, [message_example[user_state.state]])
        return 'OK'
      elif user_state.state == "waiting_for_chapter_name":
        user_state.chapter_name = event.message.text
        await reply_sender(event.reply_token, [text_message("処理中です。しばらくお待ちください。")])
        await image_handler(user_state)
      else:
        await reply_sender(event.reply_token, [text_message("画像をアップロードしてください")])
        return 'OK'
    else:
      continue


## ========== 以下ヘルパー関数 ==========

async def reply_sender(reply_token: str, messages: list[dict]):
  await line_bot_api.reply_message_with_http_info(
    ReplyMessageRequest.from_dict(
      {"replyToken" : reply_token,
      "messages" : messages}
    ), _return_http_data_only=False
  )

async def push_sender(user_id: str, messages: list[dict]):
  await line_bot_api.push_message_with_http_info(
    PushMessageRequest.from_dict(
      {"to" : user_id,
      "messages" : messages}
    ), _return_http_data_only=False
  )

async def process_front_image(user_state: UserState, message_id: str):
  """表面の画像のOCRを実行"""
  image_content = await get_image_content(message_id=message_id)
  try:
    res_text = detect_text(content=image_content)

    user_state.next_state()
    user_state.text = {'detected_text': res_text}
    return await push_sender(user_state.user_id, [message_example[user_state.state]])

  except Exception as e:
    print(e)
    await push_sender(user_state.user_id, [text_message("表面のOCRに失敗しました。もう一度アップロードしてください。")])

async def process_back_image(user_state: UserState, message_id: str):
  """裏面の画像のOCRを実行"""
  image_content = await get_image_content(message_id=message_id)
  try:
    res_text = detect_text(content=image_content)
    user_state.next_state()
    user_state.text['detected_text'] += res_text
    return "OK"

  except Exception as e:
    print(e)
    user_state.reset()
    await push_sender(user_state.user_id, [text_message("裏面のOCRに失敗しました。もう一度アップロードしてください。")])

async def image_handler(user_state: UserState):
  try:
    print(user_state.text)
    print(user_state.text['detected_text'])
    name_card_text = create_chat(user_state.text['detected_text'])
    print("name_card_text")
    res_gpt = json.loads(name_card_text.choices[0].message.content)
    print("name_card_text")

    res_gpt["職業分類"] = categorize_chat(res_gpt["職業分類"])
    print("name_card_text")

  except Exception as e:
      print(e)
      return await handle_error(e, user_state, 'テキストの解析に失敗しました。開発元に問い合わせてください。')

  res_gpt["カテゴリ"] = user_state.category
  res_gpt["チャプター名"] = user_state.chapter_name
  people = []
  try:
      occupation = res_gpt["職業分類"]
      people = recommend(occupation, user_state.category)
  except Exception as e:
      await push_sender(user_state.user_id, [text_message("レコメンドに失敗しました")])

  if len(people) == 0:
      try:
          post_stein_api(res_gpt)
          await push_sender(user_state.user_id, [text_message("レコメンドなしで、データのアップロードが完了しました")])
          user_state.reset()
          return "ok"
      except Exception as e:
          user_state.reset()
          return await handle_error(e, user_state, 'データのアップロードに失敗しました')

  await send_recommendations(user_state, people, res_gpt)

  try:
      post_stein_api(res_gpt)
      await push_sender(user_state.user_id, [text_message("データのアップロードが完了しました")])
      user_state.reset()
      return "ok"
  except Exception as e:
      user_state.reset()
      return await handle_error(e, user_state, 'データのアップロードに失敗しました')


async def send_recommendations(user_state: UserState, people: list, res_gpt: dict):
  text = "おすすめの人"
  await push_sender(user_state.user_id, [text_message(text)])

  for index, person in enumerate(people):
      res_gpt_key = f"推薦{index+1}"
      text = f"{person['名前']}様"
      res_gpt[res_gpt_key] = text

      await push_sender(user_state.user_id, [text_message(text)])

      qr_code_url = person['QRコード']
      sheet_id = extract_file_id(qr_code_url)

      try:
          binary_data = get_drive(sheet_id)
          if binary_data is not None:
              image_map[user_state.user_id] = binary_data
              await push_sender(user_state.user_id, [image_message(user_state.user_id)])
      except Exception as e:
          print(e)
          await push_sender(user_state.user_id, [text_message("QRコード画像の表示に失敗しました。")])

async def handle_error(e: Exception, user_state: UserState, error_message: str):
    print(e)
    user_state.reset()
    return await push_sender(user_state.user_id, [text_message(error_message)])

async def get_image_content(message_id: str):
  url = f"https://api-data.line.me/v2/bot/message/{message_id}/content"
  headers = {"Authorization": f"Bearer {channel_access_token}"}
  async with httpx.AsyncClient() as client:
    response = await client.get(url, headers=headers)
  if response.status_code == 200:
    return response.content
  else:
    raise HTTPException(status_code=response.status_code, detail="Failed to get image content")
