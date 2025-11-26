from app import db

class User(db.Model):
    """Represents a user who can author posts."""

    _tablename_ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)  

    posts = db.relationship("Post", back_populates="author", cascade="all, delete-orphan")

    def _repr_(self):  
        return f"<User {self.username}>"

class Post(db.Model):
    """Represents a blog post written by a user."""

    _tablename_ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False) 

    author = db.relationship("User", back_populates="posts")

    def _repr_(self):  
        return f"<Post {self.title}>"