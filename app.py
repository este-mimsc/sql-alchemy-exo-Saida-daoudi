from flask import Flask, jsonify, request
from config import Config
from extensions import db, migrate
from models import User, Post

def create_app(test_config=None):
    
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)
    
    @app.route("/")
    def index():
        return jsonify({"message": "Welcome Saida to the Flask + SQLAlchemy assignment"}), 200

    @app.route("/users", methods=["GET", "POST"])
    def users():
        if request.method == "GET":
            return jsonify([u.to_dict() for u in User.query.all()]), 200

        data = request.get_json()
        username = data.get("username")
        if not username:
            return jsonify({"error": "username is required"}), 400
        if User.query.filter_by(username=username).first():
            return jsonify({"error": "username already exists"}), 400

        new_user = User(username=username)
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict()), 201

    @app.route("/posts", methods=["GET", "POST"])
    def posts():
        if request.method == "GET":
            return jsonify([p.to_dict() for p in Post.query.all()]), 200

        data = request.get_json()
        title = data.get("title")
        content = data.get("content")
        user_id = data.get("user_id")

        if not all([title, content, user_id]):
            return jsonify({"error": "title, content and user_id are required"}), 400

        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "user_id does not exist"}), 400

        new_post = Post(title=title, content=content, user_id=user_id)
        db.session.add(new_post)
        db.session.commit()
        return jsonify(new_post.to_dict()), 201

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)

















# create Posts : Invoke-RestMethod -Uri http://127.0.0.1:5000/users -Method POST -ContentType "application/json" -Body '{"username":"saida"}'
# create Users : Invoke-RestMethod -Uri http://127.0.0.1:5000/posts -Method POST -ContentType "application/json" -Body '{"title":"Hello","content":"My first post","user_id":1}'
# get all users : Invoke-RestMethod -Uri http://127.0.0.1:5000/users -Method GET
# get all posts : Invoke-RestMethod -Uri http://127.0.0.1:5000/posts -Method GET