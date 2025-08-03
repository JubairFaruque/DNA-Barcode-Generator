import os
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog, messagebox, Toplevel, ttk
import tkinter as tk  # ✅ Required for tk.Canvas and tk widgets
from PIL import Image, ImageTk

# Backend class to connect with the UI
class DNABarcodeBackend:
    def __init__(self, ui):
        self.ui = ui
        self.figure = None
        self.canvas = None
        self.storage_file = "saved_barcodes.json"
        self.saved_dir = "saved_barcodes"
        os.makedirs(self.saved_dir, exist_ok=True)
        self.bind_ui_actions()

    def bind_ui_actions(self):
        self.ui.load_button.config(command=self.load_from_file)
        self.ui.generate_button.config(command=self.generate_barcode)
        self.ui.save_button.config(command=self.save_barcode)
        self.ui.clear_button.config(command=self.clear_all)
        self.ui.menu_saved.entryconfig("📂 View Saved Barcodes", command=self.view_saved_barcodes)
        self.ui.menu_generate.entryconfig("🧬 Generate New Barcode", command=self.show_main_frame)

    def load_from_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("FASTA Files", "*.fasta")])
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    content = f.read().strip()
                    self.ui.sequence_text.delete("1.0", "end")
                    self.ui.sequence_text.insert("1.0", content)
                    self.ui.status_var.set(f"Loaded file: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not read file:\n{str(e)}")

    def generate_barcode(self):
        sequence = self.ui.sequence_text.get("1.0", "end").strip().upper()
        if not sequence or not all(base in "ATGC" for base in sequence):
            messagebox.showerror("Invalid Input", "Sequence must contain only A, T, G, C characters.")
            return

        color_map = {'A': 'red', 'T': 'green', 'G': 'blue', 'C': 'yellow'}
        self.figure, ax = plt.subplots(figsize=(len(sequence) * 0.2, 2))
        for i, base in enumerate(sequence):
            ax.add_patch(plt.Rectangle((i, 0), 1, 1, color=color_map.get(base, 'gray')))
        ax.set_xlim(0, len(sequence))
        ax.set_ylim(0, 1)
        ax.axis('off')

        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.ui.preview_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

        self.ui.status_var.set("Barcode generated successfully.")

    def save_barcode(self):
        if not self.figure:
            messagebox.showwarning("No Barcode", "Please generate a barcode first.")
            return

        sequence = self.ui.sequence_text.get("1.0", "end").strip().upper()
        filename = f"{self.saved_dir}/barcode_{len(sequence)}_{hash(sequence) % 100000}.png"
        try:
            self.figure.savefig(filename)
            self.save_metadata(sequence, filename)
            self.ui.status_var.set(f"Barcode saved to {filename}")
        except Exception as e:
            messagebox.showerror("Save Error", str(e))

    def save_metadata(self, sequence, filepath):
        data = []
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
        data.append({"sequence": sequence, "image": filepath})
        with open(self.storage_file, 'w') as f:
            json.dump(data, f, indent=2)

    def view_saved_barcodes(self):
        if not os.path.exists(self.storage_file):
            messagebox.showinfo("No Records", "No barcodes have been saved yet.")
            return

        with open(self.storage_file, 'r') as f:
            records = json.load(f)

        viewer = Toplevel(self.ui.root)
        viewer.title("Saved DNA Barcodes")
        viewer.geometry("700x500")

        frame = ttk.Frame(viewer, padding=10)
        frame.pack(fill='both', expand=True)

        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scroll_frame = ttk.Frame(canvas)

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for rec in records:
            sub = ttk.Frame(scroll_frame, relief="ridge", padding=10)
            sub.pack(pady=5, fill='x')

            seq_label = ttk.Label(sub, text=f"Sequence: {rec['sequence'][:60]}...", wraplength=600, justify='left')
            seq_label.pack(anchor="w")

            try:
                img = Image.open(rec['image']).resize((300, 60))
                img_tk = ImageTk.PhotoImage(img)
                img_label = ttk.Label(sub, image=img_tk)
                img_label.image = img_tk  # Keep reference
                img_label.pack(pady=5)
            except Exception as e:
                ttk.Label(sub, text="[Image Not Found]").pack()

    def clear_all(self):
        self.ui.sequence_text.delete("1.0", "end")
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None
        self.ui.status_var.set("Cleared.")

    def show_main_frame(self):
        self.ui.sequence_text.delete("1.0", "end")
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None
        self.ui.status_var.set("Ready")
        self.ui.main_frame.pack(fill='both', expand=True)
