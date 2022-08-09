from app import db



class ArticleCT(db.Model):
    __tablename__ = "article"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.String(100))
    sapo = db.Column(db.String(250))

    def __init__(self, sbd, title, sapo):
        self.sapo = sapo
        self.title = title


class ArticleC(db.Model):
    __bind_key__ = "db2"
    __tablename__ = "article_c"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.String(100))
    sapo = db.Column(db.String(250))

    def __init__(self, sbd, title, sapo):
        self.sapo = sapo
        self.title = title
