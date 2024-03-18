back_massage  = { 
          "type":  "template",
          "altText": "名刺の裏面をアップロード",
          "template": {
            "type": "buttons",
            "imageBackgroundColor": "#FFFFFF",
            "title": "名刺の裏面をアップロード",
            "text": "タップでカメラロールを開きます。裏面の情報が不要な場合は「スキップ」を押してください。",
            "defaultAction": {
              "type": "cameraRoll",
              "label": "Camera roll"
            },
            "actions": [
              {
                "type": "camera",
                "label": "カメラを起動"
              },
              {
                "type": "message",
                "label": "スキップ",
                "text": "スキップ"
              },
              {
                "type": "message",
                "label": "中止",
                "text": "中止"
              }
            ]
          }
        }

category_massage = {
  "type": "template",
  "altText": "カテゴリを入力",
  "template": {
    "type": "confirm",
    "text": "カテゴリを入力してください。不要な場合は「スキップ」を押してください。",
    "actions": [
      {
        "type": "message",
        "label": "スキップ",
        "text": "スキップ"
      },
      {
        "type": "message",
        "label": "中止",
        "text": "中止"
      }
    ]
  }
}

chapter_name_message = {
  "type": "template",
  "altText": "チャプタ名を入力",
  "template": {
    "type": "confirm",
    "text": "チャプター名を入力してください。不要な場合は「スキップ」を押してください。",
    "actions": [
      {
        "type": "message",
        "label": "スキップ",
        "text": "スキップ"
      },
      {
        "type": "message",
        "label": "中止",
        "text": "中止"
      }
    ]
  }
}