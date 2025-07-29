import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox

class DNABarcodeUI:
    def __init__(self, root):
        self.root = root
        self.root.title("DNA Barcode Generator")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # Main Frame
        self.main_frame = ttk.Frame(self.root, padding=15)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        self.title_label = ttk.Label(self.main_frame, text="DNA Barcode Generator", font=("Helvetica", 18, "bold"))
        self.title_label.pack(pady=10)

        # Sequence Input Section
        input_label = ttk.Label(self.main_frame, text="Enter DNA Sequence:", font=("Helvetica", 12))
        input_label.pack(anchor=tk.W, pady=(10, 2))

        self.sequence_text = tk.Text(self.main_frame, height=5, font=("Courier New", 12))
        self.sequence_text.pack(fill=tk.X, padx=5, pady=5)

        # Buttons
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, pady=10)

        self.load_button = ttk.Button(self.button_frame, text="Load from File")
        self.load_button.pack(side=tk.LEFT, padx=5)

        self.generate_button = ttk.Button(self.button_frame, text="Generate Barcode")
        self.generate_button.pack(side=tk.LEFT, padx=5)

        self.save_button = ttk.Button(self.button_frame, text="Save Barcode")
        self.save_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = ttk.Button(self.button_frame, text="Clear")
        self.clear_button.pack(side=tk.LEFT, padx=5)

        # Barcode Display Area
        barcode_label = ttk.Label(self.main_frame, text="Barcode Preview:", font=("Helvetica", 12))
        barcode_label.pack(anchor=tk.W, pady=(20, 5))

        self.preview_frame = ttk.Frame(self.main_frame, relief=tk.SUNKEN, borderwidth=1)
        self.preview_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Status Bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W, padding=5)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

if __name__ == "__main__":
    root = tk.Tk()
    app = DNABarcodeUI(root)
    root.mainloop()
