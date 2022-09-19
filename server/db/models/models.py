from sqlalchemy import Column, Integer, ForeignKey, VARCHAR, UniqueConstraint, SMALLINT, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    last_name = Column(VARCHAR(100), nullable=True)
    first_name = Column(VARCHAR(100), nullable=True)
    otch = Column(VARCHAR(100), nullable=True)
    login = Column(VARCHAR(100), nullable=True)
    password = Column(VARCHAR(100), nullable=True)
    email = Column(VARCHAR(100), nullable=True)

    UniqueConstraint(id, name='user_id')


class Request(Base):
    __tablename__ = 'request'
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(VARCHAR(100), nullable=True)
    topic = Column(VARCHAR(100), nullable=True)
    category = Column(VARCHAR(100), nullable=True)
    description = Column(VARCHAR(100), nullable=True)
    url_img = Column(VARCHAR(100), nullable=True)
    date = Column(VARCHAR(100), nullable=True)
    date_create = Column(VARCHAR(100), nullable=True)
    status = Column(VARCHAR(100), nullable=True)

    UniqueConstraint(id, name='code')
    UniqueConstraint(user_id, name='user_id')


    # def __repr__(self):
    #     return f"<User(" \
    #            f"id='{self.id}'," \
    #            f"code='{self.code}'," \
    #            f"user_id='{self.user_id}'," \
    #            f")>"


#
# class News(Base):
#     __tablename__ = 'news'
#     id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
#     headline = Column(VARCHAR(200), nullable=True)
#     information = Column(VARCHAR(1000), nullable=True)
#
#     UniqueConstraint(headline, name='headline')


# class MusicalComposition(Base):
#     __tablename__ = 'musical_compositions'
#
#     id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
#     user_id = Column(Integer, ForeignKey(f'{User.__tablename__}.{User.id.name}'), nullable=False)
#     url = Column(VARCHAR(60), nullable=True)
#     user = relationship('User', backref='musical_composition')
#
#     def __repr__(self):
#         return f"<MusicalComposition(" \
#                f"id='{self.id}'," \
#                f"user_id='{self.user.id}'," \
#                f"url='{self.url}'" \
#                f")>"