import tkinter as tk
from tkinter import Canvas, Button, Entry, Label, ttk
from tkinter.filedialog import askopenfilename
from pathlib import Path
from PIL import Image, ImageTk
import os
import tkinter.ttk as ttk
from tktooltip import ToolTip

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
# View Page: Frame 4
# ---------------------------
class ViewPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        OUTPUT_PATH = Path(__file__).parent
        ASSETS_PATH = OUTPUT_PATH / Path(r"assets/frame4")

        def relative_to_assets(path: str) -> Path:
            return ASSETS_PATH / Path(path)
        
        orig_width, orig_height = 1455, 1041
        new_width, new_height = 800, 600
        scale_x, scale_y = new_width / orig_width, new_height / orig_height
        canvas = tk.Canvas(self, bg="#FFFFFF", height=orig_height, width=orig_width,
                           bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)
        canvas.create_rectangle(0.0, 1.0, 235.0, 1042.0, fill="#79BCF7", outline="")
        canvas.create_rectangle(1063.0, 0.0, 1455.0, 81.0, fill="#DAEBF9", outline="")

        # Setting Page
        btn1_img = scaled_photoimage(str(relative_to_assets("button_1.png")), scale_x, scale_y)
        btn1 = Button(self, image=btn1_img, borderwidth=0, highlightthickness=0,
                      command=lambda: controller.show_frame("SettingPage"), relief="flat")
        btn1.image = btn1_img
        btn1.place(x=1.0 * scale_x, y=402.0 * scale_y, width=235.0 * scale_x, height=100.0 * scale_y)

        # View Page
        btn2_img = scaled_photoimage(str(relative_to_assets("button_2.png")), scale_x, scale_y)
        btn2 = Button(self, image=btn2_img, borderwidth=0, highlightthickness=0,
                      command=lambda: controller.show_frame("ViewPage"), relief="flat")
        btn2.image = btn2_img
        btn2.place(x=0.0 * scale_x, y=302.0 * scale_y, width=235.0 * scale_x, height=100.0 * scale_y)

        # Start Page
        btn3_img = scaled_photoimage(str(relative_to_assets("button_3.png")), scale_x, scale_y)
        btn3 = Button(self, image=btn3_img, borderwidth=0, highlightthickness=0,
                      command=lambda: controller.show_frame("StartPage"), relief="flat")
        btn3.image = btn3_img
        btn3.place(x=0.0 * scale_x, y=202.0 * scale_y, width=235.0 * scale_x, height=100.0 * scale_y)

        # Upload Page
        btn4_img = scaled_photoimage(str(relative_to_assets("button_4.png")), scale_x, scale_y)
        btn4 = Button(self, image=btn4_img, borderwidth=0, highlightthickness=0,
                      command=lambda: controller.show_frame("UploadPage"), relief="flat")
        btn4.image = btn4_img
        btn4.place(x=0.0 * scale_x, y=102.0 * scale_y, width=235.0 * scale_x, height=100.0 * scale_y)

        # Home Page
        btn5_img = scaled_photoimage(str(relative_to_assets("button_5.png")), scale_x, scale_y)
        btn5 = Button(self, image=btn5_img, borderwidth=0, highlightthickness=0,
                      command=lambda: controller.show_frame("HomePage"), relief="flat")
        btn5.image = btn5_img
        btn5.place(x=0.0 * scale_x, y=1.5 * scale_y, width=235.0 * scale_x, height=100.0 * scale_y)

        entry_image_1 = scaled_photoimage(str(relative_to_assets("entry_1.png")), scale_x, scale_y)
        entry_bg_1 = canvas.create_image(1301.0 * scale_x, 40.5 * scale_y, image=entry_image_1)
        self.entry_1 = Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        self.entry_1.place(x=1167.0 * scale_x, y=14.0 * scale_y, width=268.0 * scale_x, height=51.0 * scale_y)
        self.entry_1.bind("<KeyRelease>", self.filter_table)

        #logo iamge
        img1 = scaled_photoimage(str(relative_to_assets("image_1.png")), scale_x, scale_y)
        canvas.create_image(215.0 * scale_x, 1700.0 * scale_y, image=img1)
        canvas.image = img1

        #search icon
        image_2 = scaled_photoimage(str(relative_to_assets("image_2.png")), scale_x, scale_y)
        canvas.create_image(2050.0 * scale_x, 70.0 * scale_y, image=image_2)
        canvas.image = image_2
        #ToolTip(image_2, msg="Click to Search Schedule", delay=1.0)

        canvas.create_text(1980.0 * scale_x, 195.0 * scale_y, anchor="nw",
                           text="SORT BY:", fill="#094478",
                           font=("Jomolhari Regular", int(18* scale_y)))
        
        # Export Button
        button_image_6 = scaled_photoimage(str(relative_to_assets("button_6.png")), scale_x, scale_y)
        button_6 = Button(self, image=button_image_6, borderwidth=0, highlightthickness=0,
                          command=lambda: print("button_6 clicked"), relief="flat")
        button_6.image = button_image_6
        button_6.place(x=1167.0 * scale_x, y=864.0 * scale_y, width=200.0 * scale_x, height=101.0 * scale_y)
        button_image_7 = scaled_photoimage(str(relative_to_assets("button_7.png")), scale_x, scale_y)
        button_7 = Button(self, image=button_image_7, borderwidth=0, highlightthickness=0,
                          command=lambda: print("button_7 clicked"), relief="flat")
        ToolTip(button_6, msg="Export Schedule to .csv", delay=1.0)

        # Table section
        self.columns = ("Course ID", "Day", "Time", "Professor", "Room")
        global tree
        tree = ttk.Treeview(self, columns=self.columns, show="headings")
        for col in self.columns:
            tree.heading(col, text=col)
            tree.column(col, width=30, anchor="center")
        self.courses = []  # Save all courses for filtering
        for course in self.courses:
            tree.insert("", "end", values=course)
        tree_scroll = ttk.Scrollbar(self, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=tree_scroll.set)
        canvas.create_window(240, 9, width=801, height=1026, anchor="nw", window=tree)
        tree_scroll.place(x=555, y=6, height=590)
        self.tree = tree

        button_7.image = button_image_7
        button_7.place(x=1204.0 * scale_x, y=107.0 * scale_y, width=134.0 * scale_x, height=41.0 * scale_y)
        canvas.scale("all", 0, 0, scale_x, scale_y)

        #search function
    def filter_table(self, event):
        query = self.entry_1.get().lower()
        for item in self.tree.get_children():
            self.tree.delete(item)
        for row in self.courses:
            if any(query in str(cell).lower() for cell in row):
                self.tree.insert("", "end", values=row)
