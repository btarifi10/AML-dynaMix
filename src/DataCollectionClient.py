from datetime import datetime
from time import sleep, time
import serial
import json
import matplotlib.pyplot as plt
import threading
import signal
import sys

# Initialize plot
plt.ion()
fig, ax = plt.subplots(1, 5, figsize=(20, 5))
titles = ['ECG', 'GSR', 'PPG Red', 'PPG IR', 'PPG Green']
for axis, title in zip(ax, titles):
    axis.set_title(title)
    axis.set_xlabel('Time (s)')
    axis.set_ylabel('Value')
    axis.grid(True)

# Creating separate plot lines for each measurement
plot_lines = {
    'ecg': ax[0].plot([], [], 'r-', label='ECG')[0],
    'gsr': ax[1].plot([], [], 'g-', label='GSR')[0],
    'ppg_red': ax[2].plot([], [], 'r-', label='PPG Red')[0],
    'ppg_ir': ax[3].plot([], [], 'b-', label='PPG IR')[0],
    'ppg_green': ax[4].plot([], [], 'g-', label='PPG Green')[0]
}

# Data lists
t, ecg, gsr, ppg_red, ppg_ir, ppg_green, temp = [], [], [], [], [], [], []
abs_t = []

# Thread-safe mechanism for data updates
data_lock = threading.Lock()

# Flag to control the execution
running = True

# Function to update plot
def update_plot():
    with data_lock:
        window_size = 100  # Adjust window size for data viewing
        if len(t) > window_size:
            for line, data in zip(plot_lines.values(), [ecg, gsr, ppg_red, ppg_ir, ppg_green]):
                line.set_data([tt / 1000 for tt in t[-window_size:]], data[-window_size:])
        else:
            for line, data in zip(plot_lines.values(), [ecg, gsr, ppg_red, ppg_ir, ppg_green]):
                line.set_data([tt / 1000 for tt in t], data)

    # Adjusting limits
    for axis in ax:
        axis.relim()
        axis.autoscale_view()
    plt.draw()

# Signal handler for SIGINT
def signal_handler(sig, frame):
    global running
    running = False
    print("Terminating...")

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)

# Function to collect data from the serial port
def collect_data(ser):
    global running
    try:
        while running:
            if ser.in_waiting > 0:
                sensor_data = ser.readline().decode('utf-8').rstrip()
                timestamp_, ecg_, gsr_, ppg_ir_, ppg_red_, ppg_green_, temp_ = sensor_data.split(" ")
                
                with data_lock:
                    t.append(float(timestamp_))
                    abs_t.append(time())
                    ecg.append(float(ecg_))
                    gsr.append(float(gsr_))
                    ppg_red.append(float(ppg_red_))
                    ppg_ir.append(float(ppg_ir_))
                    ppg_green.append(float(ppg_green_))
                    temp.append(float(temp_))
    finally:
        ser.close()
        print("Serial port closed.")

if __name__ == "__main__":
    # Collect user details
    user_details = {
        "name": input("Enter name: "),
        "age": input("Enter age: "),
        "sex": input("Enter sex: ")
    }

    # Set up serial connection
    com_port = input("Enter COM port: ")
    baud_rate = 230400
    ser = serial.Serial(com_port, baud_rate)
    ser.flush()

    device_found = False
    while not device_found:
        if ser.in_waiting > 0:
            message = ser.readline().decode('utf-8').rstrip()
            if message == "Ready.":
                print(f"Found device on {com_port}, starting data collection...")
                device_found = True
            else:
                print("Received message from device: ", message)
        else:
            sleep(0.5)
            print("Waiting for device...")

    # Start data collection
    ser.write("Start\n".encode())
    # ser.write(f"{int(datetime.now().timestamp() * 1000).encode()}\n".encode())
    print("Data collection started. Press CTRL+C to stop.")

    # Start data collection thread
    data_thread = threading.Thread(target=collect_data, args=(ser,))
    data_thread.start()

    try:
        while running:
            update_plot()
            plt.pause(0.1)  # Adjust as necessary for update frequency
    except KeyboardInterrupt:
        print("Program interrupted by user.")
    finally:
        running = False
        data_thread.join()
        plt.ioff()
        plt.close(fig)
        print("Cleaned up and exited.")

        # Save the collected data
        data = {
            "user_details": user_details,
            "timestamp": t,
            "absolute_time": abs_t,
            "ecg": ecg,
            "gsr": gsr,
            "ppg_red": ppg_red,
            "ppg_ir": ppg_ir,
            "ppg_green": ppg_green, 
            "temp": temp
        }
        time_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = f"{user_details['name']}_{time_now}.json"
        with open(file_name, "w") as data_file:
            json.dump(data, data_file)
