import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from rembg import remove
import mysql.connector


class KeyPostureExtractorGUI(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#fffde7")
        self.root = parent

        self.conn = self.connect_to_db()
        if not self.conn:
            return
        self.cursor = self.conn.cursor()


        tk.Label(self, text="Extract Key Posture Frames", font=("Helvetica", 20, "bold"),
                 bg="#fffde7", fg="#3e2723").pack(pady=10)


        form_frame = tk.Frame(self, bg="#fffde7")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Search Key Posture:", font=("Arial", 12, "bold"),
                 fg="#3e2723", bg="#fffde7"
        ).grid(row=0, column=0, padx=10, pady=5, sticky="e")

        self.keyposture_var = tk.StringVar()
        self.keyposture_combo = ttk.Combobox(form_frame, textvariable=self.keyposture_var, width=30)
        self.keyposture_combo.grid(row=0, column=1, padx=10)
        self.keyposture_combo['values'] = []  # You’ll fill this via `load_key_postures()`
        self.keyposture_combo.bind("<<ComboboxSelected>>", lambda e: self.log(f"Selected Key Posture: {self.keyposture_var.get()}"))


        tk.Button(form_frame, text="Load Key Postures", command=self.load_key_postures, bg="#ffee58", relief="ridge").grid(row=0, column=2, padx=5)

        tk.Label(form_frame, text="Destination Folder:", font=("Arial", 12, "bold"),
                 bg="#fffde7").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.destination_var = tk.StringVar()
        self.destination_entry = tk.Entry(form_frame, textvariable=self.destination_var, width=35)
        self.destination_entry.grid(row=1, column=1, padx=10)
        tk.Button(form_frame, text="Browse", command=self.browse_destination, bg="#ffee58", relief="ridge").grid(row=1, column=2, padx=5)

        tk.Label(form_frame, text="Source Folder:", font=("Arial", 12, "bold"),
                 bg="#fffde7").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.source_var = tk.StringVar()
        self.source_entry = tk.Entry(form_frame, textvariable=self.source_var, width=35)
        self.source_entry.grid(row=2, column=1, padx=10)
        self.source_entry.insert(0, self.find_source_folder())
        tk.Button(form_frame, text="Browse", command=self.browse_source, bg="#ffee58", relief="ridge").grid(row=2, column=2, padx=5)


        tk.Button(self, text="Extract from Database", command=self.extract_images, width=30,
                  bg="#fbc02d", fg="black", font=("Arial", 11, "bold")).pack(pady=10)

        # BUTTON: remove background from extracted images
        tk.Button(self, text="Remove Background (Extracted Images)", command=self.remove_background_from_images, width=30,
                  bg="#4caf50", fg="white", font=("Arial", 11, "bold")).pack(pady=5)

        # BUTTON: open a new window for external BG removal
        tk.Button(self, text="Open BG Remover Page", command=self.open_remove_bg_page, width=30,
                  bg="#6a1b9a", fg="white", font=("Arial", 11, "bold")).pack(pady=5)

        btn_frame = tk.Frame(self, bg="#fffde7")
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Show All", command=self.show_all, bg="#ffe082").grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Show kp_id", command=self.show_kp_id, bg="#ffe082").grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Show start_fr", command=self.show_start, bg="#ffe082").grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Show end_fr", command=self.show_end, bg="#ffe082").grid(row=0, column=3, padx=5)
        tk.Button(btn_frame, text="Exit", command=self.winfo_toplevel().quit, bg="#ef5350", fg="white").grid(row=0, column=4, padx=5)
        tk.Button(btn_frame, text="Clear Log", command=lambda: self.log_text.delete(1.0, tk.END), bg="#90a4ae").grid(row=0, column=5, padx=5)
        tk.Button(btn_frame, text="Show All Key Postures", command=self.load_key_postures, bg="#90a4ae").grid(row=0, column=6, padx=5)


        self.log_text = tk.Text(self, height=12, width=100, bg="#fffde7", fg="black")
        self.log_text.pack(pady=12, padx=10)
        self.log("Welcome to Key Posture Frame Extractor!\n")

        self.load_key_postures()

    def connect_to_db(self):
        try:
            return mysql.connector.connect(
                host="localhost",
                port=3306,
                user="root",
                password="",
                database="adavu_internship"
            )
        except mysql.connector.Error as err:
            messagebox.showerror("DB Connection Error", str(err))
            return None

    def load_key_postures(self):
        try:
            self.cursor.execute("SELECT DISTINCT kp_id FROM keyposture ORDER BY kp_id")
            options = [row[0] for row in self.cursor.fetchall()]
            self.keyposture_combo['values'] = options
        except Exception as e:
            self.log(f"Error loading keypostures: {e}")

    def browse_destination(self):
        folder = filedialog.askdirectory()
        if folder:
            self.destination_var.set(folder)

    def browse_source(self):
        folder = filedialog.askdirectory()
        if folder:
            self.source_var.set(folder)

    def extract_images(self):
        kp = self.keyposture_var.get()
        dest_root = self.destination_var.get()
        if not kp or not dest_root:
            messagebox.showwarning("Missing Data", "Please select a Key Posture and destination folder.")
            return
        try:
            self.cursor.execute("SELECT start_frame, end_frame FROM keyposture WHERE kp_id = %s", (kp,))
            row = self.cursor.fetchone()
            if not row:
                self.log(f"No entry found for kp_id: {kp}")
                return
            start, end = row
            img_folder = self.source_var.get() or self.find_source_folder()
            output_folder = os.path.join(dest_root, kp)
            os.makedirs(output_folder, exist_ok=True)
            copied = 0
            for i in range(start, end + 1):
                filename = f"Color_{i:06}.png"
                full_path = os.path.join(img_folder, filename)
                if os.path.exists(full_path):
                    shutil.copy(full_path, os.path.join(output_folder, filename))
                    self.log(f"Copied: {filename}")
                    copied += 1
                else:
                    self.log(f"Missing: {filename}")
            self.log(f"✅ Extraction complete. Total images copied: {copied}")
        except Exception as e:
            self.log(f"Extraction error: {e}")

    def remove_background_from_images(self):
        kp = self.keyposture_var.get()
        dest_root = self.destination_var.get()
        source_folder = os.path.join(dest_root, kp)
        bg_removed_folder = os.path.join(dest_root, "bg_removed", kp)
        if not os.path.exists(source_folder):
            messagebox.showerror("Folder Not Found", f"No extracted images found at: {source_folder}")
            return
        os.makedirs(bg_removed_folder, exist_ok=True)
        processed = 0
        for filename in os.listdir(source_folder):
            if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                src_path = os.path.join(source_folder, filename)
                dst_path = os.path.join(bg_removed_folder, filename)
                try:
                    with open(src_path, 'rb') as input_file:
                        input_data = input_file.read()
                        output_data = remove(input_data)
                    with open(dst_path, 'wb') as output_file:
                        output_file.write(output_data)
                    self.log(f"BG Removed: {filename}")
                    processed += 1
                except Exception as e:
                    self.log(f"Error processing {filename}: {e}")
        self.log(f"✅ Background removal complete. Total processed: {processed}")


    def open_remove_bg_page(self):
        top = tk.Toplevel(self.winfo_toplevel())
        top.title("Remove Background from Any Folder")
        top.geometry("600x300")
        top.configure(bg="#fffde7")

        tk.Label(top, text="Select Folder with Images", font=("Arial", 14, "bold"),
                 bg="#fffde7", fg="#3e2723").pack(pady=20)

        folder_var = tk.StringVar()

        def browse_and_process():
            folder = filedialog.askdirectory()
            if folder:
                folder_var.set(folder)
                dest_folder = r"C:\Users\purba\OneDrive\Desktop\internship\bg_removed"
                os.makedirs(dest_folder, exist_ok=True)

                processed = 0
                for filename in os.listdir(folder):
                    if filename.lower().endswith((".png", ".jpg", ".jpeg")):
                        src_path = os.path.join(folder, filename)
                        dst_path = os.path.join(dest_folder, filename)
                        try:
                            with open(src_path, 'rb') as input_file:
                                input_data = input_file.read()
                                output_data = remove(input_data)
                            with open(dst_path, 'wb') as output_file:
                                output_file.write(output_data)
                            processed += 1
                        except Exception as e:
                            messagebox.showerror("Error", f"Failed to process {filename}:\n{e}")

                messagebox.showinfo("Done", f"✅ Removed background from {processed} images.\nSaved to: {dest_folder}")

        tk.Button(top, text="Browse and Process", command=browse_and_process,
                  bg="#fbc02d", font=("Arial", 12, "bold")).pack(pady=10)

        tk.Entry(top, textvariable=folder_var, width=60).pack(pady=10)

    def find_source_folder(self):
        return r"C:\Users\purba\OneDrive\Desktop\Bharatnatyam\archive (1)\bharatnatyam_adavu\katti_kartari\1\Dancer1\Color"

    def show_all(self):
        self.show_query("SELECT kp_id, start_frame, end_frame FROM keyposture")

    def show_kp_id(self):
        self.show_query("SELECT kp_id FROM keyposture")

    def show_start(self):
        self.show_query("SELECT start_frame FROM keyposture")

    def show_end(self):
        self.show_query("SELECT end_frame FROM keyposture")

    def show_query(self, sql):
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            self.log("Result:\n" + "\n".join([str(r) for r in results]))
        except Exception as e:
            self.log(f"Query error: {e}")

    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)


# Run the GUI standalone
if __name__ == "__main__":
    root = tk.Tk()
    frame = KeyPostureExtractorGUI(root)
    frame.pack(fill="both", expand=True)
    root.mainloop()
