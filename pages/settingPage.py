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
# SettingPage
# ---------------------------
class SettingPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        OUTPUT_PATH = Path(__file__).parent
        ASSETS_PATH = OUTPUT_PATH / Path(r"assets/frame5")
        def relative_to_assets(path: str) -> Path:
            return ASSETS_PATH / Path(path)
        
        orig_width, orig_height = 1455, 1041
        new_width, new_height = 800, 600
        scale_x, scale_y = new_width / orig_width, new_height / orig_height
        
        canvas = Canvas(self, bg="#FFFFFF", height=orig_height, width=orig_width,
                        bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)
        
        canvas.create_rectangle(0.0, 1.0, 235.0, 1042.0, fill="#79BCF7", outline="")
        
        canvas.create_rectangle(296.0, 41.0, 1403.0, 148.0, fill="#DAEBF9", outline="")
        
        canvas.create_text(323.0, 76.0, anchor="nw", text="Font Setting:",
                           fill="#094478", font=("Jomolhari Regular", 10))
        
        canvas.create_rectangle(289.0, 502.0, 1396.0, 609.0, fill="#DAEBF9", outline="")
        canvas.create_rectangle(289.0, 697.0, 1403.0, 804.0, fill="#DAEBF9", outline="")
        
        canvas.create_rectangle(296.0, 239.0, 1403.0, 346.0, fill="#DAEBF9", outline="")
        canvas.create_text(323.0, 274.0, anchor="nw", text="Font Size:",
                           fill="#094478", font=("Jomolhari Regular", 10))
        
        canvas.create_text(296.0, 430.0, anchor="nw", text="Default display mode of class schedule: ",
                           fill="#094478", font=("Jomolhari Regular", 16))
        
        canvas.create_rectangle(502.0, 293.00000002561853, 1350.0000066752837, 298.0,
                                fill="#094478", outline="")
        
        canvas.create_text(330.0, 735.0, anchor="nw", text="Font Setting:",
                           fill="#094478", font=("Jomolhari Regular", 24))
        
        image_1 = scaled_photoimage(str(relative_to_assets("image_1.png")), scale_x, scale_y)
        canvas.create_image(215.0 * scale_x, 1700.0 * scale_y, image=image_1)
        
        # Navigation Buttons
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
        
        # Top right button (font setting control)
        button_image_6 = scaled_photoimage(str(relative_to_assets("button_6.png")), scale_x, scale_y)
        button_6 = Button(self, image=button_image_6, borderwidth=0, highlightthickness=0,
                          command=lambda: print("button_6 clicked"), relief="flat")
        button_6.image = button_image_6
        button_6.place(x=503.0 * scale_x, y=64.0 * scale_y, width=169.0 * scale_x, height=66.0 * scale_y)
        
        button_image_7 = scaled_photoimage(str(relative_to_assets("button_7.png")), scale_x, scale_y)
        button_7 = Button(self, image=button_image_7, borderwidth=0, highlightthickness=0,
                          command=lambda: print("button_7 clicked"), relief="flat")
        button_7.image = button_image_7
        button_7.place(x=503.0 * scale_x, y=64.0 * scale_y, width=169.0 * scale_x, height=66.0 * scale_y)
        
        button_image_8 = scaled_photoimage(str(relative_to_assets("button_8.png")), scale_x, scale_y)
        button_8 = Button(self, image=button_image_8, borderwidth=0, highlightthickness=0,
                          command=lambda: print("button_8 clicked"), relief="flat")
        button_8.image = button_image_8
        button_8.place(x=959.0 * scale_x, y=64.0 * scale_y, width=169.0 * scale_x, height=66.0 * scale_y)
        
        button_image_9 = scaled_photoimage(str(relative_to_assets("button_9.png")), scale_x, scale_y)
        button_9 = Button(self, image=button_image_9, borderwidth=0, highlightthickness=0,
                          command=lambda: print("button_9 clicked"), relief="flat")
        button_9.image = button_image_9
        button_9.place(x=1181.0 * scale_x, y=64.0 * scale_y, width=169.0 * scale_x, height=66.0 * scale_y)
        
        button_image_10 = scaled_photoimage(str(relative_to_assets("button_10.png")), scale_x, scale_y)
        button_10 = Button(self, image=button_image_10, borderwidth=0, highlightthickness=0,
                           command=lambda: print("button_10 clicked"), relief="flat")
        button_10.image = button_image_10
        button_10.place(x=727.0 * scale_x, y=64.0 * scale_y, width=169.0 * scale_x, height=66.0 * scale_y)
        
        # Lower button area
        canvas.create_rectangle(289.0, 502.0, 1396.0, 609.0, fill="#DAEBF9", outline="")
        canvas.create_rectangle(289.0, 697.0, 1403.0, 804.0, fill="#DAEBF9", outline="")
        
        button_image_11 = scaled_photoimage(str(relative_to_assets("button_11.png")), scale_x, scale_y)
        button_11 = Button(self, image=button_image_11, borderwidth=0, highlightthickness=0,
                           command=lambda: print("button_11 clicked"), relief="flat")
        button_11.image = button_image_11
        button_11.place(x=342.0 * scale_x, y=525.0 * scale_y, width=226.0 * scale_x, height=66.0 * scale_y)
        
        button_image_12 = scaled_photoimage(str(relative_to_assets("button_12.png")), scale_x, scale_y)
        button_12 = Button(self, image=button_image_12, borderwidth=0, highlightthickness=0,
                           command=lambda: print("button_12 clicked"), relief="flat")
        button_12.image = button_image_12
        button_12.place(x=729.0 * scale_x, y=525.0 * scale_y, width=226.0 * scale_x, height=66.0 * scale_y)
        
        button_image_13 = scaled_photoimage(str(relative_to_assets("button_13.png")), scale_x, scale_y)
        button_13 = Button(self, image=button_image_13, borderwidth=0, highlightthickness=0,
                           command=lambda: print("button_13 clicked"), relief="flat")
        button_13.image = button_image_13
        button_13.place(x=1116.0 * scale_x, y=525.0 * scale_y, width=226.0 * scale_x, height=66.0 * scale_y)
        
        canvas.create_rectangle(296.0, 239.0, 1403.0, 346.0, fill="#DAEBF9", outline="")
        canvas.create_text(323.0, 274.0, anchor="nw", text="Font Size:", fill="#094478", font=("Jomolhari Regular", 14))
        
        canvas.create_rectangle(502.0, 293.00000002561853, 1350.0000066752837, 298.0, fill="#094478", outline="")
        canvas.create_text(330.0, 735.0, anchor="nw", text="Font Setting:", fill="#094478", font=("Jomolhari Regular", 10))
        
        button_image_14 = scaled_photoimage(str(relative_to_assets("button_14.png")), scale_x, scale_y)
        button_14 = Button(self, image=button_image_14, borderwidth=0, highlightthickness=0,
                           command=lambda: print("button_14 clicked"), relief="flat")
        button_14.image = button_image_14
        button_14.place(x=551.0 * scale_x, y=718.0 * scale_y, width=298.0 * scale_x, height=66.0 * scale_y)
        
        button_image_15 = scaled_photoimage(str(relative_to_assets("button_15.png")), scale_x, scale_y)
        button_15 = Button(self, image=button_image_15, borderwidth=0, highlightthickness=0,
                           command=lambda: print("button_15 clicked"), relief="flat")
        button_15.image = button_image_15
        button_15.place(x=979.0 * scale_x, y=718.0 * scale_y, width=298.0 * scale_x, height=66.0 * scale_y)
        
        button_image_16 = scaled_photoimage(str(relative_to_assets("button_16.png")), scale_x, scale_y)
        button_16 = Button(self, image=button_image_16, borderwidth=0, highlightthickness=0,
                           command=lambda: print("button_16 clicked"), relief="flat")
        button_16.image = button_image_16
        button_16.place(x=377.0 * scale_x, y=888.0 * scale_y, width=348.0 * scale_x, height=94.0 * scale_y)
        
        button_image_17 = scaled_photoimage(str(relative_to_assets("button_17.png")), scale_x, scale_y)
        button_17 = Button(self, image=button_image_17, borderwidth=0, highlightthickness=0,
                           command=lambda: print("button_17 clicked"), relief="flat")
        button_17.image = button_image_17
        button_17.place(x=979.0 * scale_x, y=888.0 * scale_y, width=348.0 * scale_x, height=94.0 * scale_y)
        
        # 对所有 Canvas 项目进行统一缩放
        canvas.scale("all", 0, 0, scale_x, scale_y)