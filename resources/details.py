from flask_restful import Resource


class Details(Resource):
    def get(self):
        return {
            "question": "If a book sitting on a flat table starts to move horizontally, it is most likely moving because",
            "abstractive_facts": [
                "a book is a kind of object",
                "(moving;mobile) is the opposite of (stationary;unmoving)",
                "friction is a kind of force",
                "gravity is a kind of force"
            ],
            "unification facts": [
                {
                    "text": "friction exerts force on moving objects",
                    "explanatory_score": 0.7
                }
            ],
            "hypothesis_score": 0.7
        }