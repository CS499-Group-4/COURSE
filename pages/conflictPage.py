import tkinter as tk
from tkinter import Canvas, Button, Entry, Label, ttk
from tkinter.filedialog import askopenfilename
from pathlib import Path
from PIL import Image, ImageTk
import os

# ---------------------------
# Common helper functions and resource paths
# ---------------------------
OUTPUT_PATH = Path(__file__).parent
# Other pages can be adjusted as needed
ASSETS_PATH = OUTPUT_PATH / Path(r"assets/frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def scaled_photoimage(image_path: str, scale_x: float, scale_y: float) -> ImageTk.PhotoImage:
    img = Image.open(image_path)
    orig_width, orig_height = img.size
    new_size = (int(orig_width * scale_x), int(orig_height * scale_y))
    img = img.resize(new_size, resample=Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(img)

# ---------------------------
# Conflict Page
# ---------------------------
class ConflictPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        OUTPUT_PATH = Path(__file__).parent
        ASSETS_PATH = OUTPUT_PATH / Path(r"assets/frame3")
        def relative_to_assets(path: str) -> Path:
            return ASSETS_PATH / Path(path)

        orig_width, orig_height = 1455, 1041
        new_width, new_height = 800, 600
        scale_x, scale_y = new_width / orig_width, new_height / orig_height

        canvas = tk.Canvas(self, bg="#FFFFFF", height=orig_height, width=orig_width,
                           bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)

        canvas.create_rectangle(
            1070.0, 0.0, 1455.0, 1041.0,
            fill="#79BCF7", outline=""
        )

        canvas.create_text(
            500.0, 20.0,
            anchor="nw",
            text="Conflict",
            fill="#094478",
            font=("Jomolhari Regular", 15)
        )

        canvas.create_rectangle(
            34.0, 104.0, 1034.0, 194.0,
            fill="#DAEBF9", outline=""
        )

        canvas.create_text(
            42.0, 140.0,
            anchor="nw",
            text="Conflict 1",
            fill="#094478",
            font=("Jomolhari Regular", 8)
        )
        canvas.create_text(
            141.0, 140.0,
            anchor="nw",
            text="Courses and professors",
            fill="#094478",
            font=("Jomolhari Regular", 8)
        )
        canvas.create_text(
            400.0, 140.0,
            anchor="nw",
            text="conflict reason",
            fill="#094478",
            font=("Jomolhari Regular", 8)
        )

        button_image_1 = scaled_photoimage(str(relative_to_assets("button_1.png")), scale_x, scale_y)
        button_1 = ttk.Button(self, image=button_image_1, command=lambda: print("button_1 clicked"))
        button_1.image = button_image_1  # 保存引用
        button_1.place(
            x=1163.0 * scale_x, y=47.5 * scale_y,
            width=201.0 * scale_x, height=83.0 * scale_y
        )

        button_image_2 = scaled_photoimage(str(relative_to_assets("button_2.png")), scale_x, scale_y)
        button_2 = ttk.Button(self, image=button_image_2, command=lambda: print("button_2 clicked"))
        button_2.image = button_image_2
        button_2.place(
            x=1163.0 * scale_x, y=217.0 * scale_y,
            width=201.0 * scale_x, height=83.0 * scale_y
        )

        button_image_3 = scaled_photoimage(str(relative_to_assets("button_3.png")), scale_x, scale_y)
        button_3 = ttk.Button(self, image=button_image_3, command=lambda: print("button_3 clicked"))
        button_3.image = button_image_3
        button_3.place(
            x=1163.0 * scale_x, y=398.0 * scale_y,
            width=201.0 * scale_x, height=83.0 * scale_y
        )

        button_image_4 = scaled_photoimage(str(relative_to_assets("button_4.png")), scale_x, scale_y)
        button_4 = Button(self, image=button_image_4, command=lambda: controller.show_frame("StartPage"), relief="flat")
        button_4.image = button_image_4
        button_4.place(x=1163.0 * scale_x, y=587.0 * scale_y, width=201.0 * scale_x, height=83.0 * scale_y)


        options_5 = ["chooes A", "chooes B", "choose C"]
        options_6 = ["choose X", "choose Y", "choose Z"]
        dropdown_var_5 = tk.StringVar()
        dropdown_var_6 = tk.StringVar()

        dropdown_5 = ttk.Combobox(self, textvariable=dropdown_var_5, values=options_5, state="readonly")
        dropdown_5.set("room")
        dropdown_5.place(
            x=638.0 * scale_x, y=128.0 * scale_y,
            width=111.0 * scale_x, height=50.0 * scale_y
        )
        dropdown_5.bind("<<ComboboxSelected>>", lambda e: print(f"Dropdown 5 choose: {dropdown_var_5.get()}"))

        dropdown_6 = ttk.Combobox(self, textvariable=dropdown_var_6, values=options_6, state="readonly")
        dropdown_6.set("time")
        dropdown_6.place(
            x=823.0 * scale_x, y=128.0 * scale_y,
            width=111.0 * scale_x, height=50.0 * scale_y
        )
        dropdown_6.bind("<<ComboboxSelected>>", lambda e: print(f"Dropdown 6 choose: {dropdown_var_6.get()}"))

        canvas.scale("all", 0, 0, scale_x, scale_y)