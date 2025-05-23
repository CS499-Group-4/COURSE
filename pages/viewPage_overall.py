﻿import tkinter as tk
from tkinter import Canvas, Button, Entry, Label, ttk
from tkinter.filedialog import askopenfilename
from pathlib import Path
from PIL import Image, ImageTk
import os
import tkinter.ttk as ttk
import shutil
from lib.DatabaseManager import DatabaseManager
from lib.CSV_Parser import parse_csv_2
from tktooltip import ToolTip
from tkinter import messagebox

# ---------------------------
# Common helper functions and resource paths
# ---------------------------
OUTPUT_PATH = Path(__file__).parent
# Other pages can be adjusted as needed
ASSETS_PATH = OUTPUT_PATH / Path(r"assets/framehome")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

UPLOAD_DIR = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)



def scaled_photoimage(image_path: str, scale_x: float, scale_y: float) -> ImageTk.PhotoImage:
    img = Image.open(image_path)
    orig_width, orig_height = img.size
    new_size = (int(orig_width * scale_x), int(orig_height * scale_y))
    img = img.resize(new_size, resample=Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(img)

# ---------------------------
# View Page: Frame 4
# ---------------------------
class ViewPageOverall(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        OUTPUT_PATH = Path(__file__).parent
        ASSETS_PATH = OUTPUT_PATH / Path(r"assets/frame_view_overall")

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
       #  #file drop down
       # # Dropdown for uploaded files
       #  self.course_dropdown = ttk.Combobox(self, state="readonly")
       #  self.course_dropdown.set("Select File")
       #  self.course_dropdown.place(x=300.0 * scale_x, y=134.0 * scale_y, width=200.0 * scale_x, height=100.0 * scale_y)
       #  self.course_dropdown.bind("<<ComboboxSelected>>", self.on_file_selected)
        # Treeview Style
        style = ttk.Style()
        style.configure("Custom.Treeview", background="#E6F2FF", foreground="#000000",  rowheight=28,  fieldbackground="#E6F2FF" )
        style.configure("Custom.Treeview.Heading", background="#B3D9FF", foreground="#003366",  font=("Arial", 11, "bold"))
        style.map("Custom.Treeview", background=[("selected", "#0A4578")] )


        # Treeview widgets
        self.tree_Course = ttk.Treeview(self, columns=("Course ID",), show="headings", style="Custom.Treeview")
        self.tree_Course.heading("Course ID", text="Course ID")
        self.tree_Course.column("Course ID", anchor="center")
        self.tree_Course.place(x=465.0 * scale_x, y=134.0 * scale_y, width=350.0 * scale_x, height=380.0 * scale_y)

        self.scrollbar_course = ttk.Scrollbar(self, orient="vertical", command=self.tree_Course.yview)
        self.tree_Course.configure(yscrollcommand=self.scrollbar_course.set)
        self.scrollbar_course.place(x=(465.0 + 350.0) * scale_x, y=134.0 * scale_y, width=15, height=380.0 * scale_y)

        self.tree_Faculty = ttk.Treeview(self, columns=("Faculty",), show="headings", style="Custom.Treeview")
        self.tree_Faculty.heading("Faculty", text="Faculty")
        self.tree_Faculty.column("Faculty", anchor="center")
        self.tree_Faculty.place(x=880.0 * scale_x, y=134.0 * scale_y, width=350.0 * scale_x, height=380.0 * scale_y)

        self.scrollbar_faculty = ttk.Scrollbar(self, orient="vertical", command=self.tree_Faculty.yview)
        self.tree_Faculty.configure(yscrollcommand=self.scrollbar_faculty.set)
        self.scrollbar_faculty.place(x=(880.0 + 350.0) * scale_x, y=134.0 * scale_y, width=15, height=380.0 * scale_y)

        self.tree_Perferences = ttk.Treeview(self, columns=("PreferenceSummary",), show="headings", style="Custom.Treeview"  )
        self.tree_Perferences.heading("PreferenceSummary", text="Preferences Summary")
        self.tree_Perferences.column("PreferenceSummary", anchor="center")
        self.tree_Perferences.place(x=258.0 * scale_x, y=596.0 * scale_y, width=350.0 * scale_x, height=380.0 * scale_y)

        self.scrollbar_preferences = ttk.Scrollbar(self, orient="vertical", command=self.tree_Perferences.yview)
        self.tree_Perferences.configure(yscrollcommand=self.scrollbar_preferences.set)
        self.scrollbar_preferences.place(x=(258.0 + 350.0) * scale_x, y=596.0 * scale_y, width=15, height=380.0 * scale_y)

        self.tree_Rooms = ttk.Treeview(self, columns=("Rooms",), show="headings", style="Custom.Treeview")
        self.tree_Rooms.heading("Rooms", text="Rooms")
        self.tree_Rooms.column("Rooms", anchor="center")
        self.tree_Rooms.place(x=673.0 * scale_x, y=596.0 * scale_y, width=350.0 * scale_x, height=380.0 * scale_y)

        self.scrollbar_rooms = ttk.Scrollbar(self, orient="vertical", command=self.tree_Rooms.yview)
        self.tree_Rooms.configure(yscrollcommand=self.scrollbar_rooms.set)
        self.scrollbar_rooms.place(x=(673.0 + 350.0) * scale_x, y=596.0 * scale_y, width=15, height=380.0 * scale_y)

        self.tree_Time = ttk.Treeview(self, columns=("Time",), show="headings", style="Custom.Treeview")
        self.tree_Time.heading("Time", text="Time")
        self.tree_Time.column("Time", anchor="center")
        self.tree_Time.place(x=1088.0 * scale_x, y=596.0 * scale_y, width=350.0 * scale_x, height=380.0 * scale_y)

        self.scrollbar_time = ttk.Scrollbar(self, orient="vertical", command=self.tree_Time.yview)
        self.tree_Time.configure(yscrollcommand=self.scrollbar_time.set)
        self.scrollbar_time.place(x=(1088.0 + 350.0) * scale_x, y=596.0 * scale_y, width=15, height=380.0 * scale_y)


        for tree in [self.tree_Course, self.tree_Faculty, self.tree_Perferences, self.tree_Rooms, self.tree_Time]:
            tree.tag_configure("evenrow", background="#E6F2FF")
            tree.tag_configure("oddrow", background="#FFFFFF")

        self.populate_treeviews()  
        
    def populate_treeviews(self):
        db = DatabaseManager()
        db.start_session()

        for tree in [self.tree_Course, self.tree_Faculty, self.tree_Perferences, self.tree_Rooms, self.tree_Time]:
            tree.delete(*tree.get_children())

        # Course
        try:
            courses = db.get_course()
            for i, c in enumerate(courses):
                tag = "evenrow" if i % 2 == 0 else "oddrow"
                self.tree_Course.insert("", "end", values=(c.CourseID,), tags=(tag,))

        except Exception as e:
            print(f"[Course Error] {e}")

        # Faculty
        try:
            faculty_list = db.get_faculty()
            for i, f in enumerate(faculty_list):
                tag = "evenrow" if i % 2 == 0 else "oddrow"
                self.tree_Faculty.insert("", "end", values=(f.Name,), tags=(tag,))
        except Exception as e:
            print(f"[Faculty Error] {e}")

        # Preferences
        try:
            preferences = db.get_preferences()
            for i, pref in enumerate(preferences):
                summary = f"{pref.ProfessorName} | {pref.PreferenceType} | {pref.PreferenceValue}"
                tag = "evenrow" if i % 2 == 0 else "oddrow"
                self.tree_Perferences.insert("", "end", values=(summary,), tags=(tag,))
        except Exception as e:
            print(f"[Preference Error] {e}")


        # Rooms
        try:
                rooms = db.get_classrooms()
                for i, r in enumerate(rooms):
                    tag = "evenrow" if i % 2 == 0 else "oddrow"
                    self.tree_Rooms.insert("", "end", values=(r.RoomID,), tags=(tag,))
        except Exception as e:
            print(f"[Rooms Error] {e}")

        # Timeslot
        try:
            timeslots = db.get_timeslot()
            for i, t in enumerate(timeslots):
                time_str = f"{t.Days} {t.StartTime}"
                tag = "evenrow" if i % 2 == 0 else "oddrow"
                self.tree_Time.insert("", "end", values=(time_str,), tags=(tag,))
        except Exception as e:
            print(f"[Time Error] {e}")

        db.end_session()

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.populate_treeviews()

        # self.refresh_file_dropdown()

    # def refresh_file_dropdown(self):
    #     if not os.path.exists(UPLOAD_DIR):
    #         os.makedirs(UPLOAD_DIR)
    #     files = [f for f in os.listdir(UPLOAD_DIR) if f.endswith(".csv")]
    #     self.course_dropdown['values'] = files
    #     if files:
    #         self.course_dropdown.set(files[-1])

    # def on_file_selected(self, event):
    #     selected_file = self.course_dropdown.get()
    #     file_path = os.path.join(UPLOAD_DIR, selected_file)
    #     try:
    #         faculty_list, classroom_data, course_data, timeslot_data, preference_data = parse_csv_2(file_path)

    #         self.controller.selected_file_path = file_path  
            
    #         self.tree_Course.delete(*self.tree_Course.get_children())
    #         for course in course_data:
    #             self.tree_Course.insert("", "end", values=(course['course_id'],))

    #         self.tree_Faculty.delete(*self.tree_Faculty.get_children())
    #         for faculty in faculty_list:
    #             self.tree_Faculty.insert("", "end", values=(faculty.Name,))

    #         self.tree_Perferences.delete(*self.tree_Perferences.get_children())
    #         for pref in preference_data:
    #             self.tree_Perferences.insert("", "end", values=(pref,))

    #         self.tree_Rooms.delete(*self.tree_Rooms.get_children())
    #         for room in classroom_data:
    #             self.tree_Rooms.insert("", "end", values=(room['room_id'],))

    #         self.tree_Time.delete(*self.tree_Time.get_children())
    #         for timeslot in timeslot_data:
    #             self.tree_Time.insert("", "end", values=(f"{timeslot['day']} {timeslot['start_time']}-{timeslot['end_time']}",))

    #     except Exception as e:
    #         messagebox.showerror("Loading failed", f"Unable to load file content: {e}")











