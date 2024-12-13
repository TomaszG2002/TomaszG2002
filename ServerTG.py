#Tomasz Giedrojc
#100793058 
#This is my own work
import socket
import json
import tkinter as tk
import threading
import time

# Constants for server configuration
HOST = '127.0.0.1'  # Localhost IP address
PORT = 65432        # Port number for the server

# Function to handle communication with a connected client
def handle_client(client_socket):
    """
    Handles the incoming data from the client and updates the GUI.
    Args:
        client_socket: The socket object for the connected client.
    """
    try:
        while True:
            # Receive data from the client
            data = client_socket.recv(1024)
            if not data:  # If no data is received, exit the loop
                break
            # Decode and parse JSON data
            json_data = data.decode('utf-8')
            data_dict = json.loads(json_data)

            # Update the GUI with received data
            update_display(data_dict)
            
            # Turn the LED indicator on to show data reception
            update_led(True)
            
            # Schedule turning off the LED after 2 seconds
            root.after(2000, lambda: update_led(False))
    except Exception as e:
        print(f"Error: {e}")  # Log any errors
    finally:
        client_socket.close()  # Ensure the client socket is closed

# Function to update the display with received data
def update_display(data):
    """
    Updates the text area in the GUI with received JSON data.
    Args:
        data: The dictionary containing the received data.
    """
    display_text.delete(1.0, tk.END)  # Clear existing text
    display_text.insert(tk.END, f"Received Data:\n{json.dumps(data, indent=4)}\n")  # Insert new data

# Function to update the LED indicator
def update_led(state):
    """
    Updates the LED button color to indicate data reception status.
    Args:
        state: A boolean indicating whether data is being received.
    """
    if state:
        led_button.config(bg='red')  # Turn LED "on" (red)
    else:
        led_button.config(bg='green')  # Turn LED "off" (green)

# Function to start the server
def start_server():
    """
    Starts the server in a separate thread to handle client connections.
    """
    # Function to run the server logic
    def run_server():
        # Create and configure the server socket
        server_address = (HOST, PORT)
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(server_address)  # Bind the socket to the address
        server_socket.listen(1)  # Listen for one connection at a time
        print("Server is listening for connections...")

        # Accept and handle client connections in a loop
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection established with {client_address}")
            handle_client(client_socket)  # Handle the client in a separate function

    # Create and start the server thread
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True  # Ensure the thread exits when the main program ends
    server_thread.start()

# GUI setup
root = tk.Tk()  # Initialize the main Tkinter window
root.title("Server GUI")  # Set the title of the window

# Text area for displaying received data
display_text = tk.Text(root, height=15, width=50)  # Create a text widget for data display
display_text.pack(pady=10)  # Add padding and place it in the window

# Button representing the LED indicator for data reception
led_button = tk.Button(root, text="Data Status", width=10, height=3, bg='red')  # Initially set to "off"
led_button.pack(pady=20)  # Add padding and place it in the window

# Button to start the server
start_button = tk.Button(root, text="Start Server", command=start_server)  # Calls start_server when clicked
start_button.pack(pady=20)  # Add padding and place it in the window

# Start the GUI event loop
root.mainloop()
