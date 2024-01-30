import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(
    page_title='Fatigue Measurements',
    layout='wide'
)

# Load your CSV file
data = pd.read_csv("time_results.csv")

# Display the interactive table
selected_probe = st.sidebar.selectbox("Select Probe", data['Probe ID'])
selected_row = data[data['Probe ID'] == selected_probe]

st.write(selected_row)

# Directory containing the CSV files
directory = "./current data/"

# Specific column name to search for
column_name = selected_row['Probe ID'].iloc[0] # Assuming the selected row has only one column


# Iterate through each file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        filepath = os.path.join(directory, filename)

        # Read the CSV file into a DataFrame
        df = pd.read_csv(filepath)
        
        # Check if the column exists in the DataFrame
        if column_name in df.columns and 'Timestamp' in df.columns:
            # Plot the column against the 'Timestamp' column
            fig, ax = plt.subplots()
            #ax.scatter([1, 2, 3], [1, 2, 3])
            plt.plot(df['Timestamp'], df[column_name], label=filename)
            plt.xlabel('Timestamp')
            plt.ylabel(column_name)
            plt.title(f'{column_name} vs Timestamp')
            plt.legend()
            # Display the plot in Streamlit
            st.pyplot(fig)
