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
com_port = input("Enter COM port: ")
ser = serial.Serial(com_port, baud_rate)
ser.flush()
device_found = False
while not device_found:
    if ser.in_waiting > 0:
        message = ser.readline().decode('utf-8').rstrip()
        if (message == "Ready."):
            print(f"Found device on {com_port}, starting data collection...")
            device_found = True
        else:
            print("Received message from device: ", message)

# Start data collection
ser.write("Start\n".encode())
# ser.flush()
print("Data collection started. Press CTRL+C to stop.")

ani = FuncAnimation(fig, update_plot, blit=True, cache_frame_data=False)

try:
    while True:
        if ser.in_waiting > 0:
            sensor_data = ser.readline().decode('utf-8').rstrip()
            # print(sensor_data)
            timestamp_, ecg_, gsr_, ppg_ir_, ppg_red_, ppg_temp_ = sensor_data.split(" ")

            t.append(float(timestamp_))
            ecg.append(float(ecg_))
            gsr.append(float(gsr_))
            ppg_red.append(float(ppg_red_))
            ppg_ir.append(float(ppg_ir_))
            temp.append(float(ppg_temp_))

            plt.pause(0.01)
except KeyboardInterrupt:
    ser.write("Stop\n".encode())
finally:
    ser.close()
    print("Data collection stopped.")
    plt.ioff()
    plt.show()

    # Format data
    data = {
        "user_details": user_details,
        "timestamp": t,
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
