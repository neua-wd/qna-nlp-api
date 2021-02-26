from flask_restful import Resource, reqparse

from models.Template import Template


class TemplateController(Resource):
    def get(self):
        try:
            return Template().find_all()
        except Exception as e:
            return { 'error': e.args }