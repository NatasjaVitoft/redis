from flask import Flask, request, jsonify
import redis
import json

app = Flask(__name__)

# Old code without security
# r = redis.Redis(host='localhost', port=6379, decode_responses=True)

r = redis.Redis(
    host='localhost',
    port=6379,
    password='VeryStrongPassword123', # Password should be in an ENV file for more security but this is only for test purpose
    decode_responses=True
)

@app.route('/')
def home():
    return "Redis application. Use postman or curl to make post and get calls."

@app.route('/user', methods=['POST'])
def add_user():
    data = request.json
    user_id = data.get('id')
    user_data = json.dumps(data)
    # Terminal command example : SETEX user:user123 60 '{"id": "user123", "name": "user123"}'
    r.setex(f"user:{user_id}", 60, user_data)  
    return jsonify({"message": "User has been added and will expire after 60 seconds"}), 201

@app.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    user = r.get(f"user:{user_id}")
    if user:
        return jsonify(json.loads(user)), 200
    return jsonify({"error": "User was not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)


