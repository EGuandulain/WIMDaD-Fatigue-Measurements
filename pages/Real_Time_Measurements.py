import streamlit as st
import serial
from datetime import datetime, timedelta
import numpy as np
import time
import pandas as pd
import os


st.set_page_config(
	page_title = 'Fatigue Measurements',
	layout = 'wide'
	)

# Initialize serial connection
ser = None

try:
    ser = serial.Serial('COM4', 9600)
except serial.SerialException as e:
    st.error(f"SerialException: {e}")
    st.stop()

# Initialize Streamlit app
st.title("Fatigue Tests Measurements")

# Create input fields for Probe IDs
probe_ids = {}
for i in range(4):
    probe_ids[f"Probe {i+1}"] = st.text_input(f"Enter ID for Probe {i+1}", f"Probe {i+1}")

# Create a placeholder for data
data_dict = {
    'Probe 1': [],
    'Probe 2': [],
    'Probe 3': [],
    'Probe 4': [],
}

# Create a line chart for visualization
chart = st.line_chart(data_dict)
# Create columns for buttons
col1, col2 = st.columns([5, 4])


# Display previous results if available
existing_df = pd.read_csv("time_results.csv")
results_df = pd.DataFrame(columns=["Probe ID", "Time"])


savefilename = 'current_data%s.csv' % datetime.utcnow().strftime('%Y-%m-%d %H-%M-%S-%f')[:-3]


if not existing_df.empty:
    col2.header("Time Results: ")
    col2.dataframe(existing_df, width=400)

# Create a button to start the streamlit app
start_button = col1.button("Run Test")

# Create a button to stop the streamlit app
#stop_button = col2.button("Stop")
# Initialize DataFrame outside the loop
data_df = pd.DataFrame(columns=["Timestamp", "Probe 1", "Probe 2", "Probe 3", "Probe 4"])


# Display the initial DataFrame
table = col1.dataframe(data_df, width= 500, height= 200)

results_dfs = []

# Main Streamlit loop
if start_button:
    start_time = datetime.utcnow()
    probes_opened = 0
    while probes_opened < 4:
        #if stop_button:
        #    st.error("Test Stopped.")
        #    break
        
        try:
            data = ser.readline().decode().rstrip()
            analog_values = list(map(float, data.split(',')))
        except serial.SerialException as e:
            st.error(f"SerialException: {e}")
            break
        except Exception as e:
            st.error(f"Error: {e}")
            break

        coefficients = np.array([-4.04017470e-16, 4.61191660e-14, 1.47595178e-09, 8.85547458e-06, 5.31811572e-04])

        processed_values = [np.polyval(coefficients, val) * 1000 for val in analog_values]
        timestamp = datetime.utcnow()

        # Append new data to the DataFrame
        new_row = pd.Series({"Timestamp": timestamp, "Probe 1": processed_values[0], "Probe 2": processed_values[1], 
                             "Probe 3": processed_values[2], "Probe 4": processed_values[3]})
        
        data_df = pd.concat([data_df, pd.DataFrame([new_row])], ignore_index=True)
        
        # Update the displayed DataFrame
        table.dataframe(data_df)

        # Append new data to the placeholders
        for i, probe in enumerate(['Probe 1', 'Probe 2', 'Probe 3', 'Probe 4']):
            data_dict[probe].append(processed_values[i])

        # Update the line chart with the new data
        chart.line_chart(data_dict, use_container_width=True)



        # Check for probe breakage
        for i, value in enumerate(processed_values):
            if value <= 0.9 and probe_ids[f"Probe {i+1}"] not in results_df["Probe ID"].values:
                probe_id = probe_ids[f"Probe {i+1}"]
                st.write(f'Probe {i+1} ({probe_id}) opened.')
                time_taken = timestamp - start_time
                results_df = pd.concat([results_df, pd.DataFrame({"Probe ID": [probe_ids[f"Probe {i+1}"] ], "Time": [time_taken]})], ignore_index=True)
                st.write(f"Time taken for Probe {i+1} ({probe_id}) to break: {time_taken}")
                probes_opened += 1


        # Wait for a short duration before reading the next data
        time.sleep(0.1)

    # Display Results DataFrame
    # Concatenate the new DataFrame with the existing DataFrame
    concatenated_df = pd.concat([existing_df, results_df], ignore_index=True)
    concatenated_df.to_csv('time_results.csv', index=False)
    # Rename columns of data_df to probe IDs
    data_df = data_df.rename(columns={"Probe 1": probe_ids["Probe 1"],
                                    "Probe 2": probe_ids["Probe 2"],
                                    "Probe 3": probe_ids["Probe 3"],
                                    "Probe 4": probe_ids["Probe 4"]})

    # Save data_df to CSV with the updated column names

    data_df.to_csv('.\current data\current_data_%s.csv' % datetime.utcnow().strftime('%Y-%m-%d %H-%M-%S-%f')[:-3], index=False)

    st.write("Test finished. All 4 probes open")

# Close the serial connection when the Streamlit app is stopped
if ser and ser.is_open:
    ser.close()

