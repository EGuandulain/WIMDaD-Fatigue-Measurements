import serial
import os
import time
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

os.chdir(r'C:\Users\Eduardo Guandulain\OneDrive\Escritorio\Master AIT\Student Job\Windpark Blade Project\Scripts')
print(os.getcwd())

savefilename = 'data%s.csv' % datetime.utcnow().strftime('%Y-%m-%d %H-%M-%S-%f')[:-3]

ser = serial.Serial('COM4', 9600)
plt.ion()
fig, ax1 = plt.subplots()
ax2 = ax1.twinx()

analog_line1, = ax1.plot([], [], 'b-', label='Probe 1')
analog_line2, = ax1.plot([], [], 'r-', label='Probe 2')
analog_line3, = ax1.plot([], [], 'g-', label='Probe 3')
analog_line4, = ax1.plot([], [], 'k-', label='Probe 4')

ax1.set_xlabel('Time')
ax1.set_ylabel('Current (A)')

analog_ylim_min = 0
analog_ylim_max = 12
ax1.set_ylim(analog_ylim_min, analog_ylim_max)

lines = [analog_line1, analog_line2, analog_line3, analog_line4]
labels = [line.get_label() for line in lines]
ax1.legend(lines, labels)

x_data = []
analog_data1 = []
analog_data2 = []
analog_data3 = []
analog_data4 = []


while True:
    data = ser.readline().decode().rstrip()
    analog_value1, analog_value2, analog_value3, analog_value4 = data.split(',')
    
    coefficients = np.array([-4.04017470e-16, 4.61191660e-14, 1.47595178e-09, 8.85547458e-06, 5.31811572e-04])

    x1_value = float(analog_value1) 
    x2_value = float(analog_value2)
    x3_value = float(analog_value3)
    x4_value = float(analog_value4)


    y1 = np.polyval(coefficients, x1_value)
    y2 = np.polyval(coefficients, x2_value)
    y3 = np.polyval(coefficients, x3_value)
    y4 = np.polyval(coefficients, x4_value)

    new_analog_value1 = y1 * 1000
    new_analog_value2 = y2 * 1000
    new_analog_value3 = y3 * 1000
    new_analog_value4 = y4 * 1000


    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    timestamp = str(timestamp)


    output = timestamp, analog_value1, new_analog_value1, analog_value2, new_analog_value2, analog_value3, new_analog_value3, analog_value4, new_analog_value4
    
    print(output)

    f = open((savefilename) , 'a')
    f.write(str(output) + "\n")
    f.close

    x_data.append(len(x_data))
    analog_data1.append(new_analog_value1)
    analog_data2.append(new_analog_value2)
    analog_data3.append(new_analog_value3)
    analog_data4.append(new_analog_value4)

    
    # Update the label text with the new_analog_value
    analog_label1 = 'Current Probe 1: {:.5f}mA'.format(new_analog_value1)
    analog_label2 = 'Current Probe 2: {:.5f}mA'.format(new_analog_value2)
    analog_label3 = 'Current Probe 3: {:.5f}mA'.format(new_analog_value3)
    analog_label4 = 'Current Probe 4: {:.5f}mA'.format(new_analog_value4)
   
    analog_line1.set_label(analog_label1)
    analog_line2.set_label(analog_label2)
    analog_line3.set_label(analog_label3)
    analog_line4.set_label(analog_label4)


    analog_line1.set_data(x_data, analog_data1)
    analog_line2.set_data(x_data, analog_data2)
    analog_line3.set_data(x_data, analog_data3)
    analog_line4.set_data(x_data, analog_data4)

    ax1.relim()
    ax1.autoscale_view(True, True, True)
    ax2.relim()
    ax2.autoscale_view(True, True, True)
    ax1.legend()  # Update the legend to reflect the new label
    plt.pause(0.01)



ser.close()
