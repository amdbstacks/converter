import os
import sys

# CRITICAL LINUX FIX: Enables accent typing (like ~, ´, ç) within Tkinter fields
if sys.platform.startswith('linux'):
    os.environ["XMODIFIERS"] = "@im=none"

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle


class PDFConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Text to PDF Slide Converter")
        self.root.geometry("750x350")
        self.root.resizable(False, False)

        # Control variables
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.batch_mode = tk.BooleanVar(value=False)

        # Graphical User Interface
        self.create_widgets()

    def create_widgets(self):
        # Style configuration for the conversion action button
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Arial", 11, "bold"), foreground="white", background="#2ecc71")

        # Input Frame
        input_frame = ttk.LabelFrame(self.root, text=" 1. Select Source (TXT / Plain Text) ", padding=10)
        input_frame.pack(fill="x", padx=15, pady=10)

        ttk.Radiobutton(input_frame, text="Single File", variable=self.batch_mode, value=False,
                        command=self.update_labels).grid(row=0, column=0, sticky="w", padx=5)
        ttk.Radiobutton(input_frame, text="Folder (Batch Mode)", variable=self.batch_mode, value=True,
                        command=self.update_labels).grid(row=0, column=1, sticky="w", padx=5)

        self.lbl_input = ttk.Label(input_frame, text="File:")
        self.lbl_input.grid(row=1, column=0, pady=5, sticky="w", padx=5)

        self.entry_input = ttk.Entry(input_frame, textvariable=self.input_path, width=60)
        self.entry_input.grid(row=1, column=1, padx=5, sticky="ew")

        btn_browse_in = ttk.Button(input_frame, text="Browse", command=self.select_input)
        btn_browse_in.grid(row=1, column=2, padx=5)

        # Output Frame
        output_frame = ttk.LabelFrame(self.root, text=" 2. Select PDF Destination ", padding=10)
        output_frame.pack(fill="x", padx=15, pady=10)

        ttk.Label(output_frame, text="Output Folder:").grid(row=0, column=0, pady=5, sticky="w", padx=5)

        entry_output = ttk.Entry(output_frame, textvariable=self.output_path, width=60)
        entry_output.grid(row=0, column=1, padx=5, sticky="ew")

        btn_browse_out = ttk.Button(output_frame, text="Browse", command=self.select_output)
        btn_browse_out.grid(row=0, column=2, padx=5)

        # Column weight adjustment to automatically expand fields if necessary
        input_frame.columnconfigure(1, weight=1)
        output_frame.columnconfigure(1, weight=1)

        # Progress Bar Frame (Loading)
        self.progress_frame = ttk.Frame(self.root)
        self.progress_frame.pack(fill="x", padx=15, pady=10)

        self.progress_bar = ttk.Progressbar(self.progress_frame, orient="horizontal", mode="determinate")
        self.progress_bar.pack(fill="x")

        self.lbl_status = ttk.Label(self.progress_frame, text="Waiting to start...", foreground="gray")
        self.lbl_status.pack(pady=5)

        # Action Button
        self.btn_convert = ttk.Button(self.root, text="CONVERT TO PDF SLIDES", style="Accent.TButton",
                                      command=self.start_conversion)
        self.btn_convert.pack(pady=5, ipady=5)

    def update_labels(self):
        if self.batch_mode.get():
            self.lbl_input.config(text="Source Folder:")
        else:
            self.lbl_input.config(text="File:")
        self.input_path.set("")

    def select_input(self):
        if self.batch_mode.get():
            folder = filedialog.askdirectory(title="Select Folder containing Text Files")
            if folder: self.input_path.set(folder)
        else:
            file = filedialog.askopenfilename(
                title="Select Text File",
                filetypes=[("All Files", "*"), ("Text Files", "*.txt")]
            )
            if file: self.input_path.set(file)

    def select_output(self):
        folder = filedialog.askdirectory(title="Select PDF Output Folder")
        if folder: self.output_path.set(folder)

    def generate_pdf_slide(self, txt_path, destination_folder):
        pure_name = os.path.splitext(os.path.basename(txt_path))[0]
        pdf_path = os.path.join(destination_folder, f"{pure_name}.pdf")

        raw_lines = []
        for encoding in ['utf-8', 'latin-1', 'cp1252']:
            try:
                with open(txt_path, 'r', encoding=encoding) as f:
                    raw_lines = f.readlines()
                break
            except UnicodeDecodeError:
                continue

        if not raw_lines:
            return False

        slide_contents = []
        current_block = []
        title = ""

        for line in raw_lines:
            clean_line = line.strip()

            if not title and clean_line:
                title = clean_line
                continue

            if clean_line:
                current_block.append(clean_line)
            else:
                if current_block:
                    slide_contents.append(current_block)
                    current_block = []

        if current_block:
            slide_contents.append(current_block)

        width, height = landscape(letter)
        c = canvas.Canvas(pdf_path, pagesize=(width, height))

        style_title = ParagraphStyle(
            'TitleStyle',
            fontName='Helvetica-Bold',
            fontSize=44,
            leading=52,
            textColor='white',
            alignment=1
        )

        style_body = ParagraphStyle(
            'BodyStyle',
            fontName='Helvetica',
            fontSize=36,
            leading=44,
            textColor='white',
            alignment=1
        )

        lateral_margin = 50
        available_width = width - (lateral_margin * 2)

        # --- RENDER SLIDE 1: Document Title ---
        if title:
            c.setFillColorRGB(0, 0, 0)
            c.rect(0, 0, width, height, fill=True, stroke=False)

            p = Paragraph(title, style_title)
            p_width, p_height = p.wrap(available_width, height)
            p.drawOn(c, lateral_margin, (height / 2) - (p_height / 2))
            c.showPage()

        # --- RENDER SUBSEQUENT SLIDES: Organized Text Stanzas ---
        for block in slide_contents:
            c.setFillColorRGB(0, 0, 0)
            c.rect(0, 0, width, height, fill=True, stroke=False)

            block_paragraphs = []
            total_block_height = 0

            for line_text in block:
                p = Paragraph(line_text, style_body)
                p_width, p_height = p.wrap(available_width, height)
                block_paragraphs.append((p, p_height))
                total_block_height += p_height

            y_current = (height / 2) + (total_block_height / 2)

            for p, p_height in block_paragraphs:
                y_current -= p_height
                p.drawOn(c, lateral_margin, y_current)

            c.showPage()

        c.save()
        return True

    def start_conversion(self):
        source = self.input_path.get()
        destination = self.output_path.get()

        if not source or not os.path.exists(source):
            messagebox.showerror("Error", "Please select a valid source file or folder.")
            return
        if not destination:
            messagebox.showerror("Error", "Please select a valid output folder.")
            return

        if not os.path.exists(destination):
            try:
                os.makedirs(destination, exist_ok=True)
            except Exception as e:
                messagebox.showerror("Error", f"Could not create output folder:\n{str(e)}")
                return

        files_to_process = []

        if self.batch_mode.get():
            for f in os.listdir(source):
                full_path = os.path.join(source, f)
                if os.path.isfile(full_path):
                    files_to_process.append(full_path)
        else:
            files_to_process.append(source)

        total = len(files_to_process)
        if total == 0:
            messagebox.showwarning("Warning", "No files found to process.")
            return

        self.progress_bar["maximum"] = total
        self.btn_convert.config(state="disabled")

        success_count = 0
        for i, file_path in enumerate(files_to_process):
            self.lbl_status.config(text=f"Processing {i + 1}/{total}: {os.path.basename(file_path)}...")
            self.root.update()

            if self.generate_pdf_slide(file_path, destination):
                success_count += 1

            self.progress_bar["value"] = i + 1
            self.root.update()

        self.btn_convert.config(state="normal")
        self.lbl_status.config(text="Completed!", fg="green")
        messagebox.showinfo("Success",
                            f"Process finished!\n{success_count} out of {total} PDFs generated successfully.")
        self.progress_bar["value"] = 0
        self.lbl_status.config(text="Waiting to start...", fg="gray")


if __name__ == "__main__":
    root = tk.Tk()
    app = PDFConverterApp(root)
    root.mainloop()
