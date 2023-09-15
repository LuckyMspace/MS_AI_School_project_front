from flask import Flask, request, jsonify
from flask_mail import Mail, Message
import random
import string

app = Flask(__name__)

# 가상의 DB를 나타내는 딕셔너리 (실제 DB를 사용하도록 수정해야 함)
users_db = {}

# Flask-Mail 설정
app.config["MAIL_SERVER"] = "smtp.gmail.com"  # 이메일 호스트 서버 설정
app.config["MAIL_PORT"] = 587  # 이메일 호스트 포트 설정 (일반적으로 587 또는 465)
app.config["MAIL_USE_TLS"] = True  # TLS(Transport Layer Security) 사용 여부 설정
app.config["MAIL_USERNAME"] = "kdhwi92@gmail.com"  # 이메일 계정
app.config["MAIL_PASSWORD"] = "kgnfjnorrakfrwzq"  # 이메일 비밀번호
# Mail 인스턴스 생성
mail = Mail(app)

email_verification_codes = {}


@app.route("/check_username", methods=["POST"])
def check_username():
    username = request.form.get("username")
    # 'username' 필드로 중복을 확인
    for user in users_db.values():
        if user.get("username") == username:
            return jsonify({"available": False})
    return jsonify({"available": True})


@app.route("/send_code", methods=["POST"])
def send_code():
    signup_id = request.form.get("id")
    # 'id' 필드로 중복을 확인
    if signup_id in users_db:
        return jsonify({"available": False})

    # 이메일 인증 코드 생성 함수
    def generate_verification_code():
        # 4자리 숫자로 된 랜덤 코드 생성
        return "".join(random.choices(string.digits, k=4))

    # 이메일 보내기 함수
    def send_email(signup_id, verification_code):
        msg = Message("이메일 인증 코드", sender="help@example.com", recipients=[signup_id])
        msg.body = f"인증 코드: {verification_code}"
        mail.send(msg)

    # 이메일 인증 코드 생성
    verification_code = generate_verification_code()
    # 이메일 보내기 함수 호출
    send_email(signup_id, verification_code)
    # email_verification_codes 딕셔너리에 저장
    email_verification_codes[signup_id] = verification_code
    return jsonify(
        {
            "available": True,
            "message": "이메일로 인증 코드가 전송되었습니다.",
            "verification_code": verification_code,
        }
    )


@app.route("/verify", methods=["POST"])
def verify():
    signup_id = request.form.get("signup_id")
    entered_code = request.form.get("verification_code")
    stored_verification_code = email_verification_codes.get(signup_id)
    if not stored_verification_code:
        return jsonify({"message": "인증 코드를 요청하지 않았거나 유효하지 않습니다."}), 400
    if stored_verification_code == entered_code:
        return jsonify({"message": "인증 코드가 유효합니다. 이메일이 성공적으로 인증되었습니다."}), 200
    else:
        return jsonify({"message": "인증 코드가 유효하지 않습니다. 다시 확인하세요."}), 400


@app.route("/signup", methods=["POST"])
def signup():
    signup_data = request.form
    username = signup_data.get("username")
    id = signup_data.get("id")
    password = signup_data.get("password")
    gender = signup_data.get("gender")

    # username과 id 중복 여부 확인
    if any(user.get("username") == username for user in users_db.values()):
        return jsonify({"message": "이미 사용 중인 닉네임입니다."}), 400

    if id in users_db:
        return jsonify({"message": "이미 사용 중인 이메일(ID)입니다."}), 400

    # 중복이 없으면 가상의 DB에 추가
    users_db[id] = {
        "username": username,
        "id": id,
        "password": password,
        "gender": gender
        # 다른 사용자 정보 필드들...
    }

    return jsonify({"message": "회원가입이 완료되었습니다."}), 200


if __name__ == "__main__":
    app.run()
