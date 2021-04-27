from flask import Flask
from flask_restful import Api
from flask_cors import CORS
import os

from gensim.models.doc2vec import Doc2Vec
import pandas as pd

from controllers.OverviewController import OverviewController
from controllers.FactController import FactController
from controllers.TemplateController import TemplateController
from controllers.SuggestionController import SuggestionController


app = Flask(__name__)
api = Api(app)


cors = CORS(app, resources={
            r"*": {"origins":
                   ["http://localhost:3000", "https://qna-nlp.herokuapp.com"]}})

suggestion_model = Doc2Vec.load('suggestions.model')
fact_ids = pd.read_csv('fact_ids.csv')

api.add_resource(OverviewController, "/overview")
api.add_resource(FactController, "/fact")
api.add_resource(TemplateController, "/templates")
api.add_resource(SuggestionController, '/suggestions',
                 resource_class_kwargs={
                     'suggestion_model': suggestion_model,
                     'fact_ids': fact_ids})


port = int(os.environ.get("PORT", 80))
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
