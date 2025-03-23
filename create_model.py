import pickle
from sklearn.linear_model import LinearRegression
import numpy as np

# Create a simple linear regression model
model = LinearRegression()

# Create some sample training data
X = np.array([[25, 20.1, 1, 0],  # age, bmi, children, smoker
              [35, 23.4, 2, 1],
              [45, 25.7, 0, 0],
              [55, 28.3, 3, 1]])
y = np.array([5000, 15000, 8000, 20000])  # insurance costs

# Train the model
model.fit(X, y)

# Save the model
with open('insurancemodelf.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Model created and saved successfully!")