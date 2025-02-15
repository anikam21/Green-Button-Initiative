import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import os

def preprocess_and_fit(file_path, year):
    data = pd.read_csv(file_path)
    data['Date'] = pd.to_datetime(data['Date'])
    data['Day of Year'] = data['Date'].dt.dayofyear    
    data['Month'] = data['Date'].dt.month
    data['Total_Usage'] = data[['Usage TOU off-peak (kWh)', 'Usage TOU mid-peak (kWh)', 'Usage TOU on-peak (kWh)']].sum(axis=1)
    data['Temperature'] = data['Average temperature (C)']  # Adjust based on your dataset

    X = data[['Day of Year', 'Temperature']].fillna(0)
    y = data['Total_Usage']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)

    y_pred = rf_model.predict(X)

    mse = mean_squared_error(y, y_pred)
    r2 = r2_score(y, y_pred)

    # Generate and save plots within the same function
    generate_and_save_plots(data, y_pred, year, rf_model)

    return mse, r2

def generate_and_save_plots(data, y_pred, year, model):
    # Annual plot
    plt.figure(figsize=(10, 6))
    plt.plot(data['Day of Year'], data['Total_Usage'], label='Actual Usage', color='green', linewidth=2)
    plt.plot(data['Day of Year'], y_pred, label='Predicted Usage', color='red', linestyle='--')
    plt.title(f'Electricity Usage Predictions for {year}')
    plt.xlabel('Day of Year')
    plt.ylabel('Total Usage (kWh)')
    plt.legend()
    plt.tight_layout()
    save_plot(year, 'annual_electricity_usage.png')

    # Monthly plots
    for month in sorted(data['Month'].unique()):
        month_data = data[data['Month'] == month]
        y_pred_month = model.predict(month_data[['Day of Year', 'Temperature']].fillna(0))
        plt.figure(figsize=(10, 6))
        plt.plot(month_data['Day of Year'], month_data['Total_Usage'], label='Actual Usage', color='green', linewidth=2)
        plt.plot(month_data['Day of Year'], y_pred_month, label='Predicted Usage', color='red', linestyle='--')
        plt.title(f'Electricity Usage Predictions for Month {month}')
        plt.xlabel('Day of Year')
        plt.ylabel('Total Usage (kWh)')
        plt.legend()
        plt.tight_layout()
        save_plot(year, f'month_{month}_electricity_usage.png')

def save_plot(year, filename):
    # Determine the current script's directory
    module_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(module_path)
    
    # Move up one directory level to check for an "Electricity" folder there
    parent_dir = os.path.dirname(current_dir)
    electricity_dir = os.path.join(parent_dir, 'Electricity')
    
    # Check if the "Electricity" folder exists in the parent directory
    if os.path.exists(electricity_dir):
        # If it does, use it to construct the path for the "Graphs" folder
        fig_path = os.path.join(electricity_dir, 'Graphs', str(year))
    else:
        # If not, revert to using the current directory to place the "Electricity" folder
        fig_path = os.path.join(current_dir, 'Electricity', 'Graphs', str(year))
    
    # Create the "Graphs" folder if it doesn't exist
    if not os.path.exists(fig_path):
        os.makedirs(fig_path)
    
    # Save the plot to the specified filename within the "Graphs" folder
    plt.savefig(os.path.join(fig_path, filename))
    plt.close()

# Example usage
# save_plot('2022', 'example_plot.png')

def process_files_and_get_best_year(file_paths):
    results = {}
    for year, path in file_paths.items():
        mse, r2 = preprocess_and_fit(path, year)
        results[year] = {'MSE': mse, 'R2': r2}
    # Find the year with the highest R2 value
    best_year = max(results, key=lambda x: results[x]['R2'])
    print(f"Best Year based on R222: {best_year}")
    for year, metrics in results.items():
        print(f"Year: {year}, MSE: {metrics['MSE']}, R2: {metrics['R2']}")
        
    return results,best_year


def preprocess_and_fit_cost(file_path, year):
    data = pd.read_csv(file_path)
    data['Date'] = pd.to_datetime(data['Date'])
    data['Day of Year'] = data['Date'].dt.dayofyear    
    data['Month'] = data['Date'].dt.month
    data['Total_Cost'] = data[['Cost TOU off-peak ($)', 'Cost TOU mid-peak ($)', 'Cost TOU on-peak ($)']].sum(axis=1)
    data['Temperature'] = data['Average temperature (C)']  # Adjust based on your dataset

    X = data[['Day of Year', 'Temperature']].fillna(0)
    y = data['Total_Cost']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)

    y_pred = rf_model.predict(X)

    mse = mean_squared_error(y, y_pred)
    r2 = r2_score(y, y_pred)

    # Generate and save plots within the same function
    generate_and_save_plots_cost(data, y_pred, year, rf_model)

    return mse, r2

def generate_and_save_plots_cost(data, y_pred, year, model):
    # Annual plot
    plt.figure(figsize=(10, 6))
    plt.plot(data['Day of Year'], data['Total_Cost'], label='Actual Cost', color='green', linewidth=2)
    plt.plot(data['Day of Year'], y_pred, label='Predicted Cost', color='red', linestyle='--')
    plt.title(f'Electricity Cost Predictions for {year}')
    plt.xlabel('Day of Year')
    plt.ylabel('Total Cost ($)')
    plt.legend()
    plt.tight_layout()
    save_plot_cost(year, 'annual_electricity_cost.png')

    # Monthly plots
    for month in sorted(data['Month'].unique()):
        month_data = data[data['Month'] == month]
        y_pred_month = model.predict(month_data[['Day of Year', 'Temperature']].fillna(0))
        plt.figure(figsize=(10, 6))
        plt.plot(month_data['Day of Year'], month_data['Total_Cost'], label='Actual Cost', color='green', linewidth=2)
        plt.plot(month_data['Day of Year'], y_pred_month, label='Predicted Cost', color='red', linestyle='--')
        plt.title(f'Electricity Cost Predictions for Month {month}')
        plt.xlabel('Day of Year')
        plt.ylabel('Total Cost ($)')
        plt.legend()
        plt.tight_layout()
        save_plot_cost(year, f'month_{month}_electricity_cost.png')

def save_plot_cost(year, filename):
    # Determine the current script's directory
    module_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(module_path)
    
    # Move up one directory level to check for an "Electricity" folder there
    parent_dir = os.path.dirname(current_dir)
    electricity_dir = os.path.join(parent_dir, 'Electricity')
    
    # Check if the "Electricity" folder exists in the parent directory
    if os.path.exists(electricity_dir):
        # If it does, use it to construct the path for the "Graphs" folder
        fig_path = os.path.join(electricity_dir, 'Graphs_cost', str(year))
    else:
        # If not, revert to using the current directory to place the "Electricity" folder
        fig_path = os.path.join(current_dir, 'Electricity', 'Graphs_cost', str(year))
    
    # Create the "Graphs" folder if it doesn't exist
    if not os.path.exists(fig_path):
        os.makedirs(fig_path)
    
    # Save the plot to the specified filename within the "Graphs" folder
    plt.savefig(os.path.join(fig_path, filename))
    plt.close()

# Example usage
# save_plot('2022', 'example_plot.png')

def process_files_and_get_best_year_cost(file_paths):
    results = {}
    for year, path in file_paths.items():
        mse, r2 = preprocess_and_fit_cost(path, year)
        results[year] = {'MSE': mse, 'R2': r2}
    # Find the year with the highest R2 value
    best_year = max(results, key=lambda x: results[x]['R2'])
    print(f"Best Year based on R2: {best_year}")
    for year, metrics in results.items():
        print(f"Year: {year}, MSE: {metrics['MSE']}, R2: {metrics['R2']}")
        
    return results,best_year

def return_all_year():
    global results
    for key in results.keys():
        print(key)

# Example usage of defining file paths and processing them
# file_paths = {
#     '2020': 'path/to/electricity_data_2020.csv',
#     '2021': 'path/to/electricity_data_2021.csv',
#     # Add more paths as needed
# }
# best_year = process_files_and_get_best_year(file_paths)
