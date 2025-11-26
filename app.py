from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)

    class User(db.Model):
        __tablename__ = "users"
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(120), unique=True, nullable=False)
        posts = db.relationship("Post", backref="author", lazy=True)

        def to_dict(self):
            return {"id": self.id, "username": self.username}

    class Post(db.Model):
        __tablename__ = "posts"
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(200), nullable=False)
        content = db.Column(db.Text, nullable=False)
        user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

        def to_dict(self):
            return {
                "id": self.id,
                "title": self.title,
                "content": self.content,
                "user_id": self.user_id,
                "username": self.author.username if self.author else None,
            }

    @app.route("/")
    def index():
        return jsonify({"message": "Welcome Saida to the Flask + SQLAlchemy assignment"})

    @app.route("/users", methods=["GET", "POST"])
    def users():
        if request.method == "GET":
            all_users = User.query.all()
            return jsonify([u.to_dict() for u in all_users]), 200
        data = request.get_json()
        if not data or "username" not in data:
            return jsonify({"error": "username is required"}), 400
        if User.query.filter_by(username=data["username"]).first():
            return jsonify({"error": "username already exists"}), 409
        new_user = User(username=data["username"])
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict()), 201

    @app.route("/posts", methods=["GET", "POST"])
    def posts():
        if request.method == "GET":
            all_posts = Post.query.all()
            return jsonify([p.to_dict() for p in all_posts]), 200
        data = request.get_json()
        required = ["title", "content", "user_id"]
        if not data or not all(k in data for k in required):
            return jsonify({"error": "title, content, and user_id are required"}), 400
        user = User.query.get(data["user_id"])
        if not user:
            return jsonify({"error": "user_id does not exist"}), 404
        new_post = Post(title=data["title"], content=data["content"], user_id=user.id)
        db.session.add(new_post)
        db.session.commit()
        return jsonify(new_post.to_dict()), 201

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
