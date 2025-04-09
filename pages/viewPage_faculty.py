import tkinter as tk
from tkinter import Canvas, Button, Entry, Label, ttk
from tkinter.filedialog import askopenfilename
from pathlib import Path
from PIL import Image, ImageTk
import os
import tkinter.ttk as ttk
#from tktooltip import ToolTip
from lib.CSV_Parser import parse_csv_2
from lib.DatabaseManager import DatabaseManager


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
# View Page: Frame 4
# ---------------------------
class ViewPageFaculty(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        OUTPUT_PATH = Path(__file__).parent
        ASSETS_PATH = OUTPUT_PATH / Path(r"assets/frame_view_faculty")

        def relative_to_assets(path: str) -> Path:
            return ASSETS_PATH / Path(path)
        
        orig_width, orig_height = 1455, 1041
        new_width, new_height = 800, 600
        scale_x, scale_y = new_width / orig_width, new_height / orig_height
        canvas = tk.Canvas(self, bg="#FFFFFF", height=orig_height, width=orig_width,
                           bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)
        canvas.create_rectangle(0.0, 1.0, 235.0* scale_x, 1042.0, fill="#79BCF7", outline="")


      
        # Navigation button: switch page
       # ----------------------------HomePage------------------------------------------
        btn5_img = scaled_photoimage(str(relative_to_assets("button_5.png")), scale_x, scale_y)
        btn5 = Button(self, image=btn5_img, borderwidth=0, highlightthickness=0,
                      command=lambda: controller.show_frame("HomePage"), relief="flat")
        btn5.image = btn5_img
        btn5.place(x=0.0 * scale_x, y=2 * scale_y, width=235.0 * scale_x, height=100.0 * scale_y)  
       # ----------------------------UploadPage------------------------------------------
        btn4_img = scaled_photoimage(str(relative_to_assets("button_4.png")), scale_x, scale_y)
        btn4 = Button(self, image=btn4_img, borderwidth=0, highlightthickness=0,
                      command=lambda: controller.show_frame("UploadPage"), relief="flat")
        btn4.image = btn4_img
        btn4.place(x=0.0 * scale_x, y=102.0 * scale_y, width=235.0 * scale_x, height=100.0 * scale_y)
        # ----------------------------viewPage------------------------------------------
        btn4_img = scaled_photoimage(str(relative_to_assets("button_2.png")), scale_x, scale_y)
        btn4 = Button(self, image=btn4_img, borderwidth=0, highlightthickness=0,
                      command=lambda: controller.show_frame("ViewPageOverall"), relief="flat")
        btn4.image = btn4_img
        btn4.place(x=0.0 * scale_x, y=202.0 * scale_y, width=235.0 * scale_x, height=100.0 * scale_y)     
       # ----------------------------StartPage------------------------------------------
        btn3_img = scaled_photoimage(str(relative_to_assets("button_3.png")), scale_x, scale_y)
        btn3 = Button(self, image=btn3_img, borderwidth=0, highlightthickness=0,
                      command=lambda: controller.show_frame("StartPage"), relief="flat")
        btn3.image = btn3_img
        btn3.place(x=0.0 * scale_x, y=302.0 * scale_y, width=235.0 * scale_x, height=100.0 * scale_y)
       # ----------------------------ExportPage------------------------------------------
        btnexport_img = scaled_photoimage(str(relative_to_assets("export_button.png")), scale_x, scale_y)
        btnexport = Button(self, image=btnexport_img, borderwidth=0, highlightthickness=0,
                      command=lambda: controller.show_frame("ExportPage"), relief="flat")
        btnexport.image = btnexport_img
        btnexport.place(x=0.0 * scale_x, y=402.0 * scale_y, width=235.0 * scale_x, height=100.0 * scale_y)
        # ----------------------------SettingPage------------------------------------------
        btn1_img = scaled_photoimage(str(relative_to_assets("button_1.png")), scale_x, scale_y)
        btn1 = Button(self, image=btn1_img, borderwidth=0, highlightthickness=0,
                      command=lambda: controller.show_frame("SettingPage"), relief="flat")
        btn1.image = btn1_img
        btn1.place(x=0.0 * scale_x, y=502.0 * scale_y, width=235.0 * scale_x, height=100.0 * scale_y)

        #logo iamge
        img1 = scaled_photoimage(str(relative_to_assets("image_1.png")), scale_x, scale_y)
        canvas.create_image(215.0 * scale_x, 1700.0 * scale_y, image=img1)
        canvas.image = img1

        canvas.create_rectangle(234.0* scale_x,1.0* scale_y,1455.0* scale_x, 97.0* scale_y,fill="#A3D1F9",outline="")


#———————————————————————————————————————————————————————
#                             T A B
#———————————————————————————————————————————————————————
       # ----------------------------overall------------------------------------------
        btn7_img = scaled_photoimage(str(relative_to_assets("button_7.png")), scale_x, scale_y)
        btn7 = Button(self, image=btn7_img, borderwidth=0, highlightthickness=0,
                      command=lambda: controller.show_frame("ViewPageOverall"), relief="flat")
        btn7.image = btn7_img
        btn7.place(x=258.0 * scale_x, y=15.0 * scale_y, width=150.0 * scale_x, height=64.0 * scale_y)
        

        # ----------------------------Courses------------------------------------------
        btn8_img = scaled_photoimage(str(relative_to_assets("button_8.png")), scale_x, scale_y)
        btn8 = Button(self, image=btn8_img, borderwidth=0, highlightthickness=0,
                      command=lambda: controller.show_frame("ViewPageCourse"), relief="flat")
        btn8.image = btn8_img
        btn8.place(x=459.0 * scale_x, y=15.0 * scale_y, width=150.0 * scale_x, height=64.0 * scale_y)
        
        # ----------------------------Faculty------------------------------------------
        btn9_img = scaled_photoimage(str(relative_to_assets("button_9.png")), scale_x, scale_y)
        btn9 = Button(self, image=btn9_img, borderwidth=0, highlightthickness=0,
                      command=lambda: controller.show_frame("ViewPageFaculty"), relief="flat")
        btn9.image = btn9_img
        btn9.place(x=660.0 * scale_x, y=15.0 * scale_y, width=150.0 * scale_x, height=64.0 * scale_y)
        # ----------------------------Perferences------------------------------------------
        btn10_img = scaled_photoimage(str(relative_to_assets("button_10.png")), scale_x, scale_y)
        btn10 = Button(self, image=btn10_img, borderwidth=0, highlightthickness=0,
                      command=lambda: controller.show_frame("ViewPagePreference"), relief="flat")
        btn10.image = btn10_img
        btn10.place(x=861.0 * scale_x, y=15.0 * scale_y, width=150.0 * scale_x, height=64.0 * scale_y)       
        # ----------------------------Rooms------------------------------------------
        btn11_img = scaled_photoimage(str(relative_to_assets("button_11.png")), scale_x, scale_y)
        btn11 = Button(self, image=btn11_img, borderwidth=0, highlightthickness=0,
                      command=lambda: controller.show_frame("ViewPageRooms"), relief="flat")
        btn11.image = btn11_img
        btn11.place(x=1062.0 * scale_x, y=15.0 * scale_y, width=150.0 * scale_x, height=64.0 * scale_y) 
        # ----------------------------Time------------------------------------------
        btn12_img = scaled_photoimage(str(relative_to_assets("button_12.png")), scale_x, scale_y)
        btn12 = Button(self, image=btn12_img, borderwidth=0, highlightthickness=0,
                      command=lambda: controller.show_frame("ViewPageTimes"), relief="flat")
        btn12.image = btn12_img
        btn12.place(x=1263.0 * scale_x, y=15.0 * scale_y, width=150.0 * scale_x, height=64.0 * scale_y) 


#———————————————————————————————————————————————————————
#                           TABLE
#———————————————————————————————————————————————————————

        self.columns4 = ("Faculty",)
        self.tree_Faculty = ttk.Treeview(self, columns=self.columns4, show="headings", height=1)
        self.tree_Faculty.heading("Faculty", text="Faculty")
        self.tree_Faculty.column("Faculty", width=int(350 * scale_x), anchor="center")
        self.tree_Faculty.insert("", "end", values=("Dr. Smith",))
        self.tree_Faculty.place(x=271.0 * scale_x, y=124.0 * scale_y,
                                width=1150.0 * scale_x, height=700.0 * scale_y)

        # self.Faculty_entry = Entry(
        #     self, bg="#DAEBFA", fg="#0A4578",
        #     font=("Arial", int(18)), relief="flat",
        #     insertbackground="#0A4578"
        # )
        # self.Faculty_entry.place(x=274.0 * scale_x, y=937.0 * scale_y,
        #                            width=850.0 * scale_x, height=80.0 * scale_y)

        def add_faculty():
            name = entry.get().strip()  # Name field
            priority = entry2.get().strip()  # Priority field
            class_id1 = entry3.get().strip()  # Class ID 1
            class_id2 = entry4.get().strip()  # Class ID 2 (optional)
            class_id3 = entry5.get().strip()  # Class ID 3 (optional)
            class_id4 = entry6.get().strip()  # Class ID 4 (optional)

            # Ensure required fields are filled
            if name and class_id1:
                try:
                    # Default priority to 0 if not provided
                    priority = int(priority) if priority else 0

                    # Collect all class IDs and filter out empty ones
                    class_ids = [class_id for class_id in [class_id1, class_id2, class_id3, class_id4] if class_id]

                    # Add faculty to the database
                    db = DatabaseManager()
                    db.start_session()
                    db.add_faculty_ui(name=name, priority=priority, class_ids=class_ids)
                    db.end_session()

                    # Add the faculty to the Treeview
                    self.tree_Faculty.insert("", "end", values=(name,))

                    # Clear the entry fields
                    entry.delete(0, "end")
                    entry2.delete(0, "end")
                    entry3.delete(0, "end")
                    entry4.delete(0, "end")
                    entry5.delete(0, "end")
                    entry6.delete(0, "end")
                except Exception as e:
                    print(f"Error adding faculty: {e}")
            else:
                print("Please fill in all required fields (Name and Class ID 1).")

        btn13_img = scaled_photoimage(str(relative_to_assets("button_13.png")), scale_x, scale_y)
        btn13 = Button(self, image=btn13_img, borderwidth=0, highlightthickness=0,
                       command=add_faculty)
        btn13.image = btn13_img
        btn13.place(x=1192.0 * scale_x, y=935.0 * scale_y, width=200.0 * scale_x, height=80.0 * scale_y)


#——————————————————————————————————————————————————
#          USER add PART
#——————————————————————————————————————————————————

        canvas.create_rectangle(258.0* scale_x,845.0 * scale_y,1431.0* scale_x, 1032.0 * scale_y, fill="#DAEBFA", outline="")
        #----------------------------------------------------------------------------------------------------------------
        canvas.create_text(  268.0* scale_x,  869.0 * scale_y, anchor="nw", text="Name :", fill="#094478", font=("Jomolhari Regular",9))
        entry = Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=0, font=("Arial", int(16 * scale_y)))
        entry.place(x=375.0 * scale_x, y=860.0 * scale_y, width=320 * scale_x, height=50 * scale_y)
        #----------------------------------------------------------------------------------------------------------------
        canvas.create_text( 830.0* scale_x,869.0 * scale_y, anchor="nw", text="Relative Priority (>= 0):", fill="#094478", font=("Jomolhari Regular",9))
        entry2 = Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=0, font=("Arial", int(16 * scale_y)))
        entry2.place(x=1062.0 * scale_x, y=860.0 * scale_y, width=320 * scale_x, height=50 * scale_y)
        #----------------------------------------------------------------------------------------------------------------
        canvas.create_text( 324.0* scale_x,936.0 * scale_y, anchor="nw", text="Class ID 1", fill="#094478", font=("Jomolhari Regular",9))
        entry3 = Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=0, font=("Arial", int(16 * scale_y)))
        entry3.place(x=280.0 * scale_x, y=968.0 * scale_y, width=190 * scale_x, height=50 * scale_y)
        #----------------------------------------------------------------------------------------------------------------
        canvas.create_text( 559.0* scale_x, 936.0 * scale_y, anchor="nw", text="Class ID 2", fill="#094478", font=("Jomolhari Regular", 9))
        entry4 = Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=0, font=("Arial", int(16 * scale_y)))
        entry4.place(x=515.0 * scale_x, y=968.0 * scale_y, width=190 * scale_x, height=50 * scale_y)
        #----------------------------------------------------------------------------------------------------------------
        canvas.create_text( 794.0* scale_x,936.0 * scale_y, anchor="nw", text="Class ID 3", fill="#094478", font=("Jomolhari Regular", 9))
        entry5 = Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=0, font=("Arial", int(16 * scale_y)))
        entry5.place(x=750.0 * scale_x, y=968.0 * scale_y, width=190 * scale_x, height=50 * scale_y)
        #----------------------------------------------------------------------------------------------------------------
        canvas.create_text( 1029.0* scale_x,936.0 * scale_y, anchor="nw", text="Class ID 4", fill="#094478", font=("Jomolhari Regular", 9))
        entry6 = Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=0, font=("Arial", int(16 * scale_y)))
        entry6.place(x=985.0 * scale_x, y=968.0 * scale_y, width=190 * scale_x, height=50 * scale_y)
        #----------------------------------------------------------------------------------------------------------------






    # -----------------------------
    # Add Faculty to DB + UI
    # -----------------------------
    def add_faculty(self):
        name = self.Faculty_entry.get().strip()
        if name:
            db = DatabaseManager()
            db.start_session()
            db.add_faculty(name=name, priority=0)
            db.end_session()
            self.tree_Faculty.insert("", "end", values=(name,))
            self.Faculty_entry.delete(0, "end")

    # -----------------------------
    # Load Faculty from Selected File
    # -----------------------------
    def load_faculty_from_file(self, file_path):
        try:
            faculty_list, _, _, _, _ = parse_csv_2(file_path, insert_into_db=False)
            self.tree_Faculty.delete(*self.tree_Faculty.get_children())
            for faculty in faculty_list:
                self.tree_Faculty.insert("", "end", values=(faculty.Name,))
        except Exception as e:
            print(f"Error loading faculty data: {e}")

    # -----------------------------
    # Raise and Reload Faculty Table
    # -----------------------------
    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        if hasattr(self.controller, "selected_file_path"):
            self.load_faculty_from_file(self.controller.selected_file_path)














