from flask import Flask
from flask_restful import Api
import os


from controllers.OverviewController import OverviewController
from controllers.FactController import FactController
from controllers.TemplateController import TemplateController


app = Flask(__name__)
api = Api(app)


api.add_resource(OverviewController, "/overview")
api.add_resource(FactController, "/fact")
api.add_resource(TemplateController, "/templates")


port = int(os.environ.get("PORT", 80))
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
