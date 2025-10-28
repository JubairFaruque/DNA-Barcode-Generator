import tkinter as tk
from tkinter import ttk, Menu, StringVar, Text, Label, Frame, filedialog, messagebox
from PIL import Image, ImageTk
import os
from barcode_generator import DNABarcodeBackend

class DNABarcodeUI:
    def __init__(self, root):
        self.root = root
        self.root.title("DNA Barcode Generator")
        self.root.geometry("1200x800")
        self.root.resizable(False, False)

        self.status_var = StringVar()
        self.status_var.set("Ready")

        # ========== Cover Screen ==========
        self.cover_frame = Frame(self.root, bg="white")
        self.cover_frame.pack(fill="both", expand=True)

        try:
            cover_path = "dna_barcode_cover.png"
            cover_img = Image.open(cover_path).resize((900, 600), Image.Resampling.LANCZOS)
            self.cover_photo = ImageTk.PhotoImage(cover_img)
            self.cover_label = Label(self.cover_frame, image=self.cover_photo, bg="white")
            self.cover_label.pack(pady=20)
        except Exception:
            self.cover_label = Label(self.cover_frame, text="Cover Image Missing", bg="white", font=("Segoe UI", 18))
            self.cover_label.pack(pady=50)

        self.start_button = ttk.Button(self.cover_frame, text="🚀 Enter Software", command=self.show_main_ui)
        self.start_button.pack(pady=15)

        # Prepare main UI components (but do NOT pack them yet)
        self._build_main_ui()

        # Backend will be created after main UI exists (done in _build_main_ui)
        # DNABarcodeBackend will be instantiated when show_main_ui is called (to avoid premature backend actions)

    def _build_main_ui(self):
        # Menu (kept as attributes so backend can configure them)
        self.menu_bar = Menu(self.root)
        self.menu_saved = Menu(self.menu_bar, tearoff=0)
        self.menu_generate = Menu(self.menu_bar, tearoff=0)

        # Add entries (index 0 used by backend to entryconfigure)
        self.menu_saved.add_command(label="📂 View Saved Barcodes")
        self.menu_generate.add_command(label="🧬 Generate New Barcode")

        self.menu_bar.add_cascade(label="📂 Menu", menu=self.menu_saved)
        self.menu_bar.add_cascade(label="🧬 Actions", menu=self.menu_generate)

        # Main frame (hidden until cover dismissed)
        self.main_frame = Frame(self.root)

        # Top: about + profile
        self.top_frame = Frame(self.main_frame, height=140, bg="#f6f7f9")
        self.top_frame.pack(fill='x')

        about_text = ("DNA Barcode Generator — visualizes DNA sequences as color barcodes. "
                      "Input sequences (A,T,G,C), generate a barcode, and save both image and sequence.")
        self.about_label = Label(self.top_frame, text=about_text, font=("Segoe UI", 10), bg="#f6f7f9", justify="left", wraplength=900)
        self.about_label.pack(side="left", padx=16, pady=16)

        # Profile image (small)
        self.profile_frame = Frame(self.top_frame, bg="#f6f7f9")
        self.profile_frame.pack(side="right", padx=16, pady=10)
        try:
            profile_path = "9aaefe20-d86a-40ca-a9bc-90bff4169cab.png"
            profile_img = Image.open(profile_path).resize((110, 110), Image.Resampling.LANCZOS)
            self.profile_photo = ImageTk.PhotoImage(profile_img)
            self.profile_label = Label(self.profile_frame, image=self.profile_photo, bg="#f6f7f9")
            self.profile_label.pack()
        except Exception:
            self.profile_label = Label(self.profile_frame, text="No Image", bg="#f6f7f9")
            self.profile_label.pack()

        # Input
        Label(self.main_frame, text="Enter DNA Sequence (A, T, G, C):", font=("Segoe UI", 12)).pack(anchor="w", padx=12, pady=(12,0))
        self.sequence_text = Text(self.main_frame, height=6, wrap='word', font=("Courier New", 11))
        self.sequence_text.pack(fill='x', padx=12, pady=(0,10))

        # Controls
        self.control_frame = Frame(self.main_frame)
        self.control_frame.pack(fill='x', padx=12, pady=6)

        self.load_button = ttk.Button(self.control_frame, text="📂 Load Sequence from File")
        self.load_button.pack(side='left', padx=6)

        self.generate_button = ttk.Button(self.control_frame, text="🧬 Generate Barcode")
        self.generate_button.pack(side='left', padx=6)

        self.save_button = ttk.Button(self.control_frame, text="💾 Save Barcode")
        self.save_button.pack(side='left', padx=6)

        self.clear_button = ttk.Button(self.control_frame, text="❌ Clear")
        self.clear_button.pack(side='left', padx=6)

        # Preview area
        Label(self.main_frame, text="Barcode Preview:", font=("Segoe UI", 12)).pack(anchor="w", padx=12, pady=(12,0))
        self.preview_frame = Frame(self.main_frame, relief='groove', bd=2, width=1000, height=300)
        self.preview_frame.pack(fill='both', expand=True, padx=12, pady=(6,12))

        # Status bar (created but not packed until main UI shown)
        self.status_bar = Label(self.root, textvariable=self.status_var, bd=1, relief="sunken", anchor="w", font=("Segoe UI", 10))

    def show_main_ui(self):
        """Hide cover, show menu + main UI, instantiate backend and bind actions."""
        self.cover_frame.pack_forget()
        self.root.config(menu=self.menu_bar)
        self.main_frame.pack(fill="both", expand=True)
        self.status_bar.pack(side="bottom", fill="x")

        # instantiate backend once (safe to call multiple times if already exists)
        if not hasattr(self, 'backend'):
            self.backend = DNABarcodeBackend(self)
        else:
            # Re-bind UI actions if backend existed previously
            self.backend.bind_ui_actions()

if __name__ == "__main__":
    root = tk.Tk()
    app = DNABarcodeUI(root)
    root.mainloop()
