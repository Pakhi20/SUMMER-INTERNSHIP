import os
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

def load_and_show_images():
    folder = filedialog.askdirectory(title="Select Folder with Original Images and bg_removed")
    if not folder:
        return

    bg_removed_folder = os.path.join(folder, "bg_removed")

    if not os.path.exists(bg_removed_folder):
        messagebox.showerror("Missing Folder", "No 'bg_removed' folder found in selected location.")
        return

    for widget in canvas_frame.winfo_children():
        widget.destroy()

    files = [f for f in os.listdir(folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    row = 0
    for file in files:
        orig_path = os.path.join(folder, file)
        bg_path = os.path.join(bg_removed_folder, file)

        if not os.path.exists(bg_path):
            continue  # skip if no matching bg-removed image

        try:
            orig_img = Image.open(orig_path).resize((250, 250))
            bg_img = Image.open(bg_path).resize((250, 250))

            orig_img_tk = ImageTk.PhotoImage(orig_img)
            bg_img_tk = ImageTk.PhotoImage(bg_img)

            Label(canvas_frame, text=file, font=("Arial", 10, "bold")).grid(row=row, column=0, columnspan=2, pady=5)

            Label(canvas_frame, image=orig_img_tk).grid(row=row+1, column=0, padx=10)
            Label(canvas_frame, image=bg_img_tk).grid(row=row+1, column=1, padx=10)

            # store images so they don't get garbage collected
            canvas_frame.image_refs.append(orig_img_tk)
            canvas_frame.image_refs.append(bg_img_tk)

            row += 2
        except Exception as e:
            print(f"Error loading image {file}: {e}")

# GUI setup
root = Tk()
root.title("Image Comparison Viewer - Original vs BG Removed")
root.geometry("800x600")

btn = Button(root, text="Select Folder to Show Comparison", command=load_and_show_images, bg="#4caf50", fg="white", font=("Arial", 12, "bold"))
btn.pack(pady=10)

# Scrollable Canvas
canvas = Canvas(root)
scroll_y = Scrollbar(root, orient=VERTICAL, command=canvas.yview)
canvas_frame = Frame(canvas)
canvas_frame.image_refs = []  # prevent image garbage collection

canvas_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=canvas_frame, anchor="nw")
canvas.configure(yscrollcommand=scroll_y.set)

canvas.pack(side=LEFT, fill=BOTH, expand=True)
scroll_y.pack(side=RIGHT, fill=Y)

root.mainloop()
