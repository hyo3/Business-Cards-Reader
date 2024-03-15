back_massage  = { 
          "type":  "template",
          "altText": "This is a buttons template",
          "template": {
            "type": "buttons",
            "thumbnailImageUrl": "https://example.com/bot/images/image.jpg",
            "imageAspectRatio": "rectangle",
            "imageSize": "cover",
            "imageBackgroundColor": "#FFFFFF",
            "title": "裏面のアップロード",
            "text": "タップでカメラロールを開きます。",
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