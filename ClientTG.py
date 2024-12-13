#Tomasz Giedrojc
#100793058 
#This is my own work
import socket
import json
import time
import os
import tkinter as tk
from tkinter import messagebox

def collect_data(iteration):
    """
    Collects data from the Raspberry Pi using vcgencmd commands.
    
    Parameters:
        iteration (int): The current iteration count.
    
    Returns:
        dict: A dictionary containing the collected data.
    """
    data = {
        "iteration": iteration,
        "core_temp": round(get_core_temp(), 1),
        "gpu_volts": round(get_gpu_volts(), 1),
        "arm_clock": round(get_arm_clock(), 1),
        "hdmi_clock": round(get_hdmi_clock(), 1),
        "memory_usage": round(get_memory_usage(), 1)  # New data: Memory usage in MB
    }
    return data

# Functions to gather data using vcgencmd commands
def get_core_temp():
    """Returns the core temperature of the Raspberry Pi."""
    temp = os.popen('vcgencmd measure_temp').readline()
    return float(temp.split('=')[1].strip('\'C\n'))

def get_gpu_volts():
    """Returns the GPU voltage of the Raspberry Pi."""
    volts = os.popen('vcgencmd measure_volts core').readline()
    return float(volts.split('=')[1].strip('V\n'))

def get_arm_clock():
    """Returns the ARM clock frequency of the Raspberry Pi in MHz."""
    clock = os.popen('vcgencmd measure_clock arm').readline()
    return int(clock.split('=')[1].strip()) / 1000000  # Convert to MHz

def get_hdmi_clock():
    """Returns the HDMI clock frequency of the Raspberry Pi in MHz."""
    clock = os.popen('vcgencmd measure_clock hdmi').readline()
    return int(clock.split('=')[1].strip()) / 1000000  # Convert to MHz

def get_memory_usage():
    """Returns the current memory usage of the Raspberry Pi in MB."""
    # Using free command to get memory information
    mem_info = os.popen('free -m').readlines()
    total_mem = int(mem_info[1].split()[1])  # Total memory in MB
    used_mem = int(mem_info[1].split()[2])  # Used memory in MB
    return (used_mem / total_mem) * 100  # Return as percentage

def send_data():
    """Connects to the server and sends collected data."""
    server_address = ('127.0.0.1', 65432)  # Server IP and Port
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client_socket.connect(server_address)
        
        for i in range(50):  # Loop to send data multiple times
            update_led(True)  # Turn on LED to indicate data transmission
            data = collect_data(i+1)  # Collect data for the current iteration
            json_data = json.dumps(data)  # Convert data to JSON format
            client_socket.sendall(json_data.encode('utf-8'))  # Send data to the server
            time.sleep(2)  # Wait for 2 seconds before sending the next batch
            update_led(False)  # Turn off LED after data is sent
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        client_socket.close()  # Ensure the socket is closed properly
        messagebox.showinfo("Info", "Data transmission complete.")
        root.quit()  # Exit the application after transmission

def update_led(state):
    """Updates the LED (represented as a button in the GUI)."""
    if state:
        led_button.config(bg='green')  # Turn on LED (green)
    else:
        led_button.config(bg='red')  # Turn off LED (red)

def check_environment():
    """Checks if the script is running on a Raspberry Pi."""
    if os.name == 'nt':  # Check if running on Windows
        messagebox.showerror("Error", "This program can only be run on a Raspberry Pi.")
        root.quit()
    else:
        send_data()  # Proceed to data transmission if on Raspberry Pi

# GUI setup
root = tk.Tk()
root.title("Client GUI")

# Button to start data transmission
start_button = tk.Button(root, text="Start Sending Data", command=check_environment)
start_button.pack(pady=20)

# Button to exit the application
exit_button = tk.Button(root, text="Exit", command=root.quit)
exit_button.pack(pady=20)

# LED representation as a button (green = on, red = off)
led_button = tk.Button(root, text="LED", width=10, height=3, bg='red')
led_button.pack(pady=20)

root.mainloop()
