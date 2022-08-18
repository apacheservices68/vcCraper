from app import db


class TermCT(db.Model):
    __tablename__ = "ct_term"
    Id = db.Column(db.Integer, primary_key=True, unique=True)
    PartnerId = db.Column(db.BigInteger, unique=True, index=True)
    Invisibled = db.Column(db.Integer)  # Is display on search bar IMS
    Description = db.Column(db.String(250))
    ShortUrl = db.Column(db.String(150))
    SortOrder = db.Column(db.Integer)
    ParentShortUrl = db.Column(db.String(150))
    Status = db.Column(db.Integer)
    Name = db.Column(db.String(150))
    ModifiedDate = db.Column(db.String(130))
    ParentId = db.Column(db.Integer)
    Mode = db.Column(db.String(100))
    CreatedDate = db.Column(db.String(130))
    AllowComment = db.Column(db.Integer)
    ParentName = db.Column(db.String(150))
    Domain = db.Column(db.String(100))

    def __init__(self, PartnerId, Invisibled, Name, Description, ShortURL, SortOrder, ParentShortUrl, Status,
                 ModifiedDate,
                 ParentId, CreatedDate, AllowComment, ParentName, Domain, Mode):
        self.PartnerId = PartnerId
        self.Invisibled = Invisibled
        self.Name = Name
        self.Description = Description
        self.ShortURL = ShortURL
        self.SortOrder = SortOrder
        self.ParentShortUrl = ParentShortUrl
        self.Status = Status
        self.ModifiedDate = ModifiedDate
        self.ParentId = ParentId
        self.Mode = Mode
        self.CreatedDate = CreatedDate
        self.AllowComment = AllowComment
        self.ParentName = ParentName
        self.Domain = Domain


class TermC(db.Model):
    __bind_key__ = "db2"
    __tablename__ = "c_term"
    Id = db.Column(db.Integer, primary_key=True, unique=True)
    PartnerId = db.Column(db.BigInteger, unique=True, index=True)
    Invisibled = db.Column(db.Integer)  # Is display on search bar IMS
    Description = db.Column(db.String(250))
    ShortUrl = db.Column(db.String(150))
    SortOrder = db.Column(db.Integer)
    ParentShortUrl = db.Column(db.String(150))
    Status = db.Column(db.Integer)
    Name = db.Column(db.String(150))
    ModifiedDate = db.Column(db.String(130))
    ParentId = db.Column(db.Integer)
    Mode = db.Column(db.String(100))
    CreatedDate = db.Column(db.String(130))
    AllowComment = db.Column(db.Integer)
    ParentName = db.Column(db.String(150))
    Domain = db.Column(db.String(100))

    def __init__(self, PartnerId, Invisibled, Name, Description, ShortURL, SortOrder, ParentShortUrl, Status,
                 ModifiedDate,
                 ParentId, CreatedDate, AllowComment, ParentName, Domain, Mode):
        self.PartnerId = PartnerId
        self.Invisibled = Invisibled
        self.Name = Name
        self.Description = Description
        self.ShortURL = ShortURL
        self.SortOrder = SortOrder
        self.ParentShortUrl = ParentShortUrl
        self.Status = Status
        self.ModifiedDate = ModifiedDate
        self.ParentId = ParentId
        self.Mode = Mode
        self.CreatedDate = CreatedDate
        self.AllowComment = AllowComment
        self.ParentName = ParentName
        self.Domain = Domain


class TagCT(db.Model):
    __tablename__ = "ct_tag"
    Id = db.Column(db.Integer, primary_key=True, unique=True)
    PartnerId = db.Column(db.BigInteger, index=True)
    Name = db.Column(db.String(250), index=True)  # Is display on search bar IMS
    Url = db.Column(db.String(250), index=True)

    def __init__(self, PartnerId, Name, Url):
        self.PartnerId = PartnerId
        self.Name = Name
        self.Url = Url


class TagC(db.Model):
    __bind_key__ = "db2"
    __tablename__ = "c_tag"
    Id = db.Column(db.Integer, primary_key=True, unique=True)
    PartnerId = db.Column(db.BigInteger, index=True)
    Name = db.Column(db.String(250), index=True)  # Is display on search bar IMS
    Url = db.Column(db.String(250), index=True)

    def __init__(self, PartnerId, Name, Url):
        self.PartnerId = PartnerId
        self.Name = Name
        self.Url = Url


class TagRelateCT(db.Model):
    __tablename__ = "ct_tag_relate"
    Id = db.Column(db.Integer, primary_key=True, unique=True)
    PartnerId = db.Column(db.BigInteger, index=True)
    Url = db.Column(db.String(250), index=True)
    ArticleId = db.Column(db.BigInteger, index=True)

    def __init__(self, PartnerId, ArticleId, Url):
        self.PartnerId = PartnerId
        self.Url = Url
        self.ArticleId = ArticleId


class TagRelateC(db.Model):
    __bind_key__ = "db2"
    __tablename__ = "c_tag_relate"
    Id = db.Column(db.Integer, primary_key=True, unique=True)
    PartnerId = db.Column(db.BigInteger, index=True)
    Url = db.Column(db.String(250), index=True)
    ArticleId = db.Column(db.BigInteger, index=True)

    def __init__(self, PartnerId, ArticleId, Url):
        self.PartnerId = PartnerId
        self.Url = Url
        self.ArticleId = ArticleId
