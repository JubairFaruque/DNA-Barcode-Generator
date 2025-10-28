import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk

class DNABarcodeBackend:
    def __init__(self, ui):
        self.ui = ui
        self.figure = None
        self.canvas = None
        self.saved_dir = "saved_barcodes"
        self.records_file = os.path.join(self.saved_dir, "records.json")
        os.makedirs(self.saved_dir, exist_ok=True)
        # create records file if missing
        if not os.path.exists(self.records_file):
            with open(self.records_file, "w") as f:
                json.dump([], f)
        self.bind_ui_actions()

    def bind_ui_actions(self):
        """Attach UI button commands and configure menu entries."""
        # Buttons
        self.ui.load_button.config(command=self.load_from_file)
        self.ui.generate_button.config(command=self.generate_barcode)
        self.ui.save_button.config(command=self.save_barcode_dialog)  # Save As flow
        self.ui.clear_button.config(command=self.clear_all)

        # Menus: they were created with one entry each (index 0). Configure them by index.
        try:
            self.ui.menu_saved.entryconfigure(0, command=self.view_saved_barcodes)
            self.ui.menu_generate.entryconfigure(0, command=self.show_main_frame)
        except Exception:
            # If menus are not available yet, ignore (they will be configured when UI shown)
            pass

    def load_from_file(self):
        path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("FASTA Files", "*.fasta")])
        if not path:
            return
        try:
            with open(path, "r") as f:
                content = f.read().strip()
            self.ui.sequence_text.delete("1.0", "end")
            self.ui.sequence_text.insert("1.0", content)
            self.ui.status_var.set(f"Loaded sequence from {os.path.basename(path)}")
        except Exception as e:
            messagebox.showerror("Load Error", str(e))

    def generate_barcode(self):
        seq = self.ui.sequence_text.get("1.0", "end").strip().upper()
        if not seq:
            messagebox.showwarning("Empty Sequence", "Please enter or load a DNA sequence first.")
            return
        if not all(ch in "ATGC" for ch in seq):
            messagebox.showerror("Invalid Sequence", "Sequence must contain only A, T, G, C characters.")
            return

        color_map = {'A':'#e6194b', 'T':'#3cb44b', 'G':'#4363d8', 'C':'#ffe119'}  # nicer colors
        # make figure width scale reasonably (min width 6)
        width = max(6, len(seq) * 0.2)
        self.figure, ax = plt.subplots(figsize=(width, 2))
        for i, base in enumerate(seq):
            ax.add_patch(plt.Rectangle((i, 0), 1, 1, color=color_map.get(base, 'gray')))
        ax.set_xlim(0, len(seq))
        ax.set_ylim(0, 1)
        ax.axis('off')

        # display in UI preview_frame
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.ui.preview_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        self.ui.status_var.set("Barcode generated successfully.")

    def save_barcode_dialog(self):
        """Open Save As dialog inside saved_barcodes folder, save image + sequence txt, and record metadata."""
        if not self.figure:
            messagebox.showwarning("No Barcode", "Please generate a barcode first.")
            return

        # suggested base name from first 12 chars of sequence
        seq = self.ui.sequence_text.get("1.0", "end").strip().upper()
        safe_name = "".join(ch for ch in seq[:12] if ch.isalnum())
        default_name = f"barcode_{safe_name or 'seq'}"

        initial_dir = os.path.abspath(self.saved_dir)
        os.makedirs(initial_dir, exist_ok=True)

        file_path = filedialog.asksaveasfilename(
            title="Save Barcode Image As",
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png")],
            initialdir=initial_dir,
            initialfile=default_name + ".png"
        )
        if not file_path:
            return  # user cancelled

        try:
            # save image
            self.figure.savefig(file_path)
            # save sequence to .txt with same base name
            base, _ = os.path.splitext(os.path.basename(file_path))
            seq_path = os.path.join(initial_dir, base + ".txt")
            with open(seq_path, "w") as f:
                f.write(seq)

            # add metadata record
            self._append_record(sequence=seq, image_path=file_path, seq_path=seq_path)
            self.ui.status_var.set(f"Saved: {os.path.basename(file_path)}")
            messagebox.showinfo("Saved", f"Image and sequence saved to:\n{file_path}\n{seq_path}")
        except Exception as e:
            messagebox.showerror("Save Error", str(e))

    def _append_record(self, sequence, image_path, seq_path):
        try:
            with open(self.records_file, "r") as f:
                records = json.load(f)
        except Exception:
            records = []
        records.append({"sequence": sequence, "image": image_path, "sequence_file": seq_path})
        with open(self.records_file, "w") as f:
            json.dump(records, f, indent=2)

    def view_saved_barcodes(self):
        """Open a window listing saved barcodes with preview thumbnails."""
        try:
            with open(self.records_file, "r") as f:
                records = json.load(f)
        except Exception:
            records = []

        if not records:
            messagebox.showinfo("No Saved Barcodes", "No saved barcodes found.")
            return

        viewer = Toplevel(self.ui.root)
        viewer.title("Saved DNA Barcodes")
        viewer.geometry("800x600")

        frame = ttk.Frame(viewer, padding=8)
        frame.pack(fill='both', expand=True)

        canvas = tk.Canvas(frame)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scroll_frame = ttk.Frame(canvas)

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for rec in records[::-1]:  # newest first
            sub = ttk.Frame(scroll_frame, relief="ridge", padding=8)
            sub.pack(fill='x', pady=6)

            seq_short = (rec.get("sequence")[:80] + '...') if len(rec.get("sequence",""))>80 else rec.get("sequence","")
            ttk.Label(sub, text=f"Sequence: {seq_short}", wraplength=600, justify='left').pack(anchor='w')

            img_path = rec.get("image")
            if img_path and os.path.exists(img_path):
                try:
                    thumb = Image.open(img_path)
                    thumb.thumbnail((500,120))
                    thumb_tk = ImageTk.PhotoImage(thumb)
                    lbl = ttk.Label(sub, image=thumb_tk)
                    lbl.image = thumb_tk  # keep reference
                    lbl.pack(pady=6)
                except Exception:
                    ttk.Label(sub, text="[Unable to load thumbnail]").pack()
            else:
                ttk.Label(sub, text="[Image not found]").pack()

            # add a button to open the image file in default viewer
            def _open_file(p=img_path):
                try:
                    os.startfile(p)
                except Exception as e:
                    messagebox.showerror("Open Error", str(e))
            open_btn = ttk.Button(sub, text="Open Image", command=_open_file)
            open_btn.pack(anchor='e')

    def clear_all(self):
        self.ui.sequence_text.delete("1.0", "end")
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None
        self.ui.status_var.set("Cleared.")

    def show_main_frame(self):
        """If called from menu, ensure main UI is visible (useful if cover still shown)."""
        # If cover is still up, simulate pressing Enter
        if getattr(self.ui, "cover_frame", None) and self.ui.cover_frame.winfo_ismapped():
            self.ui.show_main_ui()
        else:
            # ensure main frame visible
            self.ui.main_frame.pack(fill="both", expand=True)
            self.ui.status_var.set("Ready")
