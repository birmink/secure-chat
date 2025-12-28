# Secure Python Chat App

This is a simple chat application I built in Python. It lets multiple users connect to a server and chat in real-time, with messages encrypted for privacy. The app has a GUI built with Tkinter and includes some basic security features like a password-protected server.

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
- Cryptography (`Fernet`) for message encryption  

---

## How to Use

### Server

1. Open `server.py`.  
2. (Optional) Change the server password or encryption key in the code.  
3. Run it:
```bash
python server.py
