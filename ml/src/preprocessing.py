"""
Preprocessing Module
Handles encoding, scaling, and data splitting
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

from .config import MODELS_DIR, RANDOM_STATE, TEST_SIZE, CATEGORICAL_COLUMNS, NUMERICAL_COLUMNS


class DataPreprocessor:
    """
    Handles all data preprocessing:
    - StandardScaler for numerical columns
    - OneHotEncoder for categorical columns
    """
    
    def __init__(self):
        self.preprocessor = None
        self.feature_names = None
        self.cat_cols = []
        self.num_cols = []
    
    def create_preprocessor(self, X):
        """
        Create the preprocessing pipeline.
        
        Parameters:
            X: Features DataFrame
        """
        # Find which columns exist in our data
        self.cat_cols = [col for col in CATEGORICAL_COLUMNS if col in X.columns]
        self.num_cols = [col for col in NUMERICAL_COLUMNS if col in X.columns]
        
        print(f"Categorical columns: {len(self.cat_cols)}")
        print(f"Numerical columns: {len(self.num_cols)}")
        
        # Create transformers
        categorical_transformer = Pipeline([
            ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
        ])
        
        numerical_transformer = Pipeline([
            ('scaler', StandardScaler())
        ])
        
        # Combine transformers
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('num', numerical_transformer, self.num_cols),
                ('cat', categorical_transformer, self.cat_cols)
            ],
            remainder='drop'
        )
        
        print("Preprocessor created successfully")
        return self.preprocessor
    
    def fit_transform(self, X):
        """
        Fit the preprocessor and transform data.
        
        Parameters:
            X: Features DataFrame
            
        Returns:
            Transformed numpy array
        """
        if self.preprocessor is None:
            self.create_preprocessor(X)
        
        print("\nTransforming data...")
        X_transformed = self.preprocessor.fit_transform(X)
        
        # Get feature names
        self.feature_names = self.preprocessor.get_feature_names_out().tolist()
        
        print(f"Input shape: {X.shape}")
        print(f"Output shape: {X_transformed.shape}")
        
        return X_transformed
    
    def transform(self, X):
        """
        Transform new data using fitted preprocessor.
        
        Parameters:
            X: Features DataFrame
            
        Returns:
            Transformed numpy array
        """
        if self.preprocessor is None:
            raise ValueError("Preprocessor not fitted. Call fit_transform first.")
        
        return self.preprocessor.transform(X)
    
    def save(self, filepath=None):
        """Save the preprocessor to disk."""
        if filepath is None:
            filepath = MODELS_DIR / "preprocessor.pkl"
        
        joblib.dump({
            'preprocessor': self.preprocessor,
            'feature_names': self.feature_names,
            'cat_cols': self.cat_cols,
            'num_cols': self.num_cols
        }, filepath)
        
        print(f"Preprocessor saved to: {filepath}")
        return filepath
    
    @classmethod
    def load(cls, filepath=None):
        """Load a saved preprocessor."""
        if filepath is None:
            filepath = MODELS_DIR / "preprocessor.pkl"
        
        data = joblib.load(filepath)
        
        instance = cls()
        instance.preprocessor = data['preprocessor']
        instance.feature_names = data['feature_names']
        instance.cat_cols = data['cat_cols']
        instance.num_cols = data['num_cols']
        
        print(f"Preprocessor loaded from: {filepath}")
        return instance


def split_data(X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE):
    """
    Split data into training and testing sets.
    
    Parameters:
        X: Features array
        y: Target array
        test_size: Proportion for test set (default 0.2)
        random_state: Random seed for reproducibility
        
    Returns:
        X_train, X_test, y_train, y_test
    """
    print(f"\nSplitting data (test size = {test_size * 100}%)...")
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_state,
        stratify=y  # Keep same class distribution
    )
    
    print(f"Training set: {len(X_train)} samples")
    print(f"Test set: {len(X_test)} samples")
    
    return X_train, X_test, y_train, y_test
