import os
import pandas as pd

def load_and_process_csv(file_path):
    # Load CSV, skipping the first row which is a header comment
    df = pd.read_csv(file_path, skiprows=1)
    # Convert 'Date' column to datetime
    df['Date'] = pd.to_datetime(df['Date'])
    return df

def combine_files(file_paths):
    # Create "Electricity" and "Combine" folders in the current directory
    module_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(module_path)
    # current_dir = os.getcwd()
    # electricity_folder = os.path.join(current_dir, 'Electricity')
    # combined_folder = os.path.join(electricity_folder, 'Combine')
    combined_folder = os.path.join(current_dir, rf'Electricity\Combine')
    if not os.path.exists(combined_folder):
        os.makedirs(combined_folder)
    # os.makedirs(combined_folder, exist_ok=True)
    
    for file_path in file_paths:
        df = load_and_process_csv(file_path)

        # Process and save data by year
        for year, data in df.groupby(df['Date'].dt.year):
            year_file_path = os.path.join(combined_folder, f'Combined_Electricity_Usage_{year}.csv')

            if os.path.exists(year_file_path):
                # Load existing data and combine with new data
                existing_data = pd.read_csv(year_file_path)
                existing_data['Date'] = pd.to_datetime(existing_data['Date'])
                combined_data = pd.concat([existing_data, data], ignore_index=True).drop_duplicates(subset=['Date'])
            else:
                # Just save the new data directly if the file does not exist
                combined_data = data
            
            # Save updated combined data back to the file
            combined_data.sort_values(by='Date', inplace=True)
            combined_data.to_csv(year_file_path, index=False)
            #print(f"Updated combined electricity data for {year} saved to {year_file_path}")

    # Optionally, combine all data across all years into one file
    all_data = []
    for year_file in os.listdir(combined_folder):
        year_file_path = os.path.join(combined_folder, year_file)
        df = pd.read_csv(year_file_path)
        all_data.append(df)
    
    if all_data:  # Check if there is any data to combine
        combined_all_data = pd.concat(all_data, ignore_index=True).drop_duplicates(subset=['Date'])
        combined_all_file_path = os.path.join(combined_folder, 'Combined_Electricity_Usage_All.csv')
        combined_all_data.sort_values(by='Date', inplace=True)
        combined_all_data.to_csv(combined_all_file_path, index=False)
        #print(f"Overall combined electricity data saved to {combined_all_file_path}")

