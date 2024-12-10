import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import joblib

# Load the data
data = pd.read_csv('data/housing_pricing.csv')

# Prepare the data
X = data.drop(columns=['price','mainroad','guestroom','basement','hotwaterheating','airconditioning','prefarea','furnishingstatus'])
y = data['price']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

 print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")

# Save the model
joblib.dump(model, 'linear_model.pkl')
print("Model saved as 'linear_model.pkl'")
