
from flask import Flask, request, jsonify
from data_m import users, accounts, valid_tokens
import uuid

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    username = data.get("username")
    password = data.get("password")

    if users.get(username) == password:
        token = str(uuid.uuid4())
        valid_tokens.add(token)
        return jsonify({"message": "Login successful", "token": token}), 200

    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/')
def login_form():
    return '''
        <h2>Login</h2>
        <form method="POST" action="/login">
            <label>Username:</label>
            <input type="text" name="username"><br><br>
            <label>Password:</label>
            <input type="password" name="password"><br><br>
            <input type="submit" value="Login">
        </form>
    '''


def token_required(f):
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token or token not in valid_tokens:
            return jsonify({"message": "Unauthorized"}), 401
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper


@app.route('/accounts', methods=['GET'])
@token_required
def get_accounts():
    return jsonify(accounts), 200


@app.route('/accounts/<int:account_id>/status', methods=['POST'])
@token_required
def update_status(account_id):
    data = request.get_json()
    new_status = data.get("status")

    for acc in accounts:
        if acc["id"] == account_id:
            acc["status"] = new_status
            return jsonify({"message": "Status updated"}), 200

    return jsonify({"message": "Account not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
