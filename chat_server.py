import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from cryptography.fernet import Fernet
from datetime import datetime

# Server configuration
HOST = '0.0.0.0'
PORT = 5001
BUFFER_SIZE = 4096

SERVER_PASSWORD = "supersecretpassword"
ENCRYPTION_KEY = b'eBzD2dnLcDF55TvP6RL2C8p0-D5-PcD3M3X8ny9MR60='
fernet = Fernet(ENCRYPTION_KEY)

class ChatServerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Secure Chat Server")
        self.master.geometry("700x500")

        # Chat messages display
        self.chat_area = scrolledtext.ScrolledText(master, state='disabled', wrap=tk.WORD)
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Connected users list
        self.users_frame = tk.Frame(master)
        self.users_frame.pack(padx=10, pady=(0,10), fill=tk.X)

        self.users_listbox = tk.Listbox(self.users_frame, height=6)
        self.users_listbox.pack(side=tk.LEFT, padx=(0,5))

        # Start server button
        self.start_button = tk.Button(self.users_frame, text="Start Server", command=self.start_server)
        self.start_button.pack(side=tk.LEFT, padx=(5,5))

        # Server socket and client lists
        self.server_socket = None
        self.clients = []
        self.usernames = {}

    def display_message(self, message):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, message + "\n")
        self.chat_area.yview(tk.END)
        self.chat_area.config(state='disabled')

    def update_users_list(self):
        self.users_listbox.delete(0, tk.END)
        for username in self.usernames.values():
            self.users_listbox.insert(tk.END, username)

    def broadcast(self, message, sender_socket=None):
        for client in self.clients:
            if client != sender_socket:
                try:
                    client.send(message)
                except:
                    client.close()
                    if client in self.clients:
                        self.clients.remove(client)

    def handle_client(self, client_socket):
        try:
            received_password = client_socket.recv(BUFFER_SIZE).decode()
            if received_password != SERVER_PASSWORD:
                client_socket.close()
                return
            client_socket.send("AUTH_SUCCESS".encode())

            username = client_socket.recv(BUFFER_SIZE).decode()
            self.usernames[client_socket] = username
            self.clients.append(client_socket)
            self.update_users_list()

            join_msg = f"[{datetime.now().strftime('%I:%M')}] {username} has joined the chat."
            self.display_message(join_msg)
            encrypted_join = fernet.encrypt(join_msg.encode())
            self.broadcast(encrypted_join)

            while True:
                encrypted_message = client_socket.recv(BUFFER_SIZE)
                if not encrypted_message:
                    break

                message = fernet.decrypt(encrypted_message).decode()
                timestamp = datetime.now().strftime("%I:%M")

                if message.lower() == "exit":
                    break

                full_message = f"[{timestamp}] {username}: {message}"
                self.display_message(full_message)
                encrypted_broadcast = fernet.encrypt(full_message.encode())
                self.broadcast(encrypted_broadcast, sender_socket=client_socket)

        except Exception as e:
            print(f"[-] Error: {e}")

        finally:
            if client_socket in self.clients:
                self.clients.remove(client_socket)
            leave_msg = f"[{datetime.now().strftime('%I:%M')}] {self.usernames[client_socket]} has left the chat."
            self.display_message(leave_msg)
            encrypted_leave = fernet.encrypt(leave_msg.encode())
            self.broadcast(encrypted_leave)

            client_socket.close()
            del self.usernames[client_socket]
            self.update_users_list()

    def start_server(self):
        self.start_button.config(state=tk.DISABLED)  # Disable button after starting
        self.server_socket = socket.socket()
        self.server_socket.bind((HOST, PORT))
        self.server_socket.listen(5)
        self.display_message(f"[*] Server started on {HOST}:{PORT}")

        threading.Thread(target=self.accept_clients, daemon=True).start()

    def accept_clients(self):
        while True:
            try:
                client_socket, address = self.server_socket.accept()
                print(f"[+] Connection from {address}")
                threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()
            except Exception as e:
                messagebox.showerror("Error", f"Server Error: {e}")
                break

if __name__ == "__main__":
    root = tk.Tk()
    server_app = ChatServerGUI(root)
    root.mainloop()
