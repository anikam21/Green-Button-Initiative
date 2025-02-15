import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import os

# Function to round predictions to the nearest multiple of 0.5
def round_to_nearest_half(number):
    return np.round(number * 2) / 2

# Function to preprocess and fit Linear Regression, returning MSE and R2
def preprocess_and_fit(file_path, year):
    data = pd.read_csv(file_path)
    # Data Cleaning and Preprocessing
    # Remove units and convert columns to numeric
    data['Outside Temperature (°C)'] = data['Outside Temperature (°C)'].str.replace(' C', '').astype(float)
    data['Precipitation (mm)'] = data['Precipitation (mm)'].str.replace(' mm', '').astype(float)
    # Convert "Date" to datetime format
    data['Date'] = pd.to_datetime(data['Date'])
    # Create a new feature 'Day of Year'
    data['Day of Year'] = data['Date'].dt.dayofyear    
    data['Month'] = data['Date'].dt.month

    # Sort by date to ensure the time series is in order
    data = data.sort_values(by='Date').reset_index(drop=True)

    # Prepare the data for Random Forest analysis
    X_full = data[['Outside Temperature (°C)', 'Precipitation (mm)']].fillna(0)  # Handling missing values
    y_full = data['Water Use (m³)']

    X = data[['Day of Year', 'Outside Temperature (°C)', 'Precipitation (mm)']]
    y = data['Water Use (m³)']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Split the full data into training and testing sets
    X_full_train, X_full_test, y_full_train, y_full_test = train_test_split(X_full, y_full, test_size=0.2, random_state=42)

    # Initialize and fit the Random Forest Regressor model with full data
    rf_model_full = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model_full.fit(X_full_train, y_full_train)

    # Generate predictions using the Random Forest model trained on full data
    y_full_raw_pred = rf_model_full.predict(X_full)

    # Apply rounding to the nearest multiple of 0.5 and ensure at least 0.5
    y_full_final_pred = np.maximum(np.array([round_to_nearest_half(pred) for pred in y_full_raw_pred]), 0.5)

    # Plotting the predictions in individual subplots as line graphs
    #fig, axs = plt.subplots(3, 1, figsize=(12, 18))
    # Plot for Actual vs Linear Regression
    
    # annual plot #
    plt.figure(figsize=(10, 6))
    plt.plot(X['Day of Year'], y, label='Actual', color='green', linewidth=2) # org data
    plt.plot(X['Day of Year'], y_full_final_pred, label='Linear Regression Prediction', color='red') # prediction
    plt.title('Linear Regression Predictions')
    plt.xlabel('Day of Year')
    plt.ylabel('Water Use (m³)')
    plt.legend()
    plt.tight_layout()
    #plt.show()
    module_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(module_path)
    fig_path = os.path.join(current_dir, '..', 'Water', 'Graph', str(year))
    if not os.path.exists(fig_path):
        os.makedirs(fig_path)
    fig_path = os.path.join(fig_path,'annual.png')
    plt.savefig(fig_path)
    plt.close()
    
    # monthly plot #
    months = sorted(data['Month'].unique())
    for month in months:
        plt.figure(figsize=(10, 6))
        month_data = data[data['Month'] == month]
        plt.plot(month_data['Day of Year'], month_data['Water Use (m³)'], label='Actual', color='green', linewidth=2) 
        # Corrected line for prediction, removing 'Day of Year' from the prediction data
        plt.plot(month_data['Day of Year'], rf_model_full.predict(month_data[['Outside Temperature (°C)', 'Precipitation (mm)']].fillna(0)), label='Random Forest Prediction', color='red') # prediction
        plt.title('Linear Regression Predictions for Month {}'.format(month))
        plt.xlabel('Day of Year')
        plt.ylabel('Water Use (m³)')
        plt.legend()
        plt.tight_layout()
        module_path = os.path.abspath(__file__)
        current_dir = os.path.dirname(module_path)
        fig_path = os.path.join(current_dir, '..', 'Water', 'Graph', str(year))
        if not os.path.exists(fig_path):
            os.makedirs(fig_path)
        fig_path = os.path.join(fig_path,'{}.png'.format(month))
        plt.savefig(fig_path)
        plt.close()

    # Evaluate the adjusted predictions on the full dataset
    mse = mean_squared_error(y_full, y_full_final_pred)
    r2 = r2_score(y_full, y_full_final_pred)
    
    return mse, r2

def process_files_and_get_years_with_good_r2(file_paths):
    # Dictionary to store results
    results = {}

    # Process each file and store results
    for year, path in file_paths.items():
        mse, r2 = preprocess_and_fit(path, year)
        results[year] = {'MSE': mse, 'R2': r2}

    # Filter years with R2 value greater than 0.2
    good_years = {year: result for year, result in results.items() if result['R2'] > 0.4}

    return results, good_years


# Function to predict water use based on temperature and precipitation
def predict_water_use(prediction_temperature, prediction_precipitation, file_paths, good_years):
    predictions = []
    
    for year in good_years:
        file_path = file_paths[year]
        data = pd.read_csv(file_path)
        
        # Data Cleaning and Preprocessing
        data['Outside Temperature (°C)'] = data['Outside Temperature (°C)'].str.replace(' C', '').astype(float)
        data['Precipitation (mm)'] = data['Precipitation (mm)'].str.replace(' mm', '').astype(float)
        data['Date'] = pd.to_datetime(data['Date'])
        data['Day of Year'] = data['Date'].dt.dayofyear
        data = data.sort_values(by='Date').reset_index(drop=True)
        
        X = data[['Day of Year', 'Outside Temperature (°C)', 'Precipitation (mm)']].fillna(0)
        y = data['Water Use (m³)']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
        rf_model.fit(X_train, y_train)
        
        current_date = datetime.now()
        day_of_year = current_date.timetuple().tm_yday
        
        prediction_data = pd.DataFrame({
            'Day of Year': [day_of_year], 
            'Outside Temperature (°C)': [prediction_temperature], 
            'Precipitation (mm)': [prediction_precipitation]
        })
        
        predicted_water_use = rf_model.predict(prediction_data)
        predictions.append(predicted_water_use[0])
    
    # Return the average prediction from all good years
    if predictions:
        return np.mean(predictions)
    else:
        return None

def return_all_year():
    global results
    for key in results.keys():
        print(key)

