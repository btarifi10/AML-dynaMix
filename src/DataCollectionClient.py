from datetime import datetime
import serial
import json
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Initialize plot
plt.ion()
fig, ax = plt.subplots(1, 3)
xdata, ydata = [], []

plt.sca(ax[0])
plot_ecg, = plt.plot([], [], 'r-')
plt.sca(ax[1])
plot_gsr, = plt.plot([], [], 'r-')
plt.sca(ax[2])
plot_ppg_red, = plt.plot([], [], 'r-')
plot_ppg_ir, = plt.plot([], [], 'b-')

t, ecg, gsr, ppg_red, ppg_ir, temp = [], [], [], [], [], []
data_list = []

# Function to update plot
def update_plot(frame):
    plot_ecg.set_data(t, ecg)
    plot_gsr.set_data(t, gsr)
    plot_ppg_red.set_data(t, ppg_red)
    plot_ppg_ir.set_data(t, ppg_ir)

    for axis in ax:
        axis.relim()
        axis.autoscale_view()
    return plot_ecg, plot_gsr, plot_ppg_red, plot_ppg_ir

# Collect user details and format choice
user_details = {
    "name": input("Enter name: "),
    "age": input("Enter age: "),
    "sex": input("Enter sex: ")
}

# Set up serial connection (adjust COM port as needed)
baud_rate = 115200
ser = serial.Serial(input("Enter COM port: "), baud_rate)

# Start data collection
ser.write(b"OOGA_BOOGA\n")
print("Data collection started. Press Enter to stop.")

ani = FuncAnimation(fig, update_plot, blit=True)

try:
    while True:
        if ser.in_waiting > 0:
            sensor_data = ser.readline().decode('utf-8').rstrip()
            print(sensor_data)
            timestamp, ecg, gsr, ppg_ir, ppg_red, ppg_temp = sensor_data.split(" ")

            t.append(float(timestamp))
            ecg.append(float(ecg))
            gsr.append(float(gsr))
            ppg_red.append(float(ppg_red))
            ppg_ir.append(float(ppg_ir))
            temp.append(float(ppg_temp))

            plt.pause(0.01)
        if input() == '':
            ser.write(b"BIG_CHUNGUS\n")
            break

except KeyboardInterrupt:
    pass

finally:
    ser.close()
    print("Data collection stopped.")
    plt.ioff()
    plt.show()

    # Format data
    data = {
        "user_details": user_details,
        "ecg": ecg,
        "gsr": gsr,
        "ppg_red": ppg_red,
        "ppg_ir": ppg_ir,
        "temp": temp
    }

    # name file with the users name and current time
    time_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"{user_details['name']}_{time_now}.json"

    with open(file_name, "w") as data_file:
        json.dump(data, data_file)
