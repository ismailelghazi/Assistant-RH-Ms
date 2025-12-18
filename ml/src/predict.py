"""
Prediction Utilities
Load model and make predictions
"""
import pandas as pd
import joblib

from .config import MODELS_DIR


class ChurnPredictor:
    """
    Load trained model and make predictions.
    Used by the FastAPI backend.
    """
    
    def __init__(self, model_path=None, preprocessor_path=None):
        """
        Initialize by loading model and preprocessor.
        """
        self.model = None
        self.model_name = None
        self.metrics = None
        self.preprocessor = None
        self.feature_names = None
        
        self.load(model_path, preprocessor_path)
    
    def load(self, model_path=None, preprocessor_path=None):
        """
        Load model and preprocessor from disk.
        """
        if model_path is None:
            model_path = MODELS_DIR / "best_model.pkl"
        if preprocessor_path is None:
            preprocessor_path = MODELS_DIR / "preprocessor.pkl"
        
        # Load model
        model_data = joblib.load(model_path)
        self.model = model_data['model']
        self.model_name = model_data['model_name']
        self.metrics = model_data['metrics']
        
        # Load preprocessor
        prep_data = joblib.load(preprocessor_path)
        self.preprocessor = prep_data['preprocessor']
        self.feature_names = prep_data['feature_names']
        
        print(f"Loaded model: {self.model_name}")
    
    def predict(self, employee_data):
        """
        Predict churn probability for one employee.
        
        Parameters:
            employee_data: Dictionary with employee features
            
        Returns:
            Dictionary with prediction results
        """
        # Convert to DataFrame
        df = pd.DataFrame([employee_data])
        
        # Preprocess
        X = self.preprocessor.transform(df)
        
        # Predict
        probability = self.model.predict_proba(X)[0, 1]
        prediction = int(probability >= 0.5)
        
        # Determine risk level
        if probability < 0.3:
            risk = "LOW"
        elif probability < 0.5:
            risk = "MEDIUM"
        elif probability < 0.7:
            risk = "HIGH"
        else:
            risk = "CRITICAL"
        
        return {
            'churn_probability': float(probability),
            'prediction': prediction,
            'risk_level': risk,
            'model_used': self.model_name
        }
    
    def predict_batch(self, employees_list):
        """
        Predict for multiple employees.
        
        Parameters:
            employees_list: List of employee dictionaries
            
        Returns:
            List of prediction results
        """
        return [self.predict(emp) for emp in employees_list]


# Global predictor instance
_predictor = None


def get_predictor():
    """Get or create the predictor instance."""
    global _predictor
    if _predictor is None:
        _predictor = ChurnPredictor()
    return _predictor


def predict_churn(employee_data):
    """
    Convenience function to predict churn.
    
    Parameters:
        employee_data: Dictionary with employee features
        
    Returns:
        Prediction result dictionary
    """
    predictor = get_predictor()
    return predictor.predict(employee_data)
