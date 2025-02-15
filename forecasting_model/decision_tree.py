import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeRegressor

# Generate some sample data with a more linear relationship
np.random.seed(42)
X = 2 * np.random.rand(100, 1)
y = 4 + 3 * X + 1.5 * np.random.randn(100, 1)  # Linear relationship with less noise

# Sort the data for better visualization
X.sort(axis=0)

# Fit a decision tree regression model
model = DecisionTreeRegressor(max_depth=3)
model.fit(X, y)

# Make predictions using the model
X_new = np.arange(0, 2, 0.01)[:, np.newaxis]
y_pred = model.predict(X_new)

# Plot the data points
plt.scatter(X, y, label='Data points')

# Plot the decision tree regression line
plt.plot(X_new, y_pred, 'r-', label='Decision Tree Regression')

# Add labels and a legend
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.legend()

# Show the plot
plt.show()
