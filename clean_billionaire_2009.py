import pandas as pd
import numpy as np

def clean_billionaire_data(input_file, output_file):
    """
    Cleans the billionaire data according to the specified criteria.

    Args:
        input_file (str): Path to the input CSV file.
        output_file (str): Path to save the cleaned CSV file.
    """

    try:
        df = pd.read_csv(input_file) # Read without dtype, correct later
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        return

    # Correct the "56/58" age value
    df['Age'] = df['Age'].replace('56/58', 57)

    # Convert age to numeric, handle errors by coercing to NaN
    df['Age'] = pd.to_numeric(df['Age'], errors='coerce').astype(pd.Int64Dtype())

    # Handle missing text data
    for col in ['Name', 'Citizenship', 'Residence']:
        df[col] = df[col].fillna('Unknown')

    # Handle missing ages by imputing with country average
    country_avg_age = df.groupby('Citizenship')['Age'].mean()
    df['Age'] = df.apply(lambda row: country_avg_age[row['Citizenship']] if pd.isnull(row['Age']) else row['Age'], axis=1)

    # Drop rows with missing Net Worth or Rank
    df = df.dropna(subset=['Net Worth ($bil)', 'Rank'])

    # Export cleaned data.
    df.to_csv(output_file, index=False)
    print(f"Cleaned data saved to '{output_file}'")

# Example usage
input_file = 'data/billionaire2009.csv'
output_file = 'data/billionaire2009_cleaned.csv'
clean_billionaire_data(input_file, output_file)