from datetime import datetime

from sqlalchemy import desc
from db.client.client import MySQLConnection
from db.execptions import UrlNotFoundException, UserNotFoundException

from db.models.models import Users, Base, Request
import hashlib


class DbInteraction:

    def __init__(self, host, port, user, password, db_name, rebuild_db=False):
        self.mysql_connection = MySQLConnection(
            host=host,
            port=port,
            user=user,
            password=password,
            db_name=db_name,
            rebuild_db=rebuild_db
        )

        self.engine = self.mysql_connection.connection.engine

        if rebuild_db:
            self.create_table_users()
            self.create_table_req()

    def create_table_users(self):
        if not self.engine.dialect.has_table(self.engine, 'users'):
            Base.metadata.tables['users'].create(self.engine)
        else:
            pass
            # self.mysql_connection.execute_query('DROP TABLE IF EXISTS users')
            # Base.metadata.tables['users'].create(self.engine)


    def create_table_req(self):
        if not self.engine.dialect.has_table(self.engine, 'request'):
            Base.metadata.tables['request'].create(self.engine)
        else:
            self.mysql_connection.execute_query('DROP TABLE IF EXISTS request')
            Base.metadata.tables['request'].create(self.engine)

    def add_user(
            self,
            last_name,
            first_name,
            otch,
            login,
            password,
            email
    ):
        user = Users(
            last_name=last_name,
            first_name=first_name,
            otch=otch,
            login=login,
            password=hashlib.sha256(password.encode('UTF-8')).hexdigest(),
            email=email
        )
        userInDd = self.mysql_connection.session.query(Users).filter_by(login=login).first()
        if (userInDd):
            return {
                "code": 1,
                "body": None,
                "message": "Этот логин занят"
            }
        self.mysql_connection.session.add(user)
        return self.get_user_info(login)


    def add_request(
            self,
            request_body
    ):
        _request = Request(
            user_id=request_body["user_id"],
            topic=request_body["topic"],
            category=request_body["category"],
            description=request_body["description"],
            url_img=request_body["url_img"],
            date=request_body["date"],
            date_create=datetime.today().strftime("%d.%m.%Y"),
            status=request_body["status"],
        )

        try:
            self.mysql_connection.session.add(_request)
            self.mysql_connection.session.expire_all()
            return {
                "code": 0,
                "message": "Заявка успешна создана!"
            }
        except:
            return {
                "code": 1,
                "message": "Заявке пизда!"
            }

    def auth(self, request_body):
        userInDd = self.mysql_connection.session.query(Users).filter_by(login=request_body["login"]).first()
        if (userInDd):
            if hashlib.sha256(request_body["password"].encode('UTF-8')).hexdigest() == userInDd.password:
                return {
                    "code": 0,
                    "message": "Авторизация прошла успешно!"
                }
            else:
                return {
                    "code": 1,
                    "message": "Неверный пароль!"
                }

        else:
            return {
                "code": 1,
                "message": "Неправильный логин"
            }


    def get_user_info(self, login):

        user = self.mysql_connection.session.query(Users).filter_by(login=login).first()
        if user:
            self.mysql_connection.session.expire_all()
            return {
                "code": 0,
                "body": {
                    "id": user.id,
                    "last_name": user.last_name,
                    "first_name": user.first_name,
                    "otch": user.otch,
                    "login": user.login,
                    "password": user.password,
                    "email": user.email
                },
                "message": "Пользователь успешно создан"
            }
        else:
            raise UserNotFoundException('User not found')

    def get_last4_requests(self):
        reqs = list(map(lambda req_info: {
            "id": req_info.id,
            "user_id": req_info.user_id,
            "topic": req_info.topic,
            "category": req_info.category,
            "description": req_info.description,
            "url_img": req_info.url_img,
            "date": req_info.date,
            "date_create": req_info.date_create,
            "status": req_info.status,
        }, self.mysql_connection.session.query(Request).order_by(Request.id.desc()).limit(4).all()))
        if reqs:
            return {
                "result": reqs,
                "code": 0
            }
        else:
            raise UserNotFoundException('Reqs not found')

    def edit_user_info(self, phone,  new_phone=None,):
        user = self.mysql_connection.session.query(Users).filter_by(phone=phone).first()
        if user:
            if new_phone is not None:
                user.phone = new_phone
            return self.get_user_info(phone if new_phone is None else new_phone)
        else:
            raise UserNotFoundException('User not found')

    def get_all_users_info(self):
        users = list(map(lambda user_info: user_info.phone, self.mysql_connection.session.query(Users).all()))
        users_info = dict()
        i = 1
        for user in users:
            users_info[i] = user
            i+=1
        return users_info

    #----------------------------------------------------------------------------------------------------------


    # def auth(self, code, user_id):
    #     auth = self.mysql_connection.session.query(Auth).filter_by(user_id=user_id).first()
    #     if auth and auth.code == code:
    #         self.mysql_connection.session.expire_all()
    #         self.mysql_connection.session.query(Auth).filter_by(user_id=user_id).delete()
    #         return {'user_id': user_id, 'status': 'True'}
    #     else:
    #         return {'user_id': user_id, 'status': 'False'}







