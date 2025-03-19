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
# UploadPage
# ---------------------------
class UploadPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        OUTPUT_PATH = Path(__file__).parent
        ASSETS_PATH = OUTPUT_PATH / Path(r"assets/frame1")
        def relative_to_assets(path: str) -> Path:
            return ASSETS_PATH / Path(path)

        orig_width = 1455
        orig_height = 1041
        new_width = 800
        new_height = 600
        scale_x = new_width / orig_width
        scale_y = new_height / orig_height

        self.canvas = Canvas(self, bg="#FFFFFF", height=orig_height, width=orig_width,
                             bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)
        
        self.canvas.create_rectangle(0.0, 1.0, 235.0, 1042.0, fill="#79BCF7", outline="")

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
        
       # File upload part: display the selected file name
        self.selected_file_text_id = self.canvas.create_text(
            481.0 * scale_x, 299.0 * scale_y,
            anchor="nw", text="File name", fill="#094478",
            font=("Roboto Black", int(20 * scale_y))
        )
        
        def upload_file():
            file_path = askopenfilename(
                title="choose file",
                filetypes=(("all file", "*.*"), ("text file", "*.txt"), ("Excel file", "*.xlsx"))
            )
            if file_path:
                selected_name = os.path.basename(file_path)
                print("choosed file path:", file_path)
                self.canvas.itemconfig(self.selected_file_text_id, text=selected_name)
        
        # File upload button: covers a large area, click to trigger upload
        btn6_img = scaled_photoimage(str(relative_to_assets("button_6.png")), scale_x, scale_y)
        btn6 = Button(self, image=btn6_img, borderwidth=0, highlightthickness=0,
                      command=upload_file, relief="flat")
        btn6.image = btn6_img
        btn6.place(x=250.0 * scale_x, y=25.0 * scale_y, width=1177.0 * scale_x, height=211.0 * scale_y)
        
        self.canvas.create_text(481.0 * scale_x, 452.0 * scale_y, anchor="nw",
                           text="File name", fill="#094478", font=("Roboto Black", int(20 * scale_y)))
        self.canvas.create_text(482.0 * scale_x, 615.0 * scale_y, anchor="nw",
                           text="File name", fill="#094478", font=("Roboto Black", int(20 * scale_y)))
        #logo img
        img1 = scaled_photoimage(str(relative_to_assets("image_1.png")), scale_x, scale_y)
        self.canvas.create_image(215.0 * scale_x, 1700.0 * scale_y, image=img1)
        self.canvas.image = img1
        
        #upload success img
        img2 = scaled_photoimage(str(relative_to_assets("image_2.png")), scale_x, scale_y)
        self.canvas.create_image(372.0 * scale_x, 322.0 * scale_y, image=img2)
        #uploading img
        img3 = scaled_photoimage(str(relative_to_assets("image_3.png")), scale_x, scale_y)
        self.canvas.create_image(372.0 * scale_x, 467.0 * scale_y, image=img3)
        #upload failed img
        img4 = scaled_photoimage(str(relative_to_assets("image_4.png")), scale_x, scale_y)
        self.canvas.create_image(372.0 * scale_x, 633.0 * scale_y, image=img4)
        #deleted file img
        img5 = scaled_photoimage(str(relative_to_assets("image_5.png")), scale_x, scale_y)
        self.canvas.create_image(1239.0 * scale_x, 317.0 * scale_y, image=img5)
        
        self.canvas.scale("all", 0, 0, scale_x, scale_y)

