QR Code Generator

A simple desktop Python application with a graphical interface (Tkinter + CustomTkinter) that generates a QR code from a given URL and lets you download it as an image.

Features
Enter a URL (if http:///https:// is missing, https:// is added automatically)
Validates whether the URL is well-formed and reachable (checked via the requests library)
Generates a QR code from a valid URL and displays it in the app window
Lets you choose a custom file name for saving the QR code
Downloads the generated QR code to the Downloads folder as a .jpg file
Automatically avoids overwriting existing files (appends _1, _2, ...)
Shows error messages for invalid input
Requirements
Python 3.8+
Libraries:
customtkinter
requests
qrcode
Pillow
Installation
bash
pip install customtkinter requests qrcode pillow

Note: tkinter ships with most standard Python installations (on Linux you may need to install the python3-tk package separately).

Usage
bash
python gui_qr.py
Enter a web address in the Enter URL field.
Enter a file name in the Name in folder field.
Click Generate — the app checks the URL's availability and creates the QR code.
Click Download — the QR code is saved to your ~/Downloads folder as a .jpg file.
Project structure
gui_qr.py   # main and only application file
Possible future improvements
Add options for output format (PNG, SVG) and QR code colors
Allow choosing a custom destination folder for saving
Support URL validation without a network request (offline mode)
Larger QR code preview
Improve layout (currently uses fixed coordinates via place())
