import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt



# Function to preprocess and fit Linear Regression, returning MSE and R2
def preprocess_and_fit(file_path,year):
    data = pd.read_csv(file_path)
    data['Date'] = pd.to_datetime(data['Date'])
    data['Day of Year'] = data['Date'].dt.dayofyear
    data['Month'] = data['Date'].dt.month
    data['Outside Temperature (°C)'] = data['Outside Temperature (°C)'].str.extract(r'(\d+\.\d+|\d+)').astype(float)
    data['Precipitation (mm)'] = data['Precipitation (mm)'].str.extract(r'(\d+\.\d+|\d+)').astype(float)
    #data.dropna(inplace=True)

    X = data[['Day of Year', 'Outside Temperature (°C)', 'Precipitation (mm)']].fillna(0)
    y = data['Water Use (m³)']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X)
    # print(len(y_pred))

    # Plotting the predictions in individual subplots as line graphs
    #fig, axs = plt.subplots(3, 1, figsize=(12, 18))
    # Plot for Actual vs Linear Regression
    
    # # annual plot #
    # plt.figure(figsize=(10, 6))
    # plt.plot(X['Day of Year'], y, label='Actual', color='green', linewidth=2) # org data
    # plt.plot(X['Day of Year'], y_pred, label='Linear Regression Prediction', color='red') # prediction
    # plt.title('Linear Regression Predictions')
    # plt.xlabel('Day of Year')
    # plt.ylabel('Water Use (m³)')
    # plt.legend()
    # plt.tight_layout()
    # #plt.show()
    # module_path = os.path.abspath(__file__)
    # current_dir = os.path.dirname(module_path)
    # fig_path = os.path.join(current_dir, '..', 'Water', 'Graph', str(year))
    # if not os.path.exists(fig_path):
    #     os.makedirs(fig_path)
    # fig_path = os.path.join(fig_path,'annual.png')
    # plt.savefig(fig_path)
    # plt.close()
    
    # # monthly plot #
    # months = sorted(data['Month'].unique())
    # for month in months:
    #     plt.figure(figsize=(10, 6))
    #     month_data = data[data['Month'] == month]
    #     plt.plot(month_data['Day of Year'], month_data['Water Use (m³)'], label='Actual', color='green', linewidth=2) # org data
    #     plt.plot(month_data['Day of Year'], model.predict(month_data[['Day of Year', 'Outside Temperature (°C)', 'Precipitation (mm)']].fillna(0)), label='Linear Regression Prediction', color='red') # prediction
    #     plt.title('Linear Regression Predictions for Month {}'.format(month))
    #     plt.xlabel('Day of Year')
    #     plt.ylabel('Water Use (m³)')
    #     plt.legend()
    #     plt.tight_layout()
    #     module_path = os.path.abspath(__file__)
    #     current_dir = os.path.dirname(module_path)
    #     fig_path = os.path.join(current_dir, '..', 'Water', 'Graph', str(year))
    #     if not os.path.exists(fig_path):
    #         os.makedirs(fig_path)
    #     fig_path = os.path.join(fig_path,'{}.png'.format(month))
    #     plt.savefig(fig_path)
    #     plt.close()
    
    mse = mean_squared_error(y, y_pred)
    r2 = r2_score(y, y_pred)
    
    return mse, r2

def process_files_and_get_years_with_good_r2(file_paths):
    # Dictionary to store results
    results = {}

    # Process each file and store results
    for year, path in file_paths.items():
        mse, r2 = preprocess_and_fit(path, year)
        results[year] = {'MSE': mse, 'R2': r2}

    # Filter years with R2 value greater than 0.2
    good_years = {year: result for year, result in results.items() if result['R2'] >= 0.2}

    return results, good_years


# Function to predict water use based on temperature and precipitation
def predict_water_use(prediction_temperature, prediction_precipitation, file_paths, good_years):
    predictions = []
    
    current_date = datetime.now()
    day_of_year = current_date.timetuple().tm_yday
    
    # Iterate through each good year and predict water use
    for year in good_years:
        # Load the dataset for the current good year
        file_path = file_paths[year]
        data = pd.read_csv(file_path)
        data['Date'] = pd.to_datetime(data['Date'])
        data['Day of Year'] = data['Date'].dt.dayofyear
        data['Outside Temperature (°C)'] = data['Outside Temperature (°C)'].str.extract(r'(\d+\.\d+|\d+)').astype(float)
        data['Precipitation (mm)'] = data['Precipitation (mm)'].str.extract(r'(\d+\.\d+|\d+)').astype(float)
        data.dropna(inplace=True)
    
        X = data[['Day of Year', 'Outside Temperature (°C)', 'Precipitation (mm)']]
        y = data['Water Use (m³)']
        
        # Train a model for the current good year
        model = LinearRegression()
        model.fit(X, y)
        
        # Create a DataFrame for prediction input with correct column names
        prediction_data = pd.DataFrame({
            'Day of Year': [day_of_year], 
            'Outside Temperature (°C)': [prediction_temperature], 
            'Precipitation (mm)': [prediction_precipitation]
        })
        
        # Predict water use and store the prediction
        predicted_water_use = model.predict(prediction_data)
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
