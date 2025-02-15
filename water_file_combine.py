import pandas as pd
import numpy as np
import os

# Adjusted convert_date_fixed function to return both the date and the year
def convert_date_fixed(day_of_month, file_path):
    # Extract just the file name from the full path
    file_name = file_path.split('\\')[-1]  # Correct for Windows file paths

    # Split the file name based on spaces to extract the month and year
    # Assuming file name format is "Water Use For {Month} {Year}.csv"
    parts = file_name.split(' ')

    # Extract month and year, ensuring year does not include ".csv"
    month_str = parts[-2]  # Month is the second-to-last element
    year_str = parts[-1].split('.')[0]  # Year might include ".csv", so let's fix that

    # Map month abbreviations to month numbers
    month_map = {
        "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
        "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
    }

    try:
        month = month_map[month_str[:3]]
    except KeyError:
        raise ValueError(f"Invalid month string '{month_str}' extracted from file name: {file_name}")

    # Extract day part from 'Day of Month' even if it includes the month abbreviation or is in the format 'April 1'
    day_str = day_of_month.split(' ')[-1].split('-')[0]
    day = int(day_str)

    date = pd.to_datetime(f"{year_str}-{month:02d}-{day:02d}").strftime('%Y-%m-%d')
    return date, year_str





# Combine files for multiple years with data sorted by date
def combine_files(file_paths):
    # print("in water combine")
    # Get the current working directory
    #current_dir = os.getcwd()
    module_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(module_path)
    # print(current_dir)
    # Create a 'Combine' folder if it doesn't exist
    combined_folder = os.path.join(current_dir, rf'Water\Combine')
    if not os.path.exists(combined_folder):
        os.makedirs(combined_folder)

    for file_path in file_paths:
        df = pd.read_csv(file_path)
        df['Date'], df['Year'] = zip(*df['Day of Month'].apply(lambda x: convert_date_fixed(x, file_path)))
        df.drop(['Day of Month'], axis=1, inplace=True)  # Remove 'Day of Month' column, as we now have 'Year' from 'convert_date_fixed'

        year = df['Year'].iloc[0]  # Get the year from the DataFrame (assuming all data in the same file has the same year)

        # Define the combined file path within the 'Combine' folder
        combined_file_path = os.path.join(combined_folder, f'Combined_Water_Use_{year}.csv')

        # Convert the 'Date' column to datetime
        df['Date'] = pd.to_datetime(df['Date'])

        if os.path.exists(combined_file_path):
            # Read the existing combined data for the year
            existing_data = pd.read_csv(combined_file_path)

            # Convert the 'Date' column to datetime for existing data
            existing_data['Date'] = pd.to_datetime(existing_data['Date'])

            # Combine the new data with existing data and drop duplicates based on 'Date'
            combined_data = pd.concat([existing_data, df]).drop_duplicates(subset=['Date'], keep='last')

            # Sort the combined data by 'Date'
            combined_data = combined_data.sort_values(by='Date')

            # Save the updated combined data to the existing file
            combined_data.to_csv(combined_file_path, index=False)
            npy_path = combined_file_path.replace('.csv', '.npy')
            np.save(npy_path, combined_data.values)
        else:
            # If the file doesn't exist, simply save the new data
            df = df.sort_values(by='Date')  # Sort the data by 'Date'

            # Save the new data to the combined folder
            df.to_csv(combined_file_path, index=False)
            npy_path = combined_file_path.replace('.csv', '.npy')
            np.save(npy_path, df.values)




# Process new file without requiring file_path for date conversion
def process_new_file(file_path, year):
    df = pd.read_csv(file_path)
    # Assuming the date format in the file is already "yyyy-mm-dd"
    df['Date'] = pd.to_datetime(df['Date'])
    return df

# Update combined data based on the year
def update_combined_data(file_path, new_data_df, year):
    existing_file_path = f'/mnt/data/Combined_Water_Use_{year}.csv'
    if os.path.exists(existing_file_path):
        combined_df = pd.read_csv(existing_file_path)
    else:
        combined_df = pd.DataFrame(columns=new_data_df.columns)
    
    combined_df['Date'] = pd.to_datetime(combined_df['Date'])
    updated_combined_df = pd.concat([combined_df, new_data_df]).drop_duplicates(['Date'], keep='last')
    
    updated_combined_df.to_csv(existing_file_path, index=False)
    np.save(existing_file_path.replace('.csv', '.npy'), updated_combined_df.values)



