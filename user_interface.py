import tkinter as tk
from tkinter import ttk, Menu, StringVar, Text, Label, Frame, PhotoImage
from PIL import Image, ImageTk
import os
from barcode_generator import DNABarcodeBackend

class DNABarcodeUI:
    def __init__(self, root):
        self.root = root
        self.root.title("DNA Barcode Generator")
        self.root.geometry("900x700")
        self.root.resizable(False, False)

        self.status_var = StringVar()
        self.status_var.set("Ready")

        # ==== Menu ====
        self.menu_bar = Menu(self.root)
        self.menu_saved = Menu(self.menu_bar, tearoff=0)
        self.menu_generate = Menu(self.menu_bar, tearoff=0)

        self.menu_bar.add_cascade(label="📂 Menu", menu=self.menu_saved)
        self.menu_saved.add_command(label="📂 View Saved Barcodes")

        self.menu_bar.add_cascade(label="🧬 Actions", menu=self.menu_generate)
        self.menu_generate.add_command(label="🧬 Generate New Barcode")

        self.root.config(menu=self.menu_bar)

        # ==== Profile Frame ====
        self.top_frame = Frame(self.root, height=150, bg="#f0f0f0")
        self.top_frame.pack(fill='x')

        self.about_label = Label(
            self.top_frame, text="DNA Barcode Generator\nThis software allows you to input DNA sequences (A, T, G, C) and convert them into visual barcode images. View previously saved barcodes or generate new ones easily.",
            font=("Segoe UI", 10), justify="left", bg="#f0f0f0", padx=20
        )
        self.about_label.pack(side="left", padx=10, pady=10)

        self.profile_frame = Frame(self.top_frame, bg="#f0f0f0")
        self.profile_frame.pack(side="right", padx=20)

        try:
            profile_path = "9aaefe20-d86a-40ca-a9bc-90bff4169cab.png"
            self.profile_img = Image.open(profile_path)
            self.profile_img = self.profile_img.resize((120, 120), Image.Resampling.LANCZOS)
            self.profile_photo = ImageTk.PhotoImage(self.profile_img)
            self.profile_label = Label(self.profile_frame, image=self.profile_photo, bg="#f0f0f0")
            self.profile_label.pack()
        except Exception as e:
            self.profile_label = Label(self.profile_frame, text="No Image", bg="#f0f0f0")
            self.profile_label.pack()

        # ==== Main Frame ====
        self.main_frame = Frame(self.root)
        self.main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        Label(self.main_frame, text="Enter DNA Sequence (A, T, G, C):", font=("Segoe UI", 12)).pack(anchor="w")

        self.sequence_text = Text(self.main_frame, height=6, wrap='word', font=("Courier New", 11))
        self.sequence_text.pack(fill='x', pady=(0, 10))

        # ==== Button Controls ====
        self.control_frame = Frame(self.main_frame)
        self.control_frame.pack(fill='x', pady=5)

        self.load_button = ttk.Button(self.control_frame, text="📂 Load Sequence from File")
        self.load_button.pack(side='left', padx=5)

        self.generate_button = ttk.Button(self.control_frame, text="🧬 Generate Barcode")
        self.generate_button.pack(side='left', padx=5)

        self.save_button = ttk.Button(self.control_frame, text="💾 Save Barcode")
        self.save_button.pack(side='left', padx=5)

        self.clear_button = ttk.Button(self.control_frame, text="❌ Clear")
        self.clear_button.pack(side='left', padx=5)

        # ==== Preview ====
        self.preview_frame = Frame(self.main_frame, relief='groove', bd=2)
        self.preview_frame.pack(fill='both', expand=True, pady=(10, 5))

        # ==== Status Bar ====
        self.status_bar = Label(self.root, textvariable=self.status_var, bd=1, relief="sunken", anchor="w", font=("Segoe UI", 10))
        self.status_bar.pack(side="bottom", fill="x")

        # ==== Connect to backend ====
        self.backend = DNABarcodeBackend(self)

if __name__ == "__main__":
    root = tk.Tk()
    app = DNABarcodeUI(root)
    root.mainloop()
