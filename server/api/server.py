import threading
import requests
import argparse

from flask import Flask, abort, request, jsonify
from flask_cors import CORS
from db.execptions import UserNotFoundException
from db.interaction.interaction import DbInteraction

from utils import config_parser


class Server:

    def __init__(self, host, port, db_host, db_port, db_user, db_password, db_name):
        self.host = host
        self.port = port

        self.db_interaction = DbInteraction(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_password,
            db_name=db_name,
            rebuild_db=False
        )

        self.app = Flask(__name__)
        CORS(self.app)
        #self.app.add_url_rule('/shutdown', view_func=self.shutdown)
        self.app.add_url_rule('/', view_func=self.get_home)
        self.app.add_url_rule('/home', view_func=self.get_home)
        self.app.add_url_rule('/add_user', view_func=self.add_user, methods=['POST'])
        self.app.add_url_rule('/add_request', view_func=self.add_request, methods=['POST'])
        self.app.add_url_rule('/get_last4_requests', view_func=self.get_last4_requests)
        self.app.add_url_rule('/auth', view_func=self.auth, methods=['POST'])
        self.app.add_url_rule('/get_all_users_info', view_func=self.get_all_users_info)
        self.app.add_url_rule('/edit_user_info/<phone>', view_func=self.edit_user_info, methods=['PUT'])


        self.app.register_error_handler(404, self.page_not_found)

    def page_not_found(self, err_description):
        return jsonify(error=str(err_description)), 404

    def run_server(self):
        self.server = threading.Thread(target=self.app.run, kwargs={'host': self.host, 'port': self.port})
        self.server.start()
        return self.server

    def shutdown_server(self):
        requests.get(f'http://{self.host}:{self.port}/shutdown')

    def shutdown(self):
        terminate_func = request.environ.get('werkzeug.server.shutdown')
        if terminate_func:
            terminate_func()

    def get_home(self):
        return 'Hello, api server'

    def get_data(self):
        data = self.db_interaction.get_all_users_info()
        if data:
            return data, 200
        else:
            abort(404, description='Data not found')

    def add_user(self):
        request_body = dict(request.json)
        phone = request_body['login']
        response = self.db_interaction.add_user(
            last_name=request_body["last_name"],
            first_name=request_body["first_name"],
            otch=request_body["otch"],
            login=request_body["login"],
            password=request_body["password"],
            email=request_body["email"]
        )
        return response, 201

    def add_request(self):
        request_body = dict(request.json)
        response = self.db_interaction.add_request(
            request_body
        )
        return response, 201

    def get_last4_requests(self):
        response = self.db_interaction.get_last4_requests()
        return response, 201

    def auth(self):
        request_body = dict(request.json)
        response = self.db_interaction.auth(
            request_body
        )
        return response, 201

    def get_all_users_info(self):
        try:
            user_info = self.db_interaction.get_all_users_info()
            return user_info, 200

        except UserNotFoundException:
            abort(404, description='User not found')


    def edit_user_info(self, phone):
        request_body = dict(request.json)
        new_phone = request_body['phone']
        try:
            self.db_interaction.edit_user_info(
                phone=phone,
                new_phone=new_phone,
            )
            return f'Success edited {phone}', 200
        except UserNotFoundException:
            abort(404, description='User not found')

#-----------------------------------------------------------------------------------

    def add_news(self):
        request_body = dict(request.json)
        headline = request_body['headline']
        information = request_body['information']
        self.db_interaction.add_news(
            headline=headline,
            information=information
        )
        return f'Success added news: {headline}', 201

    def get_news(self, headline):
        try:
            news_info = self.db_interaction.get_news(headline)
            return news_info, 200
        except UserNotFoundException:
            abort(404, description='News not found')


    def edit_news(self, headline):
        request_body = dict(request.json)
        new_headline = request_body['headline']
        new_information = request_body['information']
        try:
            self.db_interaction.edit_news(
                headline=headline,
                new_headline=new_headline,
                new_information=new_information
            )
            return f'Success edited news: {headline}', 200
        except UserNotFoundException:
            abort(404, description='News not found')

    def del_news(self, headline):
        try:
            self.db_interaction.del_news(headline)
            return '', 204
        except UserNotFoundException:
            abort(404, description='News not found')

    def get_all_news(self):
        try:
            news_list = self.db_interaction.get_all_news()
            return news_list, 200

        except UserNotFoundException:
            abort(404, description='News not found')



    # def auth(self):
    #     request_body = dict(request.json)
    #     code = request_body['code']
    #     user_id = request_body['user_id']
    #     response = self.db_interaction.auth(
    #         code=code,
    #         user_id=user_id
    #     )
    #     return response


if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--config', type=str, dest='config')

    # args = parser.parse_args()

    config = config_parser('D:/work/server_city_portal/server/api/config.txt')

    server_host = config['SERVER_HOST']
    server_port = config['SERVER_PORT']

    db_host = config['DB_HOST']
    db_port = config['DB_PORT']
    db_user = config['DB_USER']
    db_password = config['DB_PASSWORD']
    db_name = config['DB_NAME']

    server = Server(
        host=server_host,
        port=server_port,
        db_host=db_host,
        db_port=db_port,
        db_user=db_user,
        db_password=db_password,
        db_name=db_name
    )
    server.run_server()