import requests
import os
import json

# 테스트할 이미지 파일 경로
image_path = "/Users/sang-yun/Desktop/Fashion_project/backend/cloth_model/cloth_dataset/valid/both/blouse/blouse(6).png"

# 서버 URL
server_url = "http://127.0.0.1:5000/predict"  # 서버 주소에 맞게 변경

# 이미지 파일을 열고 POST 요청으로 서버에 전송
with open(image_path, "rb") as image_file:
    print(image_file)
    # try:
    #     response = requests.post(server_url, files={"image": image_file})

    #     # 서버에서 받은 응답 처리
    #     if response.status_code == 200:
    #         try:
    #             predicted_label = response.json()
    #             print("Predicted Label:", predicted_label)
    #         except json.JSONDecodeError:
    #             print("Error: Response is not in JSON format")
        
    #     else:
    #         print("Error:", response.status_code)
            
    # except requests.exceptions.RequestException as e:
    #     print("Error: Request exception -", e)

