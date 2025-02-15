import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from datetime import datetime
import numpy as np

# Dynamically load CSV files from "Combine" folder
folder_path = 'Combine'  # Example path to "Combine" folder
file_paths = {file.split('_')[3].split('.')[0]: os.path.join(folder_path, file) 
              for file in os.listdir(folder_path) if file.endswith('.csv')}

# Function to preprocess and fit Linear Regression, returning MSE and R2
def preprocess_and_fit(file_path):
    data = pd.read_csv(file_path)
    data['Date'] = pd.to_datetime(data['Date'])
    data['Day of Year'] = data['Date'].dt.dayofyear
    data['Outside Temperature (°C)'] = data['Outside Temperature (°C)'].str.extract(r'(\d+\.\d+|\d+)').astype(float)
    data['Precipitation (mm)'] = data['Precipitation (mm)'].str.extract(r'(\d+\.\d+|\d+)').astype(float)
    data.dropna(inplace=True)

    X = data[['Day of Year', 'Outside Temperature (°C)', 'Precipitation (mm)']]
    y = data['Water Use (m³)']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    return mse, r2

# Dictionary to store results
results = {}

# Process each file and store results
for year, path in file_paths.items():
    mse, r2 = preprocess_and_fit(path)
    results[year] = {'MSE': mse, 'R2': r2}

# Find the year with the highest R2 value
best_year = max(results, key=lambda x: results[x]['R2'])

# Function to predict water use based on temperature and precipitation
def predict_water_use(prediction_temperature, prediction_precipitation, best_year):
    # Dynamically load the best year's dataset
    file_path = file_paths[best_year]
    data = pd.read_csv(file_path)
    data['Date'] = pd.to_datetime(data['Date'])
    data['Day of Year'] = data['Date'].dt.dayofyear
    data['Outside Temperature (°C)'] = data['Outside Temperature (°C)'].str.extract(r'(\d+\.\d+|\d+)').astype(float)
    data['Precipitation (mm)'] = data['Precipitation (mm)'].str.extract(r'(\d+\.\d+|\d+)').astype(float)
    data.dropna(inplace=True)

    X = data[['Day of Year', 'Outside Temperature (°C)', 'Precipitation (mm)']]
    y = data['Water Use (m³)']
    
    model = LinearRegression()
    model.fit(X, y)
    
    current_date = datetime.now()
    day_of_year = current_date.timetuple().tm_yday
    
    # Create a DataFrame for prediction input with correct column names
    prediction_data = pd.DataFrame({
        'Day of Year': [day_of_year], 
        'Outside Temperature (°C)': [prediction_temperature], 
        'Precipitation (mm)': [prediction_precipitation]
    })
    
    predicted_water_use = model.predict(prediction_data)
    
    return predicted_water_use[0]


# Example usage of the function
prediction_temperature = 25.5  # example temperature
prediction_precipitation = 0.0  # example precipitation
predicted_water_use = predict_water_use(prediction_temperature, prediction_precipitation, best_year)

print(f"Results: {results}")
print(f"Best Year: {best_year}")
print(f"Predicted Water Use: {predicted_water_use} m³")
