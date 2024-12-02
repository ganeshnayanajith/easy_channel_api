# Importing necessary libraries
import ktrain
import yaml
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from pymongo import MongoClient

# Making a Connection with MongoClient
client = MongoClient("mongodb://localhost:27017/")
# Database
db = client["easy_channel_database"]
print('MongoDB connected....')
# Collection
user = db["users"]

app = Flask(__name__)
jwt = JWTManager(app)

# JWT Config
app.config["JWT_SECRET_KEY"] = ""

# Loading models for prediction
reloaded_predictor = ktrain.load_predictor('models/specialization_predictor')
instructions_predictor = ktrain.load_predictor('models/instructions_predictor')
print('Model loading done.')

instruction_list = ""

with open(r'resources/instructions.yaml') as file:
    instruction_list = yaml.load(file, Loader=yaml.FullLoader)


# Endpoint for user registration
@app.route("/register", methods=["POST"])
def register():
    email = request.json["email"]
    test = user.find_one({"email": email})
    if test:
        return jsonify(message="User Already Exist !!!"), 409
    else:
        first_name = request.json["first_name"]
        last_name = request.json["last_name"]
        password = request.json["password"]
        user_info = dict(first_name=first_name, last_name=last_name, email=email, password=password)
        user.insert_one(user_info)
        return jsonify(message="Registration successfully !!!"), 201


# Endpoint for user login
@app.route("/login", methods=["POST"])
def login():
    email = request.json["email"]
    password = request.json["password"]

    test = user.find_one({"email": email, "password": password})

    if test:
        access_token = create_access_token(identity=email)
        return jsonify(message="Login Succeeded !!!", access_token=access_token), 201
    else:
        return jsonify(message="Invalid Email or Password !!!"), 401


# Endpoint for welcome page
@app.route("/", methods=['GET'])
@jwt_required
def index():
    return jsonify(message="Welcome to Easy Channel !!!"), 200


# Endpoint for get doctor specialization
@app.route("/specializations", methods=['POST'])
@jwt_required
def getSpecialization():
    data = request.get_json()
    print('Request : ', data)
    print('Input Data : ', data['input'])
    print(reloaded_predictor.predict(data['input']))
    return jsonify(specialization=reloaded_predictor.predict(data['input'])), 200


# Endpoint for get instructions
@app.route("/instructions", methods=['POST'])
@jwt_required
def getInstructions():
    data = request.get_json()
    print('Request : ', data)
    print('Input Data : ', data['input'])
    emergency_class = instructions_predictor.predict(data['input'])
    instructions = ''
    for key, value in instruction_list.items():
        if key == emergency_class:
            instructions = value
    return jsonify(instructions=instructions), 200


if __name__ == "__main__":
    print('API Initiating....')
    app.run(host="localhost", port=int("5000"), debug=True)
