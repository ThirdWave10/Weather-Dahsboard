# ALL CODE UNDER THE COPYRIGHT OF SNAKE TECHNOLOGIES GLOBAL
# SNAKE TECHNOLOGIES©. (Not Official)

import os
import sys
import platform
import tkinter as tk
from tkinter import messagebox, ttk, PhotoImage

import request_api as req


# ---------- Utility Functions ----------

def resource_path(relative_path):
    """Get absolute path to resource (works for dev & PyInstaller)."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def safe_exit(window):
    window.destroy()
    sys.exit(0)


# ---------- Main UI ----------

def main_UI():
    loc_question = messagebox.askquestion(
        "Location Request",
        "Do you allow Snake Technologies to obtain your location for weather tracking purposes?"
    )

    if loc_question != "yes":
        messagebox.showinfo(
            "Application Quit",
            "Application quit due to location request being denied."
        )
        return

    # -------- Weather Data Fetch --------
    try:
        weather_data = req.request_weather(True)
        if not weather_data or len(weather_data) < 5:
            raise ValueError("Incomplete weather data received")
    except Exception as e:
        messagebox.showerror(
            "Weather Error",
            f"Failed to retrieve weather data.\n\n{e}"
        )
        return

    # -------- Window Setup --------
    window = tk.Tk()
    window.title("Snake Technologies Weather")
    window.attributes("-fullscreen", True)

    # Escape key exit
    window.bind("<Escape>", lambda e: safe_exit(window))

    title = tk.Label(
        window,
        text="Snake Technologies Weather App",
        font=("Arial", 40, "bold")
    )
    title.pack(pady=40)

    main_frame = tk.Frame(window)
    main_frame.pack(expand=True)

    # -------- Image --------
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(BASE_DIR, "weather_logo.png")
        image = PhotoImage(file=image_path)
        image_label = tk.Label(main_frame, image=image)
        image_label.image = image  # prevent GC
        image_label.grid(row=0, column=0, padx=50, pady=20)
    except Exception as e:
        image_label = tk.Label(
            main_frame,
            text="Weather Logo Not Found",
            font=("Arial", 16)
        )
        image_label.grid(row=0, column=0, padx=50, pady=20)
        print("Image error:", e)

    # -------- Weather Display --------
    weather_text = tk.Text(
        main_frame,
        width=60,
        height=20,
        font=("Arial", 16),
        bd=3,
        wrap="word"
    )
    weather_text.grid(row=0, column=1, padx=50, pady=20)

    weather_text.insert(
        tk.END,
        f"Last Updated: {weather_data[0]} {weather_data[4]} Time\n\n"
        f"Temperature: {weather_data[1]}\n\n"
        f"Wind Speed: {weather_data[2]}\n\n"
        f"Wind Direction: {weather_data[3]}"
    )

    weather_text.config(state="disabled")  # make read-only

    # -------- Exit Button --------
    exit_btn = tk.Button(
        window,
        text="Exit",
        font=("Arial", 20),
        command=lambda: safe_exit(window),
        width=10,
        bg="#737272",
        fg="black"
    )
    exit_btn.pack(pady=40)

    window.mainloop()


# ---------- Run Program ----------
if __name__ == "__main__":
    main_UI()
