import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import mysql.connector
import os
import shutil

# Database connector
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        port=3306, 
        user="root",
        password="root",  # Change if needed
        database="adavu_internship"
    )

# Extractor logic
def extract_frames(kp_id, dest_dir, log_widget):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT start_frame, end_frame, img_path FROM keyposture WHERE kp_id = %s", (kp_id,))
        rows = cursor.fetchall()

        os.makedirs(dest_dir, exist_ok=True)
        count = 0

        for start, end, img_path in rows:
            if not os.path.exists(img_path):
                log_widget.insert(tk.END, f"Not found: {img_path}\n")
                continue
            for i in range(start, end + 1):
                filename = f"Color_{i:06d}.png"
                src = os.path.join(img_path, filename)
                if os.path.exists(src):
                    shutil.copy(src, os.path.join(dest_dir, filename))
                    log_widget.insert(tk.END, f"Copied: {filename}\n")
                    count += 1
                else:
                    log_widget.insert(tk.END, f"Missing: {filename}\n")
        log_widget.insert(tk.END, f"\nExtraction complete. Total copied: {count}\n")
        conn.close()
    except Exception as e:
        log_widget.insert(tk.END, f"Error: {str(e)}\n")


# --- Import KeyPostureExtractorGUI from keyposture_gui.py ---
from keyposture_gui import KeyPostureExtractorGUI

# Page 2: Frame Extraction Page (now using KeyPostureExtractorGUI as a Frame)
class KeyPostureExtractorFrame(tk.Frame):
    def __init__(self, master, go_back):
        super().__init__(master)
        self.go_back = go_back
        # Embed the KeyPostureExtractorGUI inside this Frame
        self.inner = tk.Frame(self)
        self.inner.pack(fill="both", expand=True)
        self.kp_gui = KeyPostureExtractorGUI(self.inner)
        # Add a back button at the bottom
        tk.Button(self, text="Back to Menu", command=self.go_back, bg="#ef5350", fg="white").pack(pady=10)

# Page 1: Welcome Page
class WelcomePage(tk.Frame):
    def __init__(self, master, on_continue):
        super().__init__(master)

        bg_image = Image.open("bharatnatyam.jpg").resize((900, 600), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(bg_image)
        tk.Label(self, image=self.bg_photo).place(x=0, y=0, relwidth=1, relheight=1)

        center = tk.Frame(self, bg="", padx=20, pady=20)
        center.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center, text="Welcome to Bharatnatyam Utility", font=("Georgia", 20, "bold"),
                 fg="white", bg="black").pack(pady=10)

        tk.Button(center, text="Extract Key Posture Frames", font=("Arial", 14, "bold"),
                  bg="#fff2a8", fg="darkred", command=on_continue).pack(pady=10)
        tk.Button(center, text="Learn Mudras (Coming Soon)", font=("Arial", 14), state="disabled").pack(pady=5)
        tk.Button(center, text="Quiz Yourself (Coming Soon)", font=("Arial", 14), state="disabled").pack(pady=5)

# Main App
class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bharatnatyam Utility")
        self.geometry("900x600")
        self.resizable(False, False)

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.show_welcome()

    def show_welcome(self):
        self.clear()
        WelcomePage(self.container, self.show_extractor).pack(fill="both", expand=True)


    def show_extractor(self):
        self.clear()
        KeyPostureExtractorFrame(self.container, self.show_welcome).pack(fill="both", expand=True)

    def clear(self):
        for widget in self.container.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    MainApp().mainloop()
