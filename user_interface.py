import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Color mapping for nucleotides
COLOR_MAP = {
    'A': 'red',
    'T': 'green',
    'G': 'blue',
    'C': 'yellow'
}

# Barcode generation logic
def generate_barcode(sequence):
    sequence = sequence.upper()
    fig, ax = plt.subplots(figsize=(len(sequence) * 0.2, 2))
    for i, base in enumerate(sequence):
        color = COLOR_MAP.get(base, 'gray')
        ax.add_patch(plt.Rectangle((i, 0), 1, 1, color=color))
    ax.set_xlim(0, len(sequence))
    ax.set_ylim(0, 1)
    ax.axis('off')
    return fig

# Main UI class
class DNABarcodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DNA Barcode Generator")

        # Layout
        self.frame = ttk.Frame(root, padding=10)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.label = ttk.Label(self.frame, text="Enter DNA Sequence:")
        self.label.pack(anchor=tk.W)

        self.sequence_entry = tk.Text(self.frame, height=4, width=50)
        self.sequence_entry.pack()

        self.generate_btn = ttk.Button(self.frame, text="Generate Barcode", command=self.on_generate)
        self.generate_btn.pack(pady=5)

        self.save_btn = ttk.Button(self.frame, text="Save as Image", command=self.on_save)
        self.save_btn.pack(pady=5)

        self.canvas_frame = ttk.Frame(self.frame)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = None
        self.fig = None

    def on_generate(self):
        sequence = self.sequence_entry.get("1.0", tk.END).strip()
        if not all(base in "ATGC" for base in sequence.upper()):
            messagebox.showerror("Invalid Input", "Sequence must contain only A, T, G, C characters.")
            return
        self.fig = generate_barcode(sequence)
        self.display_barcode()

    def display_barcode(self):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def on_save(self):
        if not self.fig:
            messagebox.showwarning("Nothing to Save", "Please generate a barcode first.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG Image", "*.png")])
        if file_path:
            self.fig.savefig(file_path)
            messagebox.showinfo("Saved", f"Barcode image saved to {file_path}")

# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = DNABarcodeApp(root)
    root.mainloop()
