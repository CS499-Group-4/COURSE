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
# Home page: homePage
# ---------------------------

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        orig_width = 1455
        orig_height = 1040
        self.orig_width = orig_width
        self.orig_height = orig_height
        new_width = 800
        new_height = 600
        self.scale_x = new_width / orig_width
        self.scale_y = new_height / orig_height

        self.canvas = Canvas(self, bg="#FFFFFF", height=orig_height, width=orig_width,
                        bd=0, highlightthickness=0, relief="ridge")
        self.canvas.pack(fill="both", expand=True)
        #self.canvas.create_rectangle(0.0, 0.0, 235.0, 1042.0, fill="#79BCF7", outline="")

        
        self.make_sideBar()
        self.bind("<Configure>", self.on_resize)

    def make_sideBar(self):

        self.canvas.create_rectangle(0.0, 0.0, 235.0 * self.scale_x, 1042.0, fill="#79BCF7", outline="")
        self.x = self.scale_x
        
       # Navigation button: switch page
       # ----------------------------HomePage------------------------------------------
        btn5_img = scaled_photoimage(str(relative_to_assets("button_5.png")), self.scale_x, self.scale_y)
        btn5 = Button(self, image=btn5_img, borderwidth=0, highlightthickness=0,
                      command=lambda: self.controller.show_frame("HomePage"), relief="flat")
        btn5.image = btn5_img
        btn5.place(x=0.0 * self.scale_x, y=0 * self.scale_y, width=235.0 * self.scale_x, height=100.0 * self.scale_y)  
       # ----------------------------UploadPage------------------------------------------
        btn4_img = scaled_photoimage(str(relative_to_assets("button_4.png")), self.scale_x, self.scale_y)
        btn4 = Button(self, image=btn4_img, borderwidth=0, highlightthickness=0,
                      command=lambda: self.controller.show_frame("UploadPage"), relief="flat")
        btn4.image = btn4_img
        btn4.place(x=0.0 * self.scale_x, y=100.0 * self.scale_y, width=235.0 * self.scale_x, height=100.0 * self.scale_y)
        # ----------------------------viewPage------------------------------------------
        btn4_img = scaled_photoimage(str(relative_to_assets("button_2.png")), self.scale_x, self.scale_y)
        btn4 = Button(self, image=btn4_img, borderwidth=0, highlightthickness=0,
                      command=lambda: self.controller.show_frame("ViewPageOverall"), relief="flat")
        btn4.image = btn4_img
        btn4.place(x=0.0 * self.scale_x, y=200.0 * self.scale_y, width=235.0 * self.scale_x, height=100.0 * self.scale_y)     
       # ----------------------------StartPage------------------------------------------
        btn3_img = scaled_photoimage(str(relative_to_assets("button_3.png")), self.scale_x, self.scale_y)
        btn3 = Button(self, image=btn3_img, borderwidth=0, highlightthickness=0,
                      command=lambda: self.controller.show_frame("StartPage"), relief="flat")
        btn3.image = btn3_img
        btn3.place(x=0.0 * self.scale_x, y=300.0 * self.scale_y, width=235.0 * self.scale_x, height=100.0 * self.scale_y)
       # ----------------------------ExportPage------------------------------------------
        btnexport_img = scaled_photoimage(str(relative_to_assets("export_button.png")), self.scale_x, self.scale_y)
        btnexport = Button(self, image=btnexport_img, borderwidth=0, highlightthickness=0,
                      command=lambda: self.controller.show_frame("ExportPage"), relief="flat")
        btnexport.image = btnexport_img
        btnexport.place(x=0.0 * self.scale_x, y=400.0 * self.scale_y, width=235.0 * self.scale_x, height=100.0 * self.scale_y)
        # ----------------------------SettingPage------------------------------------------
        btn1_img = scaled_photoimage(str(relative_to_assets("button_1.png")), self.scale_x, self.scale_y)
        btn1 = Button(self, image=btn1_img, borderwidth=0, highlightthickness=0,
                      command=lambda: self.controller.show_frame("SettingPage"), relief="flat")
        btn1.image = btn1_img
        btn1.place(x=0.0 * self.scale_x, y=500.0 * self.scale_y, width=235.0 * self.scale_x, height=100.0 * self.scale_y)
                
        self.prev_width = self.orig_width
        self.prev_height = self.orig_height

        
    
    def make_GUI(self):

        self.canvas.create_rectangle(0.0, 0.0, 235.0 * self.x, 1042.0, fill="#79BCF7", outline="")

        self.canvas.create_rectangle(255.0* self.scale_x, 20.0 * self.scale_y, 1435.0* self.scale_x, 1020.0* self.scale_y, fill="#DAEBF9", outline="")
        #self.canvas.scale("all", 0, 0, self.scale_x, self.scale_y)

        self.canvas.create_text(486.2366 * self.scale_x, 95.0247 * self.scale_y,
                           anchor="nw", text="Welcome to Course Scheduling System",
                           fill="#094478", font=("Roboto Black", int(30 * self.scale_y)))
        desc_text = (
            "                                             System Description:\n\n"
            "Make a compatible easy-to-use user interface within an application that allows\n"
            "the automated scheduling of university courses by the dean of a given department\n"
            "from imported data.\n\n"
            "User Instruction：\n"
            "1. Go to the `Upload` tab to upload the .csv files\n"
            "2. Click 'Confirm' to add files to the schedule generator\n"
            "3. 'View Files' allows you to manually add in extra information\n"
            "     not previously uploaded.\n"
            "4. Navigate between the tabs at the top of 'View Files' to add\n"
            "    specific information and click 'Add' to update system with new data\n"
            "    You can also delete data from the system by rightlicking on the data\n"
            "5. Select `Generate Schedule` from the sidebar and press 'Start' to\n"
            "    generate the schedule\n"
            "6. Review conflicts under 'Conflict Summary'\n"
            "7. In 'Export Schedule' select a filter\n"
            "8. Click 'Export' to export schedule as a .csv and .pdf\n"
            "    For additional help, hover over buttons and fields for tooltips!"
        )
        self.canvas.create_text(366.4585 * self.scale_x, 234.97 * self.scale_y,
                           anchor="nw", text=desc_text, fill="#094478",
                           font=("Roboto Regular", int(20 * self.scale_y)))


    def clear_gui(self):
        self.canvas.delete("all")

    def on_resize(self, event):
        if event.width < 300 or event.height < 300:
            return  # prevent errors on small resize

        scale_x = event.width / self.orig_width
        scale_y = event.height / self.orig_height

        if (event.width, event.height) != (self.prev_width, self.prev_height):
            self.scale_y = scale_y
            self.scale_x = scale_x
            self.prev_width = event.width
            self.prev_height = event.height
            self.clear_gui()
            self.make_GUI()


