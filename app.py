from flask import Flask
from flask_restful import Api, Resource

from resources.overview import Overview
from resources.details import Details
from resources.fact import Fact
from resources.column_names import ColumnNames

app = Flask(__name__)
api = Api(app)


api.add_resource(Overview, "/overview")
api.add_resource(Details, "/details")
api.add_resource(Fact, "/fact")
api.add_resource(ColumnNames, "/column_names")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
