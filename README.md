# 🕵️ Keylogger  – Cybersecurity Project

> A comprehensive educational project combining Linux basics, network reconnaissance (Nmap), packet analysis (Wireshark), and a fully-featured keylogger disguised as a sticky note app. 

## 🔧 Project Overview

This repository is a cybersecurity project focused on simulating real-world ethical hacking tools and spyware techniques. It is designed to:

- Develop and run Linux and Python-based scripts
- Use `nmap` for host discovery and OS detection
- Perform packet sniffing and analysis with Wireshark
- Design and implement a **Python keylogger** with additional spyware-like features such as:
  - Clipboard logging
  - Screen capturing
  - Email reporting
  - File encryption
  - GUI disguise
    
---

## 📂 Features

### 🖥️ Keylogger (KeyLogger.py)
- Records every keystroke in the background
- Tracks the **window name** where each key was typed
- Stores logs in both **raw** and **formatted** formats
- Creates logs for **clipboard data** (text only)
- Takes **screenshots** of the user’s screen
- Encrypts the log files using **Fernet AES-128**
- Compresses all logs and screenshots into a `.zip` file
- Sends the zip file via **email** using SMTP

### 🗒️ Disguised UI
- Fake **sticky note** GUI using Tkinter
- Closes into a fake **review window** requesting the user's email
- Runs the spyware silently in the background

---

## 📁 File Structure

| File / Folder | Type | Description |
|---------------|------|-------------|
| `KeyLogger.py` | Python | Main keylogger script |
| `KeyDictionary.py` | Python | Maps special keys to readable names |
| `Install-Packages.bat` | Batch | Installs required libraries |
| `Clipboard.txt` | Text | Copied clipboard data |
| `Full_Log.txt` | Text | Raw keystroke log |
| `Formatted_Log.txt` | Text | User-readable log |
| `Encrypted_Full_Log.txt` | Text | Encrypted log |
| `Decrypted_Full_Log.txt` | Text | Decrypted log |
| `key.key` | Binary | Encryption key file |
| `Screenshots/` | Folder | All screenshots taken |
| `Data.zip` | Archive | Compressed logs for email |

---

## 🚀 Getting Started

### ⚙️ Installation
1. Download and extract the ZIP of this repo.
2. Run `Install-Packages.bat` to install all dependencies.

### ▶️ Run
Double-click `KeyLogger.py`  
A sticky note GUI will appear — the keylogger is now active in the background.  
On close, a review form will appear; after submission, logs will be zipped and emailed.

---

## 🧰 Dependencies

- `pynput` – Keyboard input tracking  
- `tkinter` – GUI disguise  
- `pyscreenshot` – Screen capture  
- `win32clipboard`, `win32gui` – Clipboard and window tracking  
- `cryptography.fernet` – AES encryption  
- `email.mime`, `smtplib` – Email automation  
- `zipfile`, `os`, `sys`, `datetime` – System/file management

---

## 📜 License & Disclaimer

This repository is licensed for **educational and demonstration purposes only**.  
Misuse of the scripts for malicious intent is strictly prohibited and illegal.

