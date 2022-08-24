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


class TopicCT(db.Model):
    __tablename__ = "ct_topic"
    Id = db.Column(db.Integer, primary_key=True, unique=True)
    PartnerId = db.Column(db.Integer, index=True)
    Cover = db.Column(db.String(250), index=True)
    DefaultViewMode = db.Column(db.Integer)
    Description = db.Column(db.String(250))
    DisplayUrl = db.Column(db.String(250))
    GuideToSendMail = db.Column(db.String(250))
    IsActive = db.Column(db.Integer)
    IsIconActive = db.Column(db.Integer)
    Logo = db.Column(db.String(250))
    LogoFancyClose = db.Column(db.String(250))
    LogoSubMenu = db.Column(db.String(250))
    LogoTopicName = db.Column(db.String(250))
    TopicEmail = db.Column(db.String(250))
    TopicName = db.Column(db.String(250))
    isTopToolbar = db.Column(db.Integer)
    rownum = db.Column(db.Integer)

    def __init__(self, PartnerId, Cover, DefaultViewMode, Description, DisplayUrl, GuideToSendMail, IsActive,
                 IsIconActive, Logo, LogoFancyClose,
                 LogoSubMenu, LogoTopicName, TopicEmail, isTopToolbar, TopicName, rownum):
        self.PartnerId = PartnerId
        self.Cover = Cover
        self.DefaultViewMode = DefaultViewMode
        self.Description = Description
        self.DisplayUrl = DisplayUrl
        self.GuideToSendMail = GuideToSendMail
        self.IsActive = IsActive
        self.IsIconActive = IsIconActive
        self.Logo = Logo
        self.LogoFancyClose = LogoFancyClose
        self.LogoSubMenu = LogoSubMenu
        self.LogoTopicName = LogoTopicName
        self.TopicEmail = TopicEmail
        self.TopicName = TopicName
        self.isTopToolbar = isTopToolbar
        self.rownum = rownum


class TopicC(db.Model):
    __bind_key__ = "db2"
    __tablename__ = "c_topic"
    Id = db.Column(db.Integer, primary_key=True, unique=True)
    PartnerId = db.Column(db.Integer, index=True)
    Cover = db.Column(db.String(250), index=True)
    DefaultViewMode = db.Column(db.Integer)
    Description = db.Column(db.String(250))
    DisplayUrl = db.Column(db.String(250))
    GuideToSendMail = db.Column(db.String(250))
    IsActive = db.Column(db.Integer)
    IsIconActive = db.Column(db.Integer)
    Logo = db.Column(db.String(250))
    LogoFancyClose = db.Column(db.String(250))
    LogoSubMenu = db.Column(db.String(250))
    LogoTopicName = db.Column(db.String(250))
    TopicEmail = db.Column(db.String(250))
    TopicName = db.Column(db.String(250))
    isTopToolbar = db.Column(db.Integer)
    rownum = db.Column(db.Integer)

    def __init__(self, PartnerId, Cover, DefaultViewMode, Description, DisplayUrl, GuideToSendMail, IsActive,
                 IsIconActive, Logo, LogoFancyClose,
                 LogoSubMenu, LogoTopicName, TopicEmail, isTopToolbar, TopicName, rownum):
        self.PartnerId = PartnerId
        self.Cover = Cover
        self.DefaultViewMode = DefaultViewMode
        self.Description = Description
        self.DisplayUrl = DisplayUrl
        self.GuideToSendMail = GuideToSendMail
        self.IsActive = IsActive
        self.IsIconActive = IsIconActive
        self.Logo = Logo
        self.LogoFancyClose = LogoFancyClose
        self.LogoSubMenu = LogoSubMenu
        self.LogoTopicName = LogoTopicName
        self.TopicEmail = TopicEmail
        self.TopicName = TopicName
        self.isTopToolbar = isTopToolbar
        self.rownum = rownum


class ThreadCT(db.Model):
    __tablename__ = "ct_thread"
    Id = db.Column(db.Integer, primary_key=True, unique=True)
    PartnerId = db.Column(db.Integer, index=True)
    Avatar = db.Column(db.String(250))
    ArrZoneId = db.Column(db.String(250))
    CreatedBy = db.Column(db.String(250))
    CreatedDate = db.Column(db.String(250))
    Description = db.Column(db.Text)
    EditedBy = db.Column(db.String(250))
    ExtensionType = db.Column(db.String(250))
    ExtensionValue = db.Column(db.String(250))
    HomeAvatar = db.Column(db.String(250))
    Invisibled = db.Column(db.Integer)
    IsHot = db.Column(db.Integer)
    IsOnHome = db.Column(db.Integer)
    IsPrimary = db.Column(db.Integer)
    MetaContent = db.Column(db.Text)
    MetaKeyword = db.Column(db.Text)
    ModifiedDate = db.Column(db.String(250))
    Name = db.Column(db.String(250))
    NewsCoverId = db.Column(db.String(250))
    Ordinary = db.Column(db.Integer)
    RelationThread = db.Column(db.String(250))
    RelationZone = db.Column(db.String(250))
    SpecialAvatar = db.Column(db.String(250))
    TemplateId = db.Column(db.Integer)
    Title = db.Column(db.String(250))
    Type = db.Column(db.Integer)
    UnsignName = db.Column(db.String(250))
    Url = db.Column(db.String(250))
    ZoneId = db.Column(db.BigInteger)

    def __init__(self, PartnerId, ArrZoneId, Avatar, CreatedBy, CreatedDate, Description, EditedBy, ExtensionType,
                 ExtensionValue, HomeAvatar, Invisibled, IsHot, IsOnHome, IsPrimary, MetaContent, MetaKeyword,
                 ModifiedDate, Name, NewsCoverId, Ordinary, RelationThread, RelationZone, SpecialAvatar,
                 TemplateId, Title, Type, UnsignName, Url, ZoneId):
        self.PartnerId = PartnerId
        self.Avatar = Avatar
        self.ArrZoneId = ArrZoneId
        self.CreatedBy = CreatedBy
        self.CreatedDate = CreatedDate
        self.Description = Description
        self.EditedBy = EditedBy
        self.ExtensionType = ExtensionType
        self.ExtensionValue = ExtensionValue
        self.HomeAvatar = HomeAvatar
        self.Invisibled = Invisibled
        self.IsHot = IsHot
        self.IsOnHome = IsOnHome
        self.IsPrimary = IsPrimary
        self.MetaContent = MetaContent
        self.MetaKeyword = MetaKeyword
        self.ModifiedDate = ModifiedDate
        self.Name = Name
        self.NewsCoverId = NewsCoverId
        self.Ordinary = Ordinary
        self.RelationThread = RelationThread
        self.RelationZone = RelationZone
        self.SpecialAvatar = SpecialAvatar
        self.TemplateId = TemplateId
        self.Title = Title
        self.Type = Type
        self.UnsignName = UnsignName
        self.Url = Url
        self.ZoneId = ZoneId


class ThreadC(db.Model):
    __bind_key__ = "db2"
    __tablename__ = "c_thread"
    Id = db.Column(db.Integer, primary_key=True, unique=True)
    PartnerId = db.Column(db.Integer, index=True)
    Avatar = db.Column(db.String(250))
    ArrZoneId = db.Column(db.String(250))
    CreatedBy = db.Column(db.String(250))
    CreatedDate = db.Column(db.String(250))
    Description = db.Column(db.Text)
    EditedBy = db.Column(db.String(250))
    ExtensionType = db.Column(db.String(250))
    ExtensionValue = db.Column(db.String(250))
    HomeAvatar = db.Column(db.String(250))
    Invisibled = db.Column(db.Integer)
    IsHot = db.Column(db.Integer)
    IsOnHome = db.Column(db.Integer)
    IsPrimary = db.Column(db.Integer)
    MetaContent = db.Column(db.Text)
    MetaKeyword = db.Column(db.Text)
    ModifiedDate = db.Column(db.String(250))
    Name = db.Column(db.String(250))
    NewsCoverId = db.Column(db.String(250))
    Ordinary = db.Column(db.Integer)
    RelationThread = db.Column(db.String(250))
    RelationZone = db.Column(db.String(250))
    SpecialAvatar = db.Column(db.String(250))
    TemplateId = db.Column(db.Integer)
    Title = db.Column(db.String(250))
    Type = db.Column(db.Integer)
    UnsignName = db.Column(db.String(250))
    Url = db.Column(db.String(250))
    ZoneId = db.Column(db.BigInteger)

    def __init__(self, PartnerId, ArrZoneId, Avatar, CreatedBy, CreatedDate, Description, EditedBy, ExtensionType,
                 ExtensionValue, HomeAvatar, Invisibled, IsHot, IsOnHome, IsPrimary, MetaContent, MetaKeyword,
                 ModifiedDate, Name, NewsCoverId, Ordinary, RelationThread, RelationZone, SpecialAvatar,
                 TemplateId, Title, Type, UnsignName, Url, ZoneId):
        self.PartnerId = PartnerId
        self.Avatar = Avatar
        self.ArrZoneId = ArrZoneId
        self.CreatedBy = CreatedBy
        self.CreatedDate = CreatedDate
        self.Description = Description
        self.EditedBy = EditedBy
        self.ExtensionType = ExtensionType
        self.ExtensionValue = ExtensionValue
        self.HomeAvatar = HomeAvatar
        self.Invisibled = Invisibled
        self.IsHot = IsHot
        self.IsOnHome = IsOnHome
        self.IsPrimary = IsPrimary
        self.MetaContent = MetaContent
        self.MetaKeyword = MetaKeyword
        self.ModifiedDate = ModifiedDate
        self.Name = Name
        self.NewsCoverId = NewsCoverId
        self.Ordinary = Ordinary
        self.RelationThread = RelationThread
        self.RelationZone = RelationZone
        self.SpecialAvatar = SpecialAvatar
        self.TemplateId = TemplateId
        self.Title = Title
        self.Type = Type
        self.UnsignName = UnsignName
        self.Url = Url
        self.ZoneId = ZoneId


class TopicRelateCT(db.Model):
    __tablename__ = "ct_topic_relate"
    Id = db.Column(db.Integer, primary_key=True, unique=True)
    PartnerId = db.Column(db.BigInteger, index=True)
    DisplayUrl = db.Column(db.String(250), index=True)
    ArticleId = db.Column(db.BigInteger, index=True)

    def __init__(self, PartnerId, ArticleId, DisplayUrl):
        self.PartnerId = PartnerId
        self.DisplayUrl = DisplayUrl
        self.ArticleId = ArticleId


class TopicRelateC(db.Model):
    __bind_key__ = "db2"
    __tablename__ = "c_topic_relate"
    Id = db.Column(db.Integer, primary_key=True, unique=True)
    PartnerId = db.Column(db.BigInteger, index=True)
    DisplayUrl = db.Column(db.String(250), index=True)
    ArticleId = db.Column(db.BigInteger, index=True)

    def __init__(self, PartnerId, ArticleId, DisplayUrl):
        self.PartnerId = PartnerId
        self.DisplayUrl = DisplayUrl
        self.ArticleId = ArticleId


class ThreadRelateCT(db.Model):
    __tablename__ = "ct_thread_relate"
    Id = db.Column(db.Integer, primary_key=True, unique=True)
    PartnerId = db.Column(db.BigInteger, index=True)
    Url = db.Column(db.String(250), index=True)
    ArticleId = db.Column(db.BigInteger, index=True)

    def __init__(self, PartnerId, ArticleId, Url):
        self.PartnerId = PartnerId
        self.Url = Url
        self.ArticleId = ArticleId


class ThreadRelateC(db.Model):
    __bind_key__ = "db2"
    __tablename__ = "c_thread_relate"
    Id = db.Column(db.Integer, primary_key=True, unique=True)
    PartnerId = db.Column(db.BigInteger, index=True)
    Url = db.Column(db.String(250), index=True)
    ArticleId = db.Column(db.BigInteger, index=True)

    def __init__(self, PartnerId, ArticleId, Url):
        self.PartnerId = PartnerId
        self.Url = Url
        self.ArticleId = ArticleId


class ResourceCT(db.Model):
    __tablename__ = "ct_resources"
    Id = db.Column(db.Integer, primary_key=True, unique=True)
    Path = db.Column(db.String(250), index=True)

    def __init__(self, Path):
        self.Path = Path


class ResourceC(db.Model):
    __tablename__ = "c_resources"
    __bind_key__ = "db2"
    Id = db.Column(db.Integer, primary_key=True, unique=True)
    Path = db.Column(db.String(250), index=True)

    def __init__(self, Path):
        self.Path = Path


class ResourceRelateCT(db.Model):
    __tablename__ = "ct_resource_relate"
    Id = db.Column(db.Integer, primary_key=True, unique=True)
    ArticleId = db.Column(db.BigInteger, index=True)
    ExtraParams = db.Column(db.Text)
    Path = db.Column(db.String(250), index=True)

    def __init__(self, Path, ArticleId, ExtraParams):
        self.ArticleId = ArticleId
        self.ExtraParams = ExtraParams
        self.Path = Path


class ResourceRelateC(db.Model):
    __tablename__ = "c_resource_relate"
    __bind_key__ = "db2"
    Id = db.Column(db.Integer, primary_key=True, unique=True)
    ArticleId = db.Column(db.BigInteger, index=True)
    ExtraParams = db.Column(db.Text)
    Path = db.Column(db.String(250), index=True)

    def __init__(self, Path, ArticleId, ExtraParams):
        self.ArticleId = ArticleId
        self.ExtraParams = ExtraParams
        self.Path = Path


class AuthorCT(db.Model):
    __tablename__ = "ct_author"
    Id = db.Column(db.Integer, primary_key=True, unique=True)
    AuthorName = db.Column(db.String(250), index=True)
    AuthorDisplayName = db.Column(db.String(250), index=True)
    PartnerId = db.Column(db.Integer, index=True)
    AuthorUrl = db.Column(db.String(250), index=True)

    def __init__(self, AuthorName, AuthorDisplayName, PartnerId, AuthorUrl):
        self.PartnerId = PartnerId
        self.AuthorName = AuthorName
        self.AuthorDisplayName = AuthorDisplayName
        self.AuthorUrl = AuthorUrl


class AuthorC(db.Model):
    __tablename__ = "c_author"
    __bind_key__ = "db2"
    Id = db.Column(db.Integer, primary_key=True, unique=True)
    AuthorName = db.Column(db.String(250), index=True)
    AuthorDisplayName = db.Column(db.String(250), index=True)
    PartnerId = db.Column(db.Integer, index=True)
    AuthorUrl = db.Column(db.String(250), index=True)

    def __init__(self, AuthorName, AuthorDisplayName, PartnerId, AuthorUrl):
        self.PartnerId = PartnerId
        self.AuthorName = AuthorName
        self.AuthorDisplayName = AuthorDisplayName
        self.AuthorUrl = AuthorUrl


class AuthorRelateCT(db.Model):
    __tablename__ = "ct_author_relate"
    Id = db.Column(db.Integer, primary_key=True, unique=True)
    ArticleId = db.Column(db.BigInteger, index=True)
    AuthorUrl = db.Column(db.String(250), index=True)
    AuthorName = db.Column(db.String(250), index=True)

    def __init__(self, AuthorUrl, ArticleId, AuthorName):
        self.ArticleId = ArticleId
        self.AuthorName = AuthorName
        self.AuthorUrl = AuthorUrl


class AuthorRelateC(db.Model):
    __tablename__ = "c_author_relate"
    __bind_key__ = "db2"
    Id = db.Column(db.Integer, primary_key=True, unique=True)
    ArticleId = db.Column(db.BigInteger, index=True)
    AuthorUrl = db.Column(db.String(250), index=True)
    AuthorName = db.Column(db.String(250), index=True)

    def __init__(self, AuthorUrl, ArticleId, AuthorName):
        self.ArticleId = ArticleId
        self.AuthorName = AuthorName
        self.AuthorUrl = AuthorUrl


class ObjectCT(db.Model):
    __tablename__ = "ct_object"
    Id = db.Column(db.Integer, primary_key=True, unique=True)
    PartnerId = db.Column(db.BigInteger, index=True)
    AdStore = db.Column(db.Integer)
    AdStoreUrl = db.Column(db.String(250))
    AllThread = db.Column(db.String(250))
    AllTopic = db.Column(db.String(250))
    AllZone = db.Column(db.String(250))
    AllVideo = db.Column(db.String(250))
    Author = db.Column(db.String(250))
    AuthorId = db.Column(db.Integer)
    AuthorUrl = db.Column(db.String(250))
    Avatar = db.Column(db.String(250))
    Avatar2 = db.Column(db.String(250))
    Avatar3 = db.Column(db.String(250))
    Avatar4 = db.Column(db.String(250))
    Avatar5 = db.Column(db.Text)
    AvatarDesc = db.Column(db.Text)
    Body = db.Column(db.Text)
    DisplayInSlide = db.Column(db.Integer)
    DistributionDate = db.Column(db.String(250))
    ExpiredDate = db.Column(db.String(250))
    Extention = db.Column(db.String(250))
    ExtentionType = db.Column(db.String(250))
    ExtentionValue = db.Column(db.Text)
    InitSapo = db.Column(db.Text)
    InterviewId = db.Column(db.Integer)
    IsOnHome = db.Column(db.Integer)
    KeywordFocus = db.Column(db.String(250), index=True)
    LastModifiedDate = db.Column(db.String(250))
    LocationType = db.Column(db.Integer)
    MetaDescription = db.Column(db.Text)
    MetaKeyword = db.Column(db.Text)
    MetaNewsKeyword = db.Column(db.Text)
    MetaTitle = db.Column(db.Text)
    NewsRelation = db.Column(db.Text)
    NewsType = db.Column(db.Integer)
    OriginalId = db.Column(db.BigInteger, index=True)
    OriginalUrl = db.Column(db.Text)
    ParentNewsId = db.Column(db.BigInteger)
    Position = db.Column(db.String(250))
    PrPosition = db.Column(db.Integer)
    RollingNewsId = db.Column(db.Integer)
    Sapo = db.Column(db.Text)
    SocialTitle = db.Column(db.Text)
    Source = db.Column(db.Text)
    SourceUrl = db.Column(db.Text)
    SubTitle = db.Column(db.Text)
    Tag = db.Column(db.Text)
    TagItem = db.Column(db.Text)
    TagPrimary = db.Column(db.String(250))
    TagSubTitleId = db.Column(db.Integer)
    ThreadId = db.Column(db.Integer)
    Title = db.Column(db.String(250), index=True)
    Type = db.Column(db.Integer)
    Url = db.Column(db.Text)
    WordCount = db.Column(db.Integer)
    ZoneId = db.Column(db.BigInteger)
    isOld = db.Column(db.Integer)
    LastModifiedDateTimestamp = db.Column(db.BigInteger)  ### Primary sorter

    def __init__(self, isOld, ZoneId, WordCount, Url, Type, Title, ThreadId, TagSubTitleId, TagPrimary, TagItem, Tag,
                 SubTitle,
                 SourceUrl, Source, SocialTitle, Sapo, RollingNewsId, PrPosition, Position, ParentNewsId, OriginalUrl,
                 OriginalId,
                 NewsType, NewsRelation, MetaTitle, MetaNewsKeyword, MetaKeyword, MetaDescription, LocationType,
                 LastModifiedDate,
                 KeywordFocus, IsOnHome, InterviewId, InitSapo, ExtentionValue, ExtentionType, Extention, ExpiredDate,
                 DistributionDate,
                 DisplayInSlide, Body, AvatarDesc, Avatar5, Avatar4, Avatar3, Avatar2, Avatar, AuthorUrl, AuthorId,
                 Author, AllZone,
                 AllTopic, AllThread, AdStoreUrl, AdStore, PartnerId, AllVideo, LastModifiedDateTimestamp):
        self.PartnerId = PartnerId
        self.AdStore = AdStore
        self.AdStoreUrl = AdStoreUrl
        self.AllThread = AllThread
        self.AllTopic = AllTopic
        self.AllZone = AllZone
        self.AllVideo = AllVideo
        self.Author = Author
        self.AuthorId = AuthorId
        self.AuthorUrl = AuthorUrl
        self.Avatar = Avatar
        self.Avatar2 = Avatar2
        self.Avatar3 = Avatar3
        self.Avatar4 = Avatar4
        self.Avatar5 = Avatar5
        self.AvatarDesc = AvatarDesc
        self.Body = Body
        self.DisplayInSlide = DisplayInSlide
        self.DistributionDate = DistributionDate
        self.ExpiredDate = ExpiredDate
        self.Extention = Extention
        self.ExtentionType = ExtentionType
        self.ExtentionValue = ExtentionValue
        self.InitSapo = InitSapo
        self.InterviewId = InterviewId
        self.IsOnHome = IsOnHome
        self.isOld = isOld
        self.ZoneId = ZoneId
        self.WordCount = WordCount
        self.Url = Url
        self.Type = Type
        self.Title = Title
        self.ThreadId = ThreadId
        self.TagSubTitleId = TagSubTitleId
        self.TagPrimary = TagPrimary
        self.TagItem = TagItem
        self.Tag = Tag
        self.SubTitle = SubTitle
        self.SourceUrl = SourceUrl
        self.Source = Source
        self.SocialTitle = SocialTitle
        self.Sapo = Sapo
        self.RollingNewsId = RollingNewsId
        self.PrPosition = PrPosition
        self.Position = Position
        self.ParentNewsId = ParentNewsId
        self.OriginalUrl = OriginalUrl
        self.OriginalId = OriginalId
        self.NewsType = NewsType
        self.NewsRelation = NewsRelation
        self.MetaTitle = MetaTitle
        self.MetaNewsKeyword = MetaNewsKeyword
        self.MetaKeyword = MetaKeyword
        self.MetaDescription = MetaDescription
        self.LocationType = LocationType
        self.LastModifiedDate = LastModifiedDate
        self.KeywordFocus = KeywordFocus
        self.LastModifiedDateTimestamp = LastModifiedDateTimestamp


class ObjectC(db.Model):
    __tablename__ = "c_object"
    __bind_key__ = "db2"
    Id = db.Column(db.Integer, primary_key=True, unique=True)
    PartnerId = db.Column(db.BigInteger, index=True)
    AdStore = db.Column(db.Integer)
    AdStoreUrl = db.Column(db.String(250))
    AllThread = db.Column(db.String(250))
    AllTopic = db.Column(db.String(250))
    AllZone = db.Column(db.String(250))
    AllVideo = db.Column(db.String(250))
    Author = db.Column(db.String(250))
    AuthorId = db.Column(db.Integer)
    AuthorUrl = db.Column(db.String(250))
    Avatar = db.Column(db.String(250))
    Avatar2 = db.Column(db.String(250))
    Avatar3 = db.Column(db.String(250))
    Avatar4 = db.Column(db.String(250))
    Avatar5 = db.Column(db.Text)
    AvatarDesc = db.Column(db.Text)
    Body = db.Column(db.Text)
    DisplayInSlide = db.Column(db.Integer)
    DistributionDate = db.Column(db.String(250))
    ExpiredDate = db.Column(db.String(250))
    Extention = db.Column(db.String(250))
    ExtentionType = db.Column(db.String(250))
    ExtentionValue = db.Column(db.Text)
    InitSapo = db.Column(db.Text)
    InterviewId = db.Column(db.Integer)
    IsOnHome = db.Column(db.Integer)
    KeywordFocus = db.Column(db.String(250), index=True)
    LastModifiedDate = db.Column(db.String(250))
    LocationType = db.Column(db.Integer)
    MetaDescription = db.Column(db.Text)
    MetaKeyword = db.Column(db.Text)
    MetaNewsKeyword = db.Column(db.Text)
    MetaTitle = db.Column(db.Text)
    NewsRelation = db.Column(db.Text)
    NewsType = db.Column(db.Integer)
    OriginalId = db.Column(db.BigInteger, index=True)
    OriginalUrl = db.Column(db.Text)
    ParentNewsId = db.Column(db.BigInteger)
    Position = db.Column(db.String(250))
    PrPosition = db.Column(db.Integer)
    RollingNewsId = db.Column(db.Integer)
    Sapo = db.Column(db.Text)
    SocialTitle = db.Column(db.Text)
    Source = db.Column(db.Text)
    SourceUrl = db.Column(db.Text)
    SubTitle = db.Column(db.Text)
    Tag = db.Column(db.Text)
    TagItem = db.Column(db.Text)
    TagPrimary = db.Column(db.String(250))
    TagSubTitleId = db.Column(db.Integer)
    ThreadId = db.Column(db.Integer)
    Title = db.Column(db.String(250), index=True)
    Type = db.Column(db.Integer)
    Url = db.Column(db.Text)
    WordCount = db.Column(db.Integer)
    ZoneId = db.Column(db.BigInteger)
    isOld = db.Column(db.Integer)
    LastModifiedDateTimestamp = db.Column(db.BigInteger)  ### Primary sorter

    def __init__(self, isOld, ZoneId, WordCount, Url, Type, Title, ThreadId, TagSubTitleId, TagPrimary, TagItem, Tag,
                 SubTitle,
                 SourceUrl, Source, SocialTitle, Sapo, RollingNewsId, PrPosition, Position, ParentNewsId, OriginalUrl,
                 OriginalId,
                 NewsType, NewsRelation, MetaTitle, MetaNewsKeyword, MetaKeyword, MetaDescription, LocationType,
                 LastModifiedDate,
                 KeywordFocus, IsOnHome, InterviewId, InitSapo, ExtentionValue, ExtentionType, Extention, ExpiredDate,
                 DistributionDate,
                 DisplayInSlide, Body, AvatarDesc, Avatar5, Avatar4, Avatar3, Avatar2, Avatar, AuthorUrl, AuthorId,
                 Author, AllZone,
                 AllTopic, AllThread, AdStoreUrl, AdStore, PartnerId, AllVideo, LastModifiedDateTimestamp):
        self.PartnerId = PartnerId
        self.AdStore = AdStore
        self.AdStoreUrl = AdStoreUrl
        self.AllThread = AllThread
        self.AllTopic = AllTopic
        self.AllZone = AllZone
        self.AllVideo = AllVideo
        self.Author = Author
        self.AuthorId = AuthorId
        self.AuthorUrl = AuthorUrl
        self.Avatar = Avatar
        self.Avatar2 = Avatar2
        self.Avatar3 = Avatar3
        self.Avatar4 = Avatar4
        self.Avatar5 = Avatar5
        self.AvatarDesc = AvatarDesc
        self.Body = Body
        self.DisplayInSlide = DisplayInSlide
        self.DistributionDate = DistributionDate
        self.ExpiredDate = ExpiredDate
        self.Extention = Extention
        self.ExtentionType = ExtentionType
        self.ExtentionValue = ExtentionValue
        self.InitSapo = InitSapo
        self.InterviewId = InterviewId
        self.IsOnHome = IsOnHome
        self.isOld = isOld
        self.ZoneId = ZoneId
        self.WordCount = WordCount
        self.Url = Url
        self.Type = Type
        self.Title = Title
        self.ThreadId = ThreadId
        self.TagSubTitleId = TagSubTitleId
        self.TagPrimary = TagPrimary
        self.TagItem = TagItem
        self.Tag = Tag
        self.SubTitle = SubTitle
        self.SourceUrl = SourceUrl
        self.Source = Source
        self.SocialTitle = SocialTitle
        self.Sapo = Sapo
        self.RollingNewsId = RollingNewsId
        self.PrPosition = PrPosition
        self.Position = Position
        self.ParentNewsId = ParentNewsId
        self.OriginalUrl = OriginalUrl
        self.OriginalId = OriginalId
        self.NewsType = NewsType
        self.NewsRelation = NewsRelation
        self.MetaTitle = MetaTitle
        self.MetaNewsKeyword = MetaNewsKeyword
        self.MetaKeyword = MetaKeyword
        self.MetaDescription = MetaDescription
        self.LocationType = LocationType
        self.LastModifiedDate = LastModifiedDate
        self.KeywordFocus = KeywordFocus
        self.LastModifiedDateTimestamp = LastModifiedDateTimestamp


class ObjectRelateCT(db.Model):
    __tablename__ = "ct_object_relate"
    Id = db.Column(db.Integer, primary_key=True, unique=True)
    ArticleId = db.Column(db.BigInteger, index=True)
    PartnerId = db.Column(db.BigInteger, index=True)  ## relate object

    def __init__(self, PartnerId, ArticleId):
        self.ArticleId = ArticleId
        self.PartnerId = PartnerId


class ObjectRelateC(db.Model):
    __tablename__ = "c_object_relate"
    __bind_key__ = "db2"
    Id = db.Column(db.Integer, primary_key=True, unique=True)
    ArticleId = db.Column(db.BigInteger, index=True)
    PartnerId = db.Column(db.BigInteger, index=True)  ## relate object

    def __init__(self, PartnerId, ArticleId):
        self.ArticleId = ArticleId
        self.PartnerId = PartnerId


class TermRelateCT(db.Model):
    __tablename__ = "ct_term_relate"
    Id = db.Column(db.Integer, primary_key=True, unique=True)
    PartnerId = db.Column(db.BigInteger, index=True)
    ArticleId = db.Column(db.BigInteger, index=True)

    def __init__(self, PartnerId, ArticleId):
        self.PartnerId = PartnerId
        self.ArticleId = ArticleId


class TermRelateC(db.Model):
    __tablename__ = "c_term_relate"
    __bind_key__ = "db2"
    Id = db.Column(db.Integer, primary_key=True, unique=True)
    PartnerId = db.Column(db.BigInteger, index=True)
    ArticleId = db.Column(db.BigInteger, index=True)

    def __init__(self, PartnerId, ArticleId):
        self.PartnerId = PartnerId
        self.ArticleId = ArticleId
