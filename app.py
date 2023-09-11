from flask import Flask, request, jsonify, session, redirect, make_response
from flask_session import Session
import os
import bcrypt
from pymongo import MongoClient
import torch
from torchvision.models import mobilenet_v2
import albumentations as A
from albumentations.pytorch import ToTensorV2
from datetime import timedelta
from color import *

# DB connection
client = MongoClient("mongodb+srv://sudo:sudo@atlascluster.e7pmjep.mongodb.net/")
user = client["user"]
user_info = user.info
img_data = user.img
app = Flask(__name__)

# Session config
app.secret_key = "ms_team1"
app.permanent_session_lifetime = timedelta(days=30)
app.config["SESSION_COOKIE_NAME"] = "cookie"
app.config["SESSION_TYPE"] = "filesystem"

Session(app)


@app.route("/sign-up", methods=["POST"])
def sign_up():
    info = request.json  # => front
    username = info["username"]
    email = info["email"]
    pw = info["pw"]
    gender = 0 if info["gender"] == "남성" else 1
    info["gender"] = gender
    hashed_pw = bcrypt.hashpw(pw.encode("utf-8"), bcrypt.gensalt())
    existing_user = user_info.find_one({"username": username, "email": email})
    if existing_user:
        return {
            "msg": "User with the same username and id already exists. Try another one."
        }
    else:
        info["pw"] = hashed_pw.decode("utf-8")
        user_info.insert_one(info)
        res = {"msg": "User registration has been successfully done."}
        return jsonify(res), 200


@app.route("/sign-in", methods=["GET", "POST"])
def sign_in():
    info = request.json
    email = info["email"]
    pw = info["pw"]
    user = user_info.find_one({"email": email})  # From db
    if user:
        if bcrypt.checkpw(pw.encode("utf-8"), user["pw"].encode("utf-8")):
            session["email"] = email
            gender = 0 if user["gender"] == "남성" else 1
            session["gender"] = gender
            print(gender)
            print(session["email"])
            res = make_response(jsonify({"msg": "Sign-in successful!"}), 200)
            res.set_cookie("gender", gender)
            return jsonify({"msg": "Sign-in successful!"}), 200
        else:
            print("sth wrong")
            return jsonify({"msg": "Invalid email or password."}), 401


@app.route("/logout")
def logout():
    session.clear()
    session.pop("email", None)
    res = make_response(redirect("http://localhost:8501"))
    res.delete_cookie("user_token")
    return res


# @app.route("/")
# def index():
#     if "email" in session:
#         pass
#     else:
#         return redirect("http://localhost:8501")


@app.route("/process-image", methods=["POST"])
def process_image():
    print(request.cookies.get("gender"))
    try:
        uploaded_file = request.files["image"]
        print("Uploaded Filename:", uploaded_file.filename)
        # if gender:
        #     print("male") if gender == 0 else print("female")
        # else:
        #     print("gender is empty")

        if uploaded_file.filename != "":
            # Save the uploaded file temporarily
            org_image_path = os.path.join("./temp/", uploaded_file.filename)
            uploaded_file.save(org_image_path)

            print("Saved File Path:", org_image_path)

            # Remove background
            # mask_image = remove_background(open(org_image_path, "rb").read())
            mask_image = remove_background(org_image_path)
            print("mask done") 
            # Predict color
            color_prediction = color_test(org_image_path, mask_image)

            print("predict done")
            print(color_prediction)

            return jsonify({"color": color_prediction})

    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/get-result", methods=["GET"])
def classify_item(img):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    m = mobilenet_v2()
    m.classifier[1] = torch.nn.Linear(1280, 22)
    m.load_state_dict(torch.load("./static/MobileNetV2_77.pt"))
    test_transforms = A.Compose(
        [
            A.Resize(height=640, width=640),
            A.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
            ToTensorV2(),
        ]
    )
    m.to(device)
    m.eval()

    with torch.no_grad():
        # Load and preprocess the image
        data = cv2.imread(img)
        data = test_transforms(image=data)["image"]
        data = data.unsqueeze(0).to(device)

        # Perform inference
        output = m(data)
        pred = output.argmax(dim=1, keepdim=True).item()

        # Return the predicted class index
        return jsonify({"item": pred})


if __name__ == "__main__":
    app.run(debug=True)
