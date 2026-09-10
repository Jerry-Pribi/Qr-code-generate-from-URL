from tkinter import *
import customtkinter as ctk


# ---- Import requests to know if URL exists ----
import requests
from urllib.parse import urlparse


# ---- Importing Qr-code ----
import qrcode


# ---- Importing Pillow to show image on root ----
from PIL import Image
import os
from pathlib import Path

# ---- Importing datime for SQLite
from datetime import *

# ---- Global variable to store current QR image (PIL.Image.Image) ----
current_qr_image = None
last_qr_id = None
# --- Importing sqlite3
import sqlite3
conn = sqlite3.connect("QR-code-history.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS historie (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT NOT NULL,
        name_file TEXT NOT NULL,
        date TEXT NOT NULL,
        download INTEGER NOT NULL DEFAULT 0
    )               
""")

# ---- GUI Setup ----
root = Tk()

width = 400
height = 440

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

center_x = int(screen_width / 2 - width / 2)
center_y = int(screen_height / 2 - height / 2)

root.geometry(f"{width}x{height}+{center_x}+{center_y}")
root.resizable(False, False)
root.title("QR Code Generator")
root.config(bg="gray")


# ---- Adding the Label_QR ----
Label_QR = None


# ---- def of delete QR ----
def del_QR():
    global Label_QR, current_qr_image

    if Label_QR is not None:
        Label_QR.destroy()
        Label_QR = None
    current_qr_image = None


# ---- def of Generate Button ----
def press_Button():
    global Label_QR, current_qr_image, last_qr_id

    raw = Entry_URL.get().strip()
    URL_text = raw
    name_text = Entry_QR_Name.get().strip()

    place_of_error = Label_Error.place(x=85, y=height / 2)

    if URL_text == "" and name_text == "":
        Label_Error.configure(
            text="You didn't entry any URL and name.",
            bg_color="black"
        )
        place_of_error
        return

    if URL_text == "":
        Label_Error.configure(
            text="You didn't entry any URL adress.",
            bg_color="black"
        )
        place_of_error
        return

    if name_text == "":
        Label_Error.configure(
            text="You didn't entry any file name!",
            bg_color="black"
        )
        place_of_error
        return

    if URL_text != "" and name_text != "":
        Label_Error.configure(text="", bg_color="gray")

    # ---- Adding the https part if user forget ----
    if not raw.startswith("https://") and not raw.startswith("http://"):
        URL_text = "https://" + raw

    parsed = urlparse(URL_text)

    if not parsed.scheme or not parsed.netloc:
        Label_Error.configure(
            text="Unreachable URL adress!",
            bg_color="black"
        )
        print("Unreachable URL adress")
        return

    # ---- trying if the response is reachable and URL's exists ----
    try:
        response = requests.get(URL_text, timeout=1)

        if response.status_code == 200:
            print("Your URL is correct!")

        else:
            Label_Error.configure(
                text="Your URL doesn't exist!",
                bg_color="black"
            )
            return

    except requests.exceptions.RequestException as e:
        # ---- Bad domain or something like that ----
        print("The URL isn't correcnt or is unreachable.")

        Label_Error.configure(
            text="The URL isn't correcnt or is unreachable.",
            bg_color="black"
        )

        Label_Error.place(x=50, y=height / 2)
        return

    # ---- If everything runs fine than... ----
    # If is there some old QR, he will be deleted
    del_QR()

    qr = qrcode.make(URL_text)

    # ---- from PilImage to -> PIL.Image.Image ----
    qr_pil_image = qr.get_image()
    current_qr_image = qr_pil_image

    # ---- creating the CTkImage frop qr ----
    qr_image = ctk.CTkImage(
        light_image=qr_pil_image,
        dark_image=qr_pil_image,
        size=(120, 120)
    )

    Label_QR = ctk.CTkLabel(
        root,
        text="",
        image=qr_image
    )

    Label_QR.image = qr_image
    Label_QR.place(x=140, y=220)
    
    # ---- taking it to SQLite database
    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    date_together = f"{year}-{month}-{day}"
    cursor.execute("INSERT INTO historie (url, name_file, date, download) VALUES (?, ?, ?, ?)", (Entry_URL.get(), Entry_QR_Name.get(), date_together, 0))
    conn.commit()
    last_qr_id = cursor.lastrowid


# --- def to download the image
def download_Button():
    global current_qr_image, last_qr_id
    
    if current_qr_image is None:
        Label_Error.configure(
            text="You need generate your QR code first.",
            bg_color="black"
        )
        Label_Error.place(x=70, y=height / 2)
        return

    downloads = Path.home() / "Downloads"
    downloads.mkdir(exist_ok=True)
    
    base_name = f"{Entry_QR_Name.get()}.jpg"
    path = downloads / base_name
    counter = 1
    while path.exists():
        base_name = f"{Entry_QR_Name.get().strip()}_{counter}.jpg"
        path = downloads / base_name
        counter += 1
        if counter > 1:
            Label_Error.configure(text="You already download your qr.", bg_color="black", text_color="red")
            Label_Error.place(x=85, y=180)
        
    current_qr_image.save(path)
    cursor.execute("UPDATE historie SET download = ? WHERE ID = ?", (1, last_qr_id))
    conn.commit()
   
# ---- Main Label of program ----
Label_Main = ctk.CTkLabel(
    root,
    text="Welcome to QR Code Generator",
    text_color="black",
    width=200,
    font=("Arial", 24),
    corner_radius=10
)

Label_Main.place(x=15, y=10)


# ---- Gui for URL part ----
Label_URL = ctk.CTkLabel(
    root,
    text="Enter URL:",
    text_color="black",
    font=("Arial", 20),
    width=200,
    corner_radius=10
)

Label_URL.place(x=15, y=40)

Entry_URL = ctk.CTkEntry(
    root,
    placeholder_text="Enter URL",
    text_color="white",
    width=width - 30,
    height=30,
    corner_radius=10,
    fg_color="black"
)

Entry_URL.place(x=15, y=70)
Entry_URL.bind("<KeyRelease>", lambda event: del_QR())


# ---- Button to generate QR Code ----
Button_Generate = ctk.CTkButton(
    root,
    text="Generate",
    text_color="white",
    width=75,
    height=40,
    corner_radius=10,
    fg_color="black",
    hover_color="gray",
    border_color="black",
    border_width=2,
    command=press_Button
)

Button_Generate.place(x=120, y=height - 70)


# ---- Download QR Code Button ----
Button_Download = ctk.CTkButton(
    root,
    text="Download",
    text_color="white",
    width=75,
    height=40,
    corner_radius=10,
    fg_color="black",
    hover_color="gray",
    border_color="black",
    border_width=2,
    command=download_Button
)

Button_Download.place(x=200, y=height - 70)


# ---- Name in folder for QR.jpg ----
Label_QR_Name = ctk.CTkLabel(
    root,
    text="Name in folder:",
    text_color="black",
    font=("Arial", 20),
    width=200,
    corner_radius=10
)

Label_QR_Name.place(x=15, y=105)

Entry_QR_Name = ctk.CTkEntry(
    root,
    placeholder_text="Enter name of QR:",
    text_color="white",
    width=width - 30,
    height=30,
    corner_radius=10,
    fg_color="black"
)

Entry_QR_Name.place(x=15, y=140)
Entry_QR_Name.bind("<KeyRelease>", lambda event: del_QR())


# ---- Label For Error ----
Label_Error = ctk.CTkLabel(
    root,
    text="",
    text_color="red",
    font=("Arial", 14, "bold"),
    width=200,
    corner_radius=10
)

Label_Error.place(x=85, y=height / 2)


# ---- Launching the program ----
root.mainloop()
