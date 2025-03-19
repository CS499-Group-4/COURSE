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
# Home page: homePage
# ---------------------------

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        orig_width = 1455
        orig_height = 1041
        new_width = 800
        new_height = 600
        scale_x = new_width / orig_width
        scale_y = new_height / orig_height

        canvas = Canvas(self, bg="#FFFFFF", height=orig_height, width=orig_width,
                        bd=0, highlightthickness=0, relief="ridge")
        canvas.pack(fill="both", expand=True)
        
        canvas.create_rectangle(0.0, 1.0, 235.0, 1042.0, fill="#79BCF7", outline="")

# Navigation button: switch page
        btn1_img = scaled_photoimage(str(relative_to_assets("button_1.png")), scale_x, scale_y)
        btn1 = Button(self, image=btn1_img, borderwidth=0, highlightthickness=0,
                      command=lambda: controller.show_frame("SettingPage"), relief="flat")
        btn1.image = btn1_img
        btn1.place(x=1.0 * scale_x, y=402.0 * scale_y, width=235.0 * scale_x, height=100.0 * scale_y)
        
        btn2_img = scaled_photoimage(str(relative_to_assets("button_2.png")), scale_x, scale_y)
        btn2 = Button(self, image=btn2_img, borderwidth=0, highlightthickness=0,
                      command=lambda: controller.show_frame("ViewPage"), relief="flat")
        btn2.image = btn2_img
        btn2.place(x=0.0 * scale_x, y=302.0 * scale_y, width=235.0 * scale_x, height=100.0 * scale_y)
        
        btn3_img = scaled_photoimage(str(relative_to_assets("button_3.png")), scale_x, scale_y)
        btn3 = Button(self, image=btn3_img, borderwidth=0, highlightthickness=0,
                      command=lambda: controller.show_frame("StartPage"), relief="flat")
        btn3.image = btn3_img
        btn3.place(x=0.0 * scale_x, y=202.0 * scale_y, width=235.0 * scale_x, height=100.0 * scale_y)
        
        btn4_img = scaled_photoimage(str(relative_to_assets("button_4.png")), scale_x, scale_y)
        btn4 = Button(self, image=btn4_img, borderwidth=0, highlightthickness=0,
                      command=lambda: controller.show_frame("UploadPage"), relief="flat")
        btn4.image = btn4_img
        btn4.place(x=0.0 * scale_x, y=102.0 * scale_y, width=235.0 * scale_x, height=100.0 * scale_y)
        
        btn5_img = scaled_photoimage(str(relative_to_assets("button_5.png")), scale_x, scale_y)
        btn5 = Button(self, image=btn5_img, borderwidth=0, highlightthickness=0,
                      command=lambda: controller.show_frame("HomePage"), relief="flat")
        btn5.image = btn5_img
        btn5.place(x=0.0 * scale_x, y=1.5 * scale_y, width=235.0 * scale_x, height=100.0 * scale_y)
        
        #logo iamge
        img1 = scaled_photoimage(str(relative_to_assets("image_1.png")), scale_x, scale_y)
        canvas.create_image(215.0 * scale_x, 1700.0 * scale_y, image=img1)
        canvas.image = img1
        canvas.create_rectangle(257.0, 13.0, 1434.0, 1023.0, fill="#DAEBF9", outline="")
        canvas.scale("all", 0, 0, scale_x, scale_y)
        canvas.create_text(486.2366 * scale_x, 95.0247 * scale_y,
                           anchor="nw", text="Welcome to Course Scheduling System",
                           fill="#094478", font=("Roboto Black", int(30 * scale_y)))
        desc_text = (
            "                                             System Description:\n\n"
            "Make a compatible easy-to-use user interface within an application that allows\n"
            "the automated scheduling of university courses by the dean of a given department\n"
            "from imported data.\n\n"
            "User Instruction：\n"
            "1. Go to the `Input Data` module to enter course, faculty, and classroom details.\n"
            "2. Select `Generate Schedule` from the main dashboard to create the course schedule.\n"
            "3. View the generated schedule in `View Schedule` for a detailed overview.\n"
            "4. Use the `Conflict Resolution` module to address any detected issues.\n"
            "5. Generate reports in the `Reports` module for printing or sharing.\n"
            "6. Adjust system settings in the `Settings` module if needed.\n\n"
            "For additional help, click the `Help` button in the navigation bar."
        )
        canvas.create_text(366.4585 * scale_x, 234.97 * scale_y,
                           anchor="nw", text=desc_text, fill="#094478",
                           font=("Roboto Regular", int(20 * scale_y)))
