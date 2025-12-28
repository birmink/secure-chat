import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime
import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet

load_dotenv()

# Client configuration
SERVER_HOST = os.getenv("SERVER_HOST", "127.0.0.1")
SERVER_PORT = int(os.getenv("SERVER_PORT", 5001))
BUFFER_SIZE = 4096

CLIENT_PASSWORD = os.getenv("CLIENT_PASSWORD")
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")  # Must match the server key
if CLIENT_PASSWORD is None or ENCRYPTION_KEY is None:
    raise ValueError("Missing CLIENT_PASSWORD or ENCRYPTION_KEY in .env file")

ENCRYPTION_KEY = ENCRYPTION_KEY.encode()
fernet = Fernet(ENCRYPTION_KEY)

class ChatClientGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Secure Chat Client")
        self.master.geometry("500x500")

        # Chat display area
        self.chat_area = scrolledtext.ScrolledText(master, state='disabled', wrap=tk.WORD)
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        # Configure tags for alignment and color
        self.chat_area.tag_configure('left', justify='left', foreground='gray', font=('Helvetica', 10, 'normal'))
        self.chat_area.tag_configure('right', justify='right', foreground='blue', font=('Helvetica', 10, 'bold'))



        # Message entry box
        self.msg_entry = tk.Entry(master)
        self.msg_entry.pack(padx=10, pady=(0,10), fill=tk.X)
        self.msg_entry.bind("<Return>", self.send_message)

        # Send button
        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.pack(padx=10, pady=(0,10))

        # Initialize socket and username
        self.s = socket.socket()
        self.username = ""
        self.connect_to_server()

        # Start thread to receive messages
        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.daemon = True
        self.receive_thread.start()

    def connect_to_server(self):
        try:
            self.s.connect((SERVER_HOST, SERVER_PORT))
            self.s.send(CLIENT_PASSWORD.encode())
            response = self.s.recv(BUFFER_SIZE).decode()

            if response != "AUTH_SUCCESS":
                self.display_message("Authentication failed. Closing...")
                self.master.after(2000, self.master.destroy)
                return

            self.username = self.ask_username()
            self.s.send(self.username.encode())

        except Exception as e:
            self.display_message(f"Connection error: {e}")
            self.master.after(2000, self.master.destroy)

    def ask_username(self):
        username_window = tk.Toplevel(self.master)
        username_window.title("Enter Username")
        username_window.geometry("300x100")

        label = tk.Label(username_window, text="Username:")
        label.pack(pady=5)

        username_entry = tk.Entry(username_window)
        username_entry.pack(pady=5)
        username_entry.focus()

        def submit():
            self.username_value = username_entry.get()
            username_window.destroy()

        submit_button = tk.Button(username_window, text="Submit", command=submit)
        submit_button.pack(pady=5)

        self.master.wait_window(username_window)
        return self.username_value

    def receive_messages(self):
        while True:
            try:
                encrypted_message = self.s.recv(BUFFER_SIZE)
                if not encrypted_message:
                    break
                message = fernet.decrypt(encrypted_message).decode()
                self.display_message(message, side='left')

            except Exception:
                self.display_message("Disconnected from server.", side='left')
                break


    def send_message(self, event=None):
        message = self.msg_entry.get()
        self.msg_entry.delete(0, tk.END)

        if message:
            timestamp = datetime.now().strftime("%I:%M")
            self.display_message(f"[{timestamp}] {self.username}: {message}", side='right')

            encrypted_message = fernet.encrypt(message.encode())
            self.s.send(encrypted_message)

            if message.lower() == "exit":
                self.master.destroy()


    def display_message(self, message, side='left'):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, message + "\n", side)
        self.chat_area.yview(tk.END)
        self.chat_area.config(state='disabled')



if __name__ == "__main__":
    root = tk.Tk()
    client_app = ChatClientGUI(root)
    root.mainloop()
