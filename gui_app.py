
import tkinter as tk
from tkinter import messagebox
import requests
import os

API_URL = "http://localhost:8080/analyze"

class SecureCommGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Secure Communications")
        self.root.geometry("400x300")

        self.label = tk.Label(root, text="Enter Secure Message:")
        self.label.pack(pady=10)

        self.text_box = tk.Text(root, height=6, width=40)
        self.text_box.pack(pady=5)

        self.send_button = tk.Button(root, text="Analyze & Encrypt", command=self.analyze_message)
        self.send_button.pack(pady=10)

        self.output = tk.Label(root, text="", wraplength=350, justify="left")
        self.output.pack(pady=10)

    def analyze_message(self):
        message = self.text_box.get("1.0", tk.END).strip()
        if not message:
            messagebox.showwarning("Warning", "Message cannot be empty.")
            return
        try:
            response = requests.post(API_URL, json={"message": message})
            if response.status_code == 200:
                sentiment = response.json()[0]
                result = f"Label: {sentiment['label']}, Score: {sentiment['score']:.2f}"
                self.output.config(text=result)
            else:
                self.output.config(text="Server Error")
        except Exception as e:
            self.output.config(text=f"Error: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SecureCommGUI(root)
    root.mainloop()
