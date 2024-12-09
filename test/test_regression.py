import pytest
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# Test 1: Check if the LinearRegression model is initialized
def test_model_initialization():
    model = LinearRegression()
    assert isinstance(model, LinearRegression), "Model should be an instance of LinearRegression"

# Test 2: Check if the training process works
def test_model_training():
    X_train = np.array([[1], [2], [3], [4]])
    y_train = np.array([2, 4, 6, 8])
    model = LinearRegression()
    model.fit(X_train, y_train)
    assert hasattr(model, 'coef_'), "Model should have coefficients after training"

# Test 3: Check predictions
def test_model_prediction():
    X_train = np.array([[1], [2], [3], [4]])
    y_train = np.array([2, 4, 6, 8])
    X_test = np.array([[5], [6]])
    expected = np.array([10, 12])
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    assert np.allclose(y_pred, expected), "Predictions do not match expected values"

# Test 4: Evaluate metrics
def test_model_metrics():
    y_test = np.array([10, 12])
    y_pred = np.array([10, 11.8])
    
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    assert mse < 0.1, "Mean Squared Error should be small"
    assert 0.95 <= r2 <= 1.0, "R-squared should be close to 1 for a good fit"
