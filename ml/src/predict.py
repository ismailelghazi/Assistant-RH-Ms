class Predictor:
    def __init__(self):
        pass

    def predict(self, data):
        # Dummy prediction logic since original model is missing
        return {
            "churn_probability": 0.45,
            "risk_level": "Medium"
        }

def get_predictor():
    return Predictor()
