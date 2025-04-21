import tkinter as tk
from tkinter import Canvas, Button, Entry, Label, ttk
from tkinter.filedialog import askopenfilename
from pathlib import Path
from PIL import Image, ImageTk
import os
import tkinter.ttk as ttk
from tktooltip import ToolTip
from lib.CSV_Parser import parse_csv_2
from lib.DatabaseManager import DatabaseManager, Course
import tkinter.messagebox as mbox
import re

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

        self.columns4 = ("Name", "Priority", "Class1", "Class2", "Class3", "Class4", "Class5")
        self.tree_Faculty = ttk.Treeview(self, columns=self.columns4, show="headings", height=10)
        for col in self.columns4:
            self.tree_Faculty.heading(col, text=col, command=lambda _col=col: self.sort_treeview(_col, False))
            self.tree_Faculty.column(col, width=int(1150 * scale_x)//len(self.columns4), anchor="center")
        self.tree_Faculty.place(x=271.0 * scale_x, y=124.0 * scale_y, width=1150.0 * scale_x, height=700.0 * scale_y)
        
        self.tree_Faculty.bind("<Button-3>", self.show_context_menu)

        self.scrollbar_faculty = ttk.Scrollbar(self, orient="vertical", command=self.tree_Faculty.yview)
        self.tree_Faculty.configure(yscrollcommand=self.scrollbar_faculty.set)
        self.scrollbar_faculty.place(x=271.0 * scale_x + 1150.0 * scale_x, y=124.0 * scale_y, width=15, height=700.0 * scale_y)

        self.tree_Faculty.tag_configure("evenrow", background="#E6F2FF")
        self.tree_Faculty.tag_configure("oddrow", background="#FFFFFF")


        def add_faculty():
            name = entry.get().strip()
            priority_str = entry2.get().strip()
            class_id1 = entry3.get().strip()
            class_id2 = entry4.get().strip()
            class_id3 = entry5.get().strip()
            class_id4 = entry6.get().strip()

            # Check for empty Professor name and missing Class ID 1
            if not name:
                mbox.showerror("Missing Field", "Professor name cannot be empty.")
                return
            if not class_id1:
                mbox.showerror("Missing Field", "At least one class (Class ID 1) must be provided.")
                return

            db = DatabaseManager()
            db.start_session()
            # Check for duplicate professor name (case-insensitive)
            faculties = db.get_faculty()
            if any(fac.Name.lower() == name.lower() for fac in faculties):
                mbox.showerror("Duplicate Entry", "A professor with this name already exists in the database.")
                db.end_session()
                return

            # Convert and validate priority
            try:
                priority = int(priority_str) if priority_str else 0
            except ValueError:
                mbox.showerror("Invalid Value", "Please enter a valid value (number >= 0) for the priority.")
                db.end_session()
                return

            if priority < 0:
                mbox.showerror("Invalid Priority", "Priority must be a non-negative value (number >= 0).")
                db.end_session()
                return

            # Function to standardize class IDs (e.g., "abc123" -> "ABC 123")
            def standardize_class_id(cid):
                """
                Expects cid in the format 'CS 155-1' or 'CS 155-01' (with optional spaces around the dash).
                Returns the course ID in the format 'CS 155-01' (section padded to two digits).
                If the input does not match, returns None.
                """
                cid = cid.strip()

                print(f"Standardizing class ID: {cid}")
                match = re.match(r'([A-Za-z]+\s*\d+)-(\d+)$', cid)
                print(f"Match: {match}")

                if match:
                    base = match.group(1).strip()
                    section = match.group(2).strip()
                    if len(section) == 1:
                        section = section.zfill(2)
                    return f"{base}-{section}"
                else:
                    return None

            # Process each class input:
            class_id1 = standardize_class_id(entry3.get().strip())
            if class_id1 is None:
                mbox.showerror("Invalid Class ID", "Class ID 1 must be entered in the format 'CS 155-01'.")
                db.end_session()
                return

            # Process optional Class IDs similarly:
            class_id2_raw = entry4.get().strip()
            class_id2 = standardize_class_id(class_id2_raw) if class_id2_raw else None
            if class_id2_raw and class_id2 is None:
                mbox.showerror("Invalid Class ID", "Class ID 2 must be entered in the format 'CS 155-01'.")
                db.end_session()
                return

            class_id3_raw = entry5.get().strip()
            class_id3 = standardize_class_id(class_id3_raw) if class_id3_raw else None
            if class_id3_raw and class_id3 is None:
                mbox.showerror("Invalid Class ID", "Class ID 3 must be entered in the format 'CS 155-01'.")
                db.end_session()
                return

            class_id4_raw = entry6.get().strip()
            class_id4 = standardize_class_id(class_id4_raw) if class_id4_raw else None
            if class_id4_raw and class_id4 is None:
                mbox.showerror("Invalid Class ID", "Class ID 4 must be entered in the format 'CS 155-01'.")
                db.end_session()
                return

            # Then prepare the list for insertion:
            class_ids = [class_id1, class_id2, class_id3, class_id4]

            # For each non-None class, warn if the course doesn't exist in the database.
            for cid in [class_id1, class_id2, class_id3, class_id4]:
                if cid:
                    existing_course = db.session.query(Course).filter_by(CourseID=cid).first()
                    if not existing_course:
                        mbox.showwarning(
                            "Course Not Found",
                            f"Course '{cid}' does not exist. The professor won't be assigned to this course unless added on the Courses page."
                        )

            # Prepare class IDs list, filtering out None for optional ones if desired
            class_ids = [class_id1]
            for cid in [class_id2, class_id3, class_id4]:
                class_ids.append(cid)  # will be None if not provided

            try:
                db.add_faculty_ui(name=name, priority=priority, class_ids=class_ids)
                db.end_session()

                # Refresh the treeview
                self.update_treeview()

                # Clear the entry fields
                entry.delete(0, "end")
                entry2.delete(0, "end")
                entry3.delete(0, "end")
                entry4.delete(0, "end")
                entry5.delete(0, "end")
                entry6.delete(0, "end")
            except Exception as e:
                db.end_session()
                mbox.showerror("Error Adding Faculty", f"Error adding faculty: {e}")

        btn13_img = scaled_photoimage(str(relative_to_assets("button_13.png")), scale_x, scale_y)
        btn13 = Button(self, image=btn13_img, borderwidth=0, highlightthickness=0,
                       command=add_faculty)
        btn13.image = btn13_img
        btn13.place(x=1192.0 * scale_x, y=935.0 * scale_y, width=200.0 * scale_x, height=80.0 * scale_y)
        ToolTip(btn13, msg="Add new data to system", delay=0.5)


#——————————————————————————————————————————————————
#          USER add PART
#——————————————————————————————————————————————————

        canvas.create_rectangle(258.0* scale_x,845.0 * scale_y,1431.0* scale_x, 1032.0 * scale_y, fill="#DAEBFA", outline="")
        #----------------------------------------------------------------------------------------------------------------
        canvas.create_text(  268.0* scale_x,  869.0 * scale_y, anchor="nw", text="Name :", fill="#094478", font=("Jomolhari Regular",9))
        entry = Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=0, font=("Arial", int(16 * scale_y)))
        entry.place(x=375.0 * scale_x, y=860.0 * scale_y, width=320 * scale_x, height=50 * scale_y)
        ToolTip(entry, msg="Enter Professor Name \nExample: Dr. Hozier", delay=0.5)
        #----------------------------------------------------------------------------------------------------------------
        canvas.create_text( 830.0* scale_x,869.0 * scale_y, anchor="nw", text="Relative Priority (>= 0):", fill="#094478", font=("Jomolhari Regular",9))
        entry2 = Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=0, font=("Arial", int(16 * scale_y)))
        entry2.place(x=1062.0 * scale_x, y=860.0 * scale_y, width=320 * scale_x, height=50 * scale_y)
        ToolTip(entry2, msg="Enter Professor relative Priority \nExample: 1", delay=0.5)
        #----------------------------------------------------------------------------------------------------------------
        canvas.create_text( 324.0* scale_x,936.0 * scale_y, anchor="nw", text="Class ID 1", fill="#094478", font=("Jomolhari Regular",9))
        entry3 = Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=0, font=("Arial", int(16 * scale_y)))
        entry3.place(x=280.0 * scale_x, y=968.0 * scale_y, width=190 * scale_x, height=50 * scale_y)
        ToolTip(entry3, msg="Add file to system", delay=0.5)
        ToolTip(entry3, msg="Enter Assigned Class ID \nExample: CS 127", delay=0.5)
        #----------------------------------------------------------------------------------------------------------------
        canvas.create_text( 559.0* scale_x, 936.0 * scale_y, anchor="nw", text="Class ID 2", fill="#094478", font=("Jomolhari Regular", 9))
        entry4 = Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=0, font=("Arial", int(16 * scale_y)))
        entry4.place(x=515.0 * scale_x, y=968.0 * scale_y, width=190 * scale_x, height=50 * scale_y)
        ToolTip(entry4, msg="Add file to system", delay=0.5)
        ToolTip(entry4, msg="Enter Assigned Class ID \nExample: CS 232", delay=0.5)
        #----------------------------------------------------------------------------------------------------------------
        canvas.create_text( 794.0* scale_x,936.0 * scale_y, anchor="nw", text="Class ID 3", fill="#094478", font=("Jomolhari Regular", 9))
        entry5 = Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=0, font=("Arial", int(16 * scale_y)))
        entry5.place(x=750.0 * scale_x, y=968.0 * scale_y, width=190 * scale_x, height=50 * scale_y)
        ToolTip(entry5, msg="Add file to system", delay=0.5)
        ToolTip(entry5, msg="Enter Assigned Class ID \nExample: CS 101", delay=0.5)
        #----------------------------------------------------------------------------------------------------------------
        canvas.create_text( 1029.0* scale_x,936.0 * scale_y, anchor="nw", text="Class ID 4", fill="#094478", font=("Jomolhari Regular", 9))
        entry6 = Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=0, font=("Arial", int(16 * scale_y)))
        entry6.place(x=985.0 * scale_x, y=968.0 * scale_y, width=190 * scale_x, height=50 * scale_y)
        ToolTip(entry6, msg="Add file to system", delay=0.5)
        ToolTip(entry6, msg="Enter Assigned Class ID \nExample: CS 128", delay=0.5)
        #----------------------------------------------------------------------------------------------------------------


    def sort_treeview(self, col, reverse):
        # Get values and item ids from treeview
        l = [(self.tree_Faculty.set(k, col), k) for k in self.tree_Faculty.get_children('')]
        try:
            l.sort(key=lambda t: float(t[0]) if t[0].replace('.','',1).isdigit() else t[0], reverse=reverse)
        except Exception:
            l.sort(reverse=reverse)
        for index, (val, k) in enumerate(l):
            self.tree_Faculty.move(k, '', index)
        self.tree_Faculty.heading(col, command=lambda: self.sort_treeview(col, not reverse))



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


    def update_treeview(self):
        for item in self.tree_Faculty.get_children():
            self.tree_Faculty.delete(item)
        db = DatabaseManager()
        db.start_session()
        faculties = db.get_faculty()
        db.end_session()
        for i, fac in enumerate(faculties):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.tree_Faculty.insert("", "end", iid=fac.FacultyID, values=(
                fac.Name,
                fac.Priority,
                fac.Class1,
                fac.Class2,
                fac.Class3,
                fac.Class4,
                fac.Class5
            ), tags=(tag,))
    
    def show_context_menu(self, event):
        item = self.tree_Faculty.identify_row(event.y)
        if item:
            menu = tk.Menu(self, tearoff=0)
            menu.add_command(label="Delete", command=lambda: self.delete_item(item))
            menu.post(event.x_root, event.y_root)
    
    def delete_item(self, item):
        vals = self.tree_Faculty.item(item, 'values')  # (Name, Priority, Class1, Class2, Class3, Class4, Class5)
        if not vals or len(vals) < 7:
            print("Cannot determine faculty details.")
            return
        name, priority, cl1, cl2, cl3, cl4, cl5 = vals
        try:
            db = DatabaseManager()
            db.start_session()
            print(f"Deleting faculty: {name}, Priority: {priority}, Classes: {cl1}, {cl2}, {cl3}, {cl4}, {cl5}")
            db.delete_faculty_by_values(name, priority, cl1, cl2, cl3, cl4, cl5)
            db.end_session()
            self.update_treeview()
        except Exception as e:
            print(f"Error deleting faculty: {e}")

    # -----------------------------
    # Raise and Reload Faculty Table
    # -----------------------------
    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.update_treeview()











