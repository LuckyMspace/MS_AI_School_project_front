from flask import Flask, request, jsonify
import os
from io import BytesIO
import cv2

app = Flask(__name__)


@app.route(
    "/login", methods=["POST"]
)  # HTTP POST요청 처리. login경로에 대한 routing 설정. 여기로 엔드포인트 오면 함수실행.
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    # 임시코드에 불과함. 추후에 DB에서 회원정보를 검증하는 코드로 바꿔야함.
    if email == "test@test.com" and password == "password":
        return jsonify({"message": "로그인 성공"}), 200
    else:
        return jsonify({"message": "이메일 주소와 비밀번호를 확인해주세요."}), 401


# 업로드 요청이 왔을 때 실행되는 함수
@app.route("/upload", methods=["POST"])
def upload_file():
    try:
        email = request.files["email"].read().decode("utf-8")
        style = request.files["style"].read().decode("utf-8")
        img = request.files["image"].read()

        return (
            jsonify({"message": "이미지 업로드 성공"}),
            200,
        )  # json형식의 응답을 생성하고 '메시지', '200'을 반환
    except Exception as e:
        print(e)
        print(e.type)
        print("///////////////////////////////////////////////////////")
        return jsonify({"message": "이미지 업로드 실패", "err": e}), 400


# 회원가입 Flask  / 현준님의 backend 코드임. /참고용 코드
# HJ_01

# @app.route("/sign-up", methods=["POST"])

# def sign_up():
#     info = request.json  # => front
#     username = info["username"]
#     id = info["id"]
#     pw = info["pw"]
#     gender = info["gender"]
#     existing_user = user_info.find_one({"username": username, "id": id, "pw": pw, "gender" : gender})
#     if existing_user:
#         return {
#             "msg": "User with the same username and id already exists. Try another one."
#         }

#     else:
#         user_info.insert_one(info)
#         res = {"msg": "User registration has been successfully done."}
#         return jsonify(res), 200

if __name__ == "__main__":
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    app.run(debug=True)
