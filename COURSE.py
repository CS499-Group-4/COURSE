﻿import tkinter as tk
from tkinter import Canvas, Button, Entry, Label, ttk
from tkinter.filedialog import askopenfilename
from pathlib import Path
from PIL import Image, ImageTk
import os

from pages.homePage import HomePage
from pages.startPage import StartPage
from pages.uploadPage import UploadPage
from pages.settingPage import SettingPage
from pages.conflictPage import ConflictPage
#from pages.viewPage import ViewPage
from pages.exportPage import ExportPage
from pages.viewPage_overall import ViewPageOverall
from pages.viewPage_course import ViewPageCourse
from pages.viewPage_faculty import ViewPageFaculty
from pages.viewPage_perferences import ViewPagePreference
from pages.viewPage_times import ViewPageTimes
from pages.viewPage_rooms import ViewPageRooms
from tkinterdnd2 import DND_FILES, TkinterDnD


# ---------------------------
# Common helper functions and resource paths
# ---------------------------
OUTPUT_PATH = Path(__file__).parent
# Other pages can be adjusted as needed
ASSETS_PATH = OUTPUT_PATH / Path(r"assets/framehome")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def scaled_photoimage(image_path: str, scale_x: float, scale_y: float) -> ImageTk.PhotoImage:
    img = Image.open(image_path)
    orig_width, orig_height = img.size
    new_size = (int(orig_width * scale_x), int(orig_height * scale_y))
    img = img.resize(new_size, resample=Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(img)

# ---------------------------
# Main application: manage the jump of each page# ---------------------------
class MainApp(TkinterDnD.Tk):
    
    def __init__(self):
        super().__init__()
        self.title("course")
        self.geometry("800x600")

        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        for F in (HomePage, StartPage, UploadPage, SettingPage, ConflictPage, ExportPage,ViewPageOverall,ViewPageCourse, ViewPageFaculty, ViewPagePreference, ViewPageTimes, ViewPageRooms):
        #for F in (HomePage, StartPage, UploadPage, SettingPage, ConflictPage, ViewPage, ExportPage,ViewPageOverall,ViewPageCourse, ViewPageFaculty, ViewPagePreference, ViewPageTimes, ViewPageRooms):
            pageName = F.__name__
            page = F(parent=container, controller=self)
            self.frames[pageName] = page
            page.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame("HomePage")
    
    def show_frame(self, page_class):
        frame = self.frames[page_class]
        frame.tkraise()

# ---------------------------
# Program entry
# ---------------------------
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()



