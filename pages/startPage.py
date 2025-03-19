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
# StartPage
# ---------------------------
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        OUTPUT_PATH = Path(__file__).parent
        ASSETS_PATH = OUTPUT_PATH / Path(r"assets/frame2")
        def relative_to_assets(path: str) -> Path:
            return ASSETS_PATH / Path(path)

        orig_width, orig_height = 1455, 1041
        new_width, new_height = 800, 600
        scale_x, scale_y = new_width / orig_width, new_height / orig_height

        canvas = Canvas(self, bg="#FFFFFF", height=orig_height, width=orig_width,
                        bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)
        
        canvas.create_rectangle(0.0, 1.0, 235.0, 1042.0, fill="#79BCF7", outline="")
        
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
        
        # Canvas（Logo）
        image_1 = scaled_photoimage(str(relative_to_assets("image_1.png")), scale_x, scale_y)
        canvas.create_image(215.0 * scale_x, 1700.0 * scale_y, image=image_1)
        
        canvas.create_rectangle(918.0, 1.0, 1458.0, 1042.0, fill="#DAEBF9", outline="")
        
        # Upper right button
        button_image_6 = scaled_photoimage(str(relative_to_assets("button_6.png")), scale_x, scale_y)
        button_6 = Button(self, image=button_image_6, borderwidth=0, highlightthickness=0,
                          command=lambda: print("button_6 clicked"), relief="flat")
        button_6.image = button_image_6
        button_6.place(x=942.0 * scale_x, y=36.0 * scale_y, width=206.0 * scale_x, height=101.0 * scale_y)
        
        button_image_7 = scaled_photoimage(str(relative_to_assets("button_7.png")), scale_x, scale_y)
        button_7 = Button(self, image=button_image_7, borderwidth=0, highlightthickness=0,
                          command=lambda: print("button_7 clicked"), relief="flat")
        button_7.image = button_image_7
        button_7.place(x=1224.0 * scale_x, y=36.0 * scale_y, width=200.0 * scale_x, height=112.0 * scale_y)
        
       # Status and conflict summary text
        canvas.create_text(2000.0 * scale_x, 270.0 * scale_y, anchor="nw",
                           text="Status:", fill="#094478",
                           font=("Jomolhari Regular", int(20 * scale_y)))
        canvas.create_rectangle(935.0, 339.0, 1435.0, 818.0, fill="#FFFFFF", outline="")
        canvas.create_text(1064.0, 339.0, anchor="nw",
                           text="Conflict  Summary：", fill="#094478",
                           font=("Jomolhari Regular", int(20 * -1)))
        canvas.create_text(1800.0 * scale_x, 350.0 * scale_y, anchor="nw",
                           text="status info", fill="#000000",
                           font=("Jomolhari Regular", int(15 * scale_y)))
        
        # Lower right button
        button_image_8 = scaled_photoimage(str(relative_to_assets("button_8.png")), scale_x, scale_y)
        button_8 = Button(self, image=button_image_8, borderwidth=0, highlightthickness=0,
                          command=lambda: print("button_8 clicked"), relief="flat")
        button_8.image = button_image_8
        button_8.place(x=1206.0 * scale_x, y=737.0 * scale_y, width=200.0 * scale_x, height=65.0 * scale_y)
        
        button_image_9 = scaled_photoimage(str(relative_to_assets("button_9.png")), scale_x, scale_y)
        button_9 = Button(self, image=button_image_9, borderwidth=0, highlightthickness=0,
                      command=lambda: controller.show_frame("ConflictPage"), relief="flat")
        button_9.image = button_image_9
        button_9.place(x=972.0 * scale_x, y=741.0 * scale_y, width=200.0 * scale_x, height=61.0 * scale_y)
        
        button_image_10 = scaled_photoimage(str(relative_to_assets("button_10.png")), scale_x, scale_y)
        button_10 = Button(self, image=button_image_10, borderwidth=0, highlightthickness=0,
                           command=lambda: print("button_10 clicked"), relief="flat")
        button_10.image = button_image_10
        button_10.place(x=942.0 * scale_x, y=893.0 * scale_y, width=200.0 * scale_x, height=101.0 * scale_y)
        
        button_image_11 = scaled_photoimage(str(relative_to_assets("button_11.png")), scale_x, scale_y)
        button_11 = Button(self, image=button_image_11, borderwidth=0, highlightthickness=0,
                           command=lambda: print("button_11 clicked"), relief="flat")
        button_11.image = button_image_11
        button_11.place(x=1224.0 * scale_x, y=893.0 * scale_y, width=200.0 * scale_x, height=101.0 * scale_y)
        
        # Divider
        canvas.create_rectangle(916.98816, 153.4765, 1455.01141, 154.4765, fill="#094478", outline="")
        canvas.create_rectangle(918.0, 314.0, 1456.02325, 315.0, fill="#094478", outline="")
        
        # Table section
        columns = ("Course ID", "Course Name", "Time", "Room", "Professor", "Days")
        tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=30, anchor="center")
        courses = [
            ("CS 115", "Intro to Programming", "9:00 AM - 10:30 AM", "Room 341", "Dr. Echo", "Mon, Wed"),
            ("CS 310", "Data Structures", "10:45 AM - 12:15 PM", "Room 243", "Dr. Juliet", "Tue, Thu"),
            ("CS 382", "Algorithms", "1:00 PM - 2:30 PM", "Room 341", "Dr. Lima", "Mon, Wed, Fri"),
            ("CS 419", "Artificial Intelligence", "2:45 PM - 4:15 PM", "Room 134", "Dr. Lima", "Tue, Thu"),
            ("CS 438", "Machine Learning", "4:30 PM - 6:00 PM", "Room 241", "Dr. November", "Mon, Wed"),
            ("CS 452", "Computer Security", "6:15 PM - 7:45 PM", "Room 244", "Dr. Foxtrot", "Tue, Thu"),
            ("CS 501", "Advanced Programming", "8:00 AM - 9:30 AM", "Room 244", "Dr. November", "Mon, Wed"),
            ("CS 558", "Cryptography", "9:45 AM - 11:15 AM", "Room 244", "Dr. Hotel", "Tue, Thu"),
            ("CS 572", "Deep Learning", "11:30 AM - 1:00 PM", "Room 244", "Dr. Dog", "Mon, Wed, Fri"),
        ]
        for course in courses:
            tree.insert("", "end", values=course)
        tree_scroll = ttk.Scrollbar(self, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=tree_scroll.set)
        canvas.create_window(240, 9, width=671, height=1026, anchor="nw", window=tree)
        tree_scroll.place(x=500, y=6, height=1025)
        
        canvas.scale("all", 0, 0, scale_x, scale_y)