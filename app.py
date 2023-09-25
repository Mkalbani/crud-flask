from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

# Create a flag to track whether tables have been created
tables_created = False

@app.before_request
def create_tables():
    global tables_created
    if not tables_created:
        db.create_all()
        tables_created = True

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = [{"id": user.id, "username": user.username} for user in users]
    return jsonify(user_list)

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')

    if not username:
        return jsonify({"message": "Username is required"}), 400

    new_user = User(username=username)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully"})

@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_user(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'GET':
        return jsonify({"id": user.id, "username": user.username})

    if request.method == 'PUT':
        data = request.get_json()
        username = data.get('username')

        if not username:
            return jsonify({"message": "Username is required"}), 400

        user.username = username
        db.session.commit()
        return jsonify({"message": "User updated successfully"})

    if request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"})

if __name__ == '__main__':
    app.run(debug=True)
