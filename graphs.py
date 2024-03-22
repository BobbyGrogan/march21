import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load data from CSV
df = pd.read_csv("./records.csv")

# Ensure all sales data columns are stripped of dollar signs and converted to float
df['Coffee Sales'] = pd.to_numeric(df['Coffee Sales'].str.replace('[$,]', '', regex=True))
df['Hot Chocolate Sales'] = pd.to_numeric(df['Hot Chocolate Sales'].str.replace('[$,]', '', regex=True))
df['Tea Sales'] = pd.to_numeric(df['Tea Sales'].str.replace('[$,]', '', regex=True))

# Determine the number of chunks (each of 32 rows)
num_chunks = np.ceil(len(df) / 32).astype(int)

# Days of the week for naming files
days_of_week = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

# Loop through each chunk, create a plot, and save to a file
for i in range(num_chunks):
    # Select the subset of the DataFrame for the current chunk
    start_row = i * 32
    end_row = start_row + 32
    chunk_data = df.iloc[start_row:end_row]
    chunk_data.reset_index(drop=True, inplace=True)  # Reset index for plotting
    
    # Plotting
    plt.figure(figsize=(12, 6))
    plt.plot(chunk_data.index, chunk_data['Coffee Sales'], label='Coffee Sales')
    plt.plot(chunk_data.index, chunk_data['Hot Chocolate Sales'], label='Hot Chocolate Sales')
    plt.plot(chunk_data.index, chunk_data['Tea Sales'], label='Tea Sales')

    day_name = days_of_week[i % 7]  # Loop through days of the week
    plt.title(f"Drink Sales for {day_name} Segment {i+1}")
    plt.xlabel('Index within Segment')
    plt.ylabel('Sales ($)')
    plt.legend()
    plt.tight_layout()

    # Saving the figure and data
    plt.savefig(f"./{day_name}_segment_{i+1}.png")
    plt.close()  # Close the figure to free memory

    # Optionally, save the chunk data as a CSV file for further analysis
    chunk_data.to_csv(f"./{day_name}_segment_{i+1}.csv", index=False)
