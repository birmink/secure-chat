# Secure Python Chat App

This is a simple chat application I built in Python. It lets multiple users connect to a server and chat in real-time, with messages encrypted for privacy using Fernet symmetric encryption. The app has a GUI built with Tkinter and includes some basic security features like a password-protected server.

---

## Features

- **Encrypted Chat:** Messages are encrypted with Fernet so they can’t be read in transit.  
- **Multiple Clients:** More than one person can connect and chat at the same time.  
- **Password-Protected Server:** Only clients with the right password can join.  
- **User-Friendly GUI:** Easy-to-use chat interface with a message log.  
- **Timestamps & Notifications:** Shows when users join or leave, and timestamps each message.

---

## Technologies

- Python 3  
- Tkinter for GUI  
- Socket programming for client-server communication  
- Threading for handling multiple clients  
- Cryptography (`Fernet`) for secure message encryption
- Python-dotenv for environment variables

---

## How to Use
### Start the Server
- Click **Start Server** in the GUI.
- The server will begin listening for client connections.
### Connect with a Client
- Enter your username when prompted.
- Start chatting securely with other connected users.

---
## Usage
- Type messages in the entry box and click **Enter** or click **Send**.
- Type exit to leave the chat.
- Messages are displayed in different colors for your messages vs. others.

 ---

## Notes
- Make sure the server is running before starting clients.
- The encryption key and passwords must match between server and client.

## License
This project is open-source and free to use.
