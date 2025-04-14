import tkinter as tk
from tkinter import Canvas, Button, Entry, Label, ttk
from tkinter.filedialog import askopenfilename
from pathlib import Path
from PIL import Image, ImageTk
import os
import tkinter.ttk as ttk
from lib.CSV_Parser import parse_csv_2
from lib.DatabaseManager import DatabaseManager, Classroom, Course
import re
import tkinter.messagebox as mbox
from tktooltip import ToolTip

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
class ViewPageCourse(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        OUTPUT_PATH = Path(__file__).parent
        ASSETS_PATH = OUTPUT_PATH / Path(r"assets/frame_view_course")

        def relative_to_assets(path: str) -> Path:
            return ASSETS_PATH / Path(path)
        
        orig_width, orig_height = 1455, 1041
        new_width, new_height = 800, 600
        scale_x, scale_y = new_width / orig_width, new_height / orig_height
        canvas = tk.Canvas(self, bg="#FFFFFF", height=orig_height, width=orig_width,
                           bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)
        canvas.create_rectangle(0.0, 1.0, 235.0* scale_x, 1042.0, fill="#79BCF7", outline="")


        
    # def load_courses_from_file_if_applicable(self):
    #     if hasattr(self.controller, "selected_file_path"):
    #         self.load_courses_from_file(self.controller.selected_file_path)
        
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
        self.columns = ("Course ID", "Department", "Max Enroll", "Room1", "Room2", "Room3", "Room4", "Room5")
        self.tree_Course = ttk.Treeview(self, columns=self.columns, show="headings", height=10)
        for col in self.columns:
            self.tree_Course.heading(col, text=col, command=lambda _col=col: self.sort_treeview(_col, False))
            self.tree_Course.column(col, width=int(1150 * scale_x)//len(self.columns), anchor="center")
        self.tree_Course.place(x=271.0 * scale_x, y=124.0 * scale_y, width=1150.0 * scale_x, height=700.0 * scale_y)
        
        self.scrollbar_course = ttk.Scrollbar(self, orient="vertical", command=self.tree_Course.yview)
        self.tree_Course.configure(yscrollcommand=self.scrollbar_course.set)
        self.scrollbar_course.place(x=271.0 * scale_x + 1150.0 * scale_x, y=124.0 * scale_y, width=15, height=700.0 * scale_y)

        self.tree_Course.bind("<Button-3>", self.show_context_menu)

        self.tree_Course.tag_configure("evenrow", background="#E6F2FF")
        self.tree_Course.tag_configure("oddrow", background="#FFFFFF")

        # self.course_id_entry = Entry(
        #     self, bg="#DAEBFA", fg="#0A4578", 
        #     font=("Arial", int(18)), relief="flat",
        #     insertbackground="#0A4578"
        # )
        # self.course_id_entry.place(x=274.0 * scale_x, y=937.0 * scale_y, width=850.0 * scale_x, height=80.0 * scale_y)
        def add_course():
            course_id = entry.get().strip()
            # Standardize course_id: Ensure the department part is uppercase and there's a space before the number
            match = re.match(r'([A-Za-z]+)\s*(\d+)', course_id)
            if match:
                dept = match.group(1).upper()
                number = match.group(2)
                course_id = f"{dept} {number}"
            # Retrieve remaining values
            department = entry2.get().strip()
            max_enrollment = entry3.get().strip()
            required_room1 = entry4.get().strip()
            required_room2 = entry5.get().strip()
            required_room3 = entry6.get().strip()
            required_room4 = entry7.get().strip()
            
            # Standardize required room inputs to uppercase
            if required_room1:
                required_room1 = required_room1.upper()
            if required_room2:
                required_room2 = required_room2.upper()
            if required_room3:
                required_room3 = required_room3.upper()
            if required_room4:
                required_room4 = required_room4.upper()
            
            # -- Error checking for required fields -- 
            if not course_id or not department or not max_enrollment:
                mbox.showerror("Missing Required Field", "Please fill in Course ID, Department, and Max/Estimated Enrollment.")
                return
            
            try:
                max_enrollment_int = int(max_enrollment)
                if max_enrollment_int <= 0:
                    mbox.showerror("Invalid Enrollment", "Max/Estimated Enrollment must be a positive integer greater than zero.")
                    return
            except ValueError:
                mbox.showerror("Invalid Enrollment", "Max/Estimated Enrollment must be a valid integer.")
                return

            # Create a DatabaseManager session for checking room existence
            db = DatabaseManager()
            db.start_session()
            
            # -- Check warnings for room IDs (if provided) --
            def check_room(room_str):
                if room_str:
                    existing_room = db.session.query(Classroom).filter_by(RoomID=room_str).first()
                    if not existing_room:
                        mbox.showwarning("Room Not Found", f"Room '{room_str}' does not exist in the database. It will not be assigned to the course unless added on the Rooms tab.")
                    return room_str
                return None

            

            required_room1 = check_room(required_room1)
            required_room2 = check_room(required_room2)
            required_room3 = check_room(required_room3)
            required_room4 = check_room(required_room4)
            
            # Check if the course already exists in the database


            try:
                existing_course = db.session.query(Course).filter_by(CourseID=course_id).first()
                if existing_course:
                    mbox.showerror("Course Exists", f"Course '{course_id}' already exists in the database.")
                    db.end_session()
                    return
                # Add the course to the database
                db.add_course(
                    course_id=course_id,
                    department=department,
                    max_enrollment=max_enrollment_int,
                    req_room1=required_room1,
                    req_room2=required_room2,
                    req_room3=required_room3,
                    req_room4=required_room4
                )
                db.end_session()
                # Refresh the Course treeview after DB insertion
                self.update_treeview()
                # Clear the entry fields
                entry.delete(0, "end")
                entry2.delete(0, "end")
                entry3.delete(0, "end")
                entry4.delete(0, "end")
                entry5.delete(0, "end")
                entry6.delete(0, "end")
                entry7.delete(0, "end")
            except Exception as e:
                db.end_session()
                mbox.showerror("Error Adding Course", f"Error adding course: {e}")
        # add
        btn13_img = scaled_photoimage(str(relative_to_assets("button_13.png")), scale_x, scale_y)
        btn13 = Button(self, image=btn13_img, borderwidth=0, highlightthickness=0, command=add_course)
        btn13.image = btn13_img
        btn13.place(x=1192.0 * scale_x, y=935.0 * scale_y, width=200.0 * scale_x, height=80.0 * scale_y)
        ToolTip(btn13, msg="Add new data to system", delay=1.0)
        

#——————————————————————————————————————————————————
#          USER add PART
#——————————————————————————————————————————————————

        canvas.create_rectangle(258.0* scale_x,845.0 * scale_y,1431.0* scale_x, 1032.0 * scale_y, fill="#DAEBFA", outline="")
        #----------------------------------------------------------------------------------------------------------------
        canvas.create_text(  268.0* scale_x,  869.0 * scale_y, anchor="nw", text="Course ID:", fill="#094478", font=("Jomolhari Regular",9))
        entry = Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=0, font=("Arial", int(16 * scale_y)))
        entry.place(x=375.0 * scale_x, y=860.0 * scale_y, width=(575.0 - 375.0) * scale_x, height=(910.0 - 860.0) * scale_y)
        #----------------------------------------------------------------------------------------------------------------
        canvas.create_text( 604.0* scale_x,869.0 * scale_y, anchor="nw", text="Department", fill="#094478", font=("Jomolhari Regular",9))
        entry2 = Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=0, font=("Arial", int(16 * scale_y)))
        entry2.place(x=743.0 * scale_x, y=860.0 * scale_y, width=(943.0 - 743.0) * scale_x, height=(910.0 - 860.0) * scale_y)
        #----------------------------------------------------------------------------------------------------------------
        canvas.create_text( 970.0* scale_x,869.0 * scale_y, anchor="nw", text="Max/Estimated Enrollment:", fill="#094478", font=("Jomolhari Regular",9))
        entry3 = Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=0, font=("Arial", int(16 * scale_y)))
        entry3.place(x=1240.0 * scale_x, y=860.0 * scale_y, width=(1413.0 - 1240.0) * scale_x, height=(910.0 - 860.0) * scale_y)
        #----------------------------------------------------------------------------------------------------------------
        canvas.create_text( 307.0* scale_x, 929.0 * scale_y, anchor="nw", text="Required room 1", fill="#094478", font=("Jomolhari Regular", 9))
        entry4 = Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=0, font=("Arial", int(16 * scale_y)))
        entry4.place(x=285.0 * scale_x, y=968.0 * scale_y, width=(475.0 - 285.0) * scale_x, height=(1018.0 - 968.0) * scale_y)
        #----------------------------------------------------------------------------------------------------------------
        canvas.create_text( 522.0* scale_x,929.0 * scale_y, anchor="nw", text="Required room 2", fill="#094478", font=("Jomolhari Regular", 9))
        entry5 = Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=0, font=("Arial", int(16 * scale_y)))
        entry5.place(x=500.0 * scale_x, y=968.0 * scale_y, width=(690.0 - 500.0) * scale_x, height=(1018.0 - 968.0) * scale_y)
        #----------------------------------------------------------------------------------------------------------------
        canvas.create_text( 738.0* scale_x,929.0 * scale_y, anchor="nw", text="Required room 3", fill="#094478", font=("Jomolhari Regular", 9))
        entry6 = Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=0, font=("Arial", int(16 * scale_y)))
        entry6.place(x=716.0 * scale_x, y=968.0 * scale_y, width=(906.0 - 716.0) * scale_x, height=(1018.0 - 968.0) * scale_y)
        #----------------------------------------------------------------------------------------------------------------
        canvas.create_text( 965.0* scale_x,929.0 * scale_y, anchor="nw", text="Required room 4", fill="#094478", font=("Jomolhari Regular", 9))
        entry7 = Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=0, font=("Arial", int(16 * scale_y)))
        entry7.place(x=943.0 * scale_x, y=968.0 * scale_y, width=(1133.0 - 943.0) * scale_x, height=(1018.0 - 968.0) * scale_y)


    def sort_treeview(self, col, reverse):
        # Get values and item ids from treeview
        l = [(self.tree_Course.set(k, col), k) for k in self.tree_Course.get_children('')]
        try:
            l.sort(key=lambda t: float(t[0]) if t[0].replace('.','',1).isdigit() else t[0], reverse=reverse)
        except Exception:
            l.sort(reverse=reverse)
        for index, (val, k) in enumerate(l):
            self.tree_Course.move(k, '', index)
        self.tree_Course.heading(col, command=lambda: self.sort_treeview(col, not reverse))
                
    def update_treeview(self):
        for item in self.tree_Course.get_children():
            self.tree_Course.delete(item)
        db = DatabaseManager()
        db.start_session()
        courses = db.get_course()
        db.end_session()
        for i, course in enumerate(courses):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.tree_Course.insert("", "end", iid=course.CourseID, values=(
                course.CourseID,
                course.Department,
                course.MaxEnrollment,
                course.ReqRoom1,
                course.ReqRoom2,
                course.ReqRoom3,
                course.ReqRoom4,
                course.ReqRoom5
            ), tags=(tag,))
    
    def show_context_menu(self, event):
        item = self.tree_Course.identify_row(event.y)
        if item:
            menu = tk.Menu(self, tearoff=0)
            menu.add_command(label="Delete", command=lambda: self.delete_item(item))
            menu.post(event.x_root, event.y_root)
    
    def delete_item(self, course_id):
        try:
            db = DatabaseManager()
            db.start_session()
            db.delete_course(course_id)  # Implement delete_course in DatabaseManager
            db.end_session()
            self.update_treeview()
        except Exception as e:
            print(f"Error deleting course: {e}")

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.update_treeview()

# def add_placeholder(entry, placeholder):
#     entry.insert(0, placeholder)
#     entry.config(fg='grey')
#     def on_focus_in(event):
#         if entry.get() == placeholder:
#             entry.delete(0, 'end')
#             entry.config(fg='black')
#     def on_focus_out(event):
#         if not entry.get():
#             entry.insert(0, placeholder)
#             entry.config(fg='grey')
#     entry.bind("<FocusIn>", on_focus_in)
#     entry.bind("<FocusOut>", on_focus_out)

















