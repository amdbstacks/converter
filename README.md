# 🎬 Text to PDF Slide Converter

An elegant, lightweight, and zero-installation desktop application built in Python that automatically converts plain text files (`.txt` or extensionless) into landscape, slide-styled presentation PDFs (with beautiful black backgrounds and crisp white text).

Designed specifically for automated slide production, worship lyrics, presentations, and batch reporting, this application runs entirely standalone on both **Linux** and **Windows** without requiring a Python installation!

---

## ✨ Features

* **🔄 Dual Conversion Modes:** Supports single-file conversion or automatic folder batch processing.
* **🏷️ Smart Stanza Grouping:** Automatically detects empty lines in your text to group lines into beautiful, vertically centered slide stanzas.
* **👑 Dynamic Title Page:** Instantly transforms the very first line of your document into a prominent Bold Presentation Title slide.
* **🛡️ Smart Text Wrapping:** Long lines are automatically split and wrapped to guarantee your text never overflows the slide edges.
* **🌍 Universal Encoding:** Automatic character fallback to seamlessly handle accentuation (`~`, `´`, `ç`) on both operating systems.
* **⚡ Zero Installation:** Download the single binary for your OS, click, and run.

---

## 📂 Project Structure & Executables

Pre-compiled standalone binaries are available inside the `executables/` directory. You do not need to install Python or any dependencies to use them.

```text
├── executables/
│   ├── linux/
│   │   └── TextToSlide          # Native Linux executable (standalone binary)
│   └── windows/
│       └── TextToSlide.exe      # Portable Windows executable (.exe)
├── main.py                      # Original Python source code
└── README.md                    # Project documentation
```

---

## 🚀 How to Run the App (No Installation Required)

### 🐧 On Linux
1. Navigate to the `executables/linux/` directory.
2. Grant execution permission to the binary file. You can do this via terminal:
   ```bash
   chmod +x TextToSlide
   ```
   *(Or right-click the file, go to **Properties -> Permissions**, and check **"Allow executing file as program"**).*
3. Double-click the file or run `./TextToSlide` from the terminal to launch the interface.

### 🪟 On Windows
1. Navigate to the `executables/windows/` directory.
2. Double-click `TextToSlide.exe` to launch the application instantly. 
3. No console window or command prompt will block your screen.

---

## 📝 Example Text Format Guide

To achieve perfect slide formatting, arrange your source text file following this structure:

```text
Amazing Grace (How Sweet the Sound)

Amazing grace! how sweet the sound,
That saved a wretch like me!
I once was lost, but now am found,
Was blind, but now I see.

'Twas grace that taught my heart to fear,
And grace my fears relieved;
How precious did that grace appear
The hour I first believed!
```

* **Slide 1:** Will act as the presentation title: `"Amazing Grace (How Sweet the Sound)"` in a large `44pt` bold font.
* **Slide 2:** Will render the first stanza group perfectly centered at `36pt` font.
* **Slide 3:** Will render the second stanza group seamlessly.

---

## 🛠️ Built With

* **Python 3** - Programming language core.
* **Tkinter / TTK** - Native, modern cross-platform graphical user interface elements.
* **ReportLab** - High-fidelity programmatic PDF generating engine.
* **PyInstaller** - Standalone dependency packaging framework.

---

## 📄 License

This project is open-source and free to use. Modify, distribute, and adapt it however you like!
