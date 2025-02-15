import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import os

def preprocess_and_fit_electricity(file_path):
    # Assuming 'weather_forecast' module is available for merging weather data
    # import weather_forecast as wf

    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    # df = pd.merge(df, wf.history_df, on='Date', how='inner')
    
    # Assuming specific electricity usage and weather columns are defined here
    # Calculate 'Total_Usage'
    df['Total_Usage'] = df[['Usage TOU off-peak (kWh)', 'Usage TOU mid-peak (kWh)', 'Usage TOU on-peak (kWh)']].sum(axis=1)
    
    # Feature Engineering
    df = df.assign(Year=df['Date'].dt.year, Month=df['Date'].dt.month, Day=df['Date'].dt.day, Weekday=df['Date'].dt.weekday)
    features = ['Year', 'Month', 'Day', 'Weekday', 'Average temperature (C)']
    target = 'Total_Usage'
    
    # Data Preparation
    X = df[features].fillna(df[features].mean())
    y = df[target]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)
    
    # Model fitting with Lasso Regression
    lasso = Lasso(max_iter=10000)
    param_grid = {'alpha': np.logspace(-4, 0, 5)}
    grid_search = GridSearchCV(lasso, param_grid=param_grid, cv=5, scoring='r2')
    grid_search.fit(X_train, y_train)
    
    best_model = grid_search.best_estimator_
    y_pred = best_model.predict(X_scaled)
    
    # Evaluation
    mse = mean_squared_error(y, y_pred)
    r2 = r2_score(y, y_pred)
    
    print(f"Best Parameterss: {grid_search.best_params_}")
    print(f"MSE: {mse}, R2: {r2}")
    
    return best_model, mse, r2

def process_files_and_get_best_model_electricity(file_paths):
    results = {}
    for year, path in file_paths.items():
        _, mse, r2 = preprocess_and_fit_electricity(path)
        results[year] = {'MSE': mse, 'R2': r2}
    
    best_year = max(results, key=lambda x: results[x]['R2'])
    return results, best_year

def preprocess_and_fit_electricity_cost(file_path):
    # Assuming 'weather_forecast' module is available for merging weather data
    # import weather_forecast as wf

    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'])
    # df = pd.merge(df, wf.history_df, on='Date', how='inner')
    
    # Assuming specific electricity usage and weather columns are defined here
    # Calculate 'Total_Usage'
    df['Total_Cost'] = df[['Cost TOU off-peak ($)', 'Cost TOU mid-peak ($)', 'Cost TOU on-peak ($)']].sum(axis=1)
    
    # Feature Engineering
    df = df.assign(Year=df['Date'].dt.year, Month=df['Date'].dt.month, Day=df['Date'].dt.day, Weekday=df['Date'].dt.weekday)
    features = ['Year', 'Month', 'Day', 'Weekday', 'Average temperature (C)']
    target = 'Total_Cost'
    
    # Data Preparation
    X = df[features].fillna(df[features].mean())
    y = df[target]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)
    
    # Model fitting with Lasso Regression
    lasso = Lasso(max_iter=10000)
    param_grid = {'alpha': np.logspace(-4, 0, 5)}
    grid_search = GridSearchCV(lasso, param_grid=param_grid, cv=5, scoring='r2')
    grid_search.fit(X_train, y_train)
    
    best_model = grid_search.best_estimator_
    y_pred = best_model.predict(X_scaled)
    
    # Evaluation
    mse = mean_squared_error(y, y_pred)
    r2 = r2_score(y, y_pred)
    
    print(f"Best Parameters: {grid_search.best_params_}")
    print(f"MSE: {mse}, R2: {r2}")
    
    return best_model, mse, r2

def process_files_and_get_best_model_electricity_cost(file_paths):
    results = {}
    for year, path in file_paths.items():
        _, mse, r2 = preprocess_and_fit_electricity_cost(path)
        results[year] = {'MSE': mse, 'R2': r2}
    
    best_year = max(results, key=lambda x: results[x]['R2'])
    return results, best_year



def return_all_year():
    global results
    for key in results.keys():
        print(key)
        
# Assuming file paths are defined here for each year
# file_paths = {'2020': 'path/to/electricity_2020.csv', '2021': 'path/to/electricity_2021.csv'}
# results, best_year = process_files_and_get_best_model_electricity(file_paths)
