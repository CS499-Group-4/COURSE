import tkinter as tk
from tkinter import Canvas, Button, Entry, Label, ttk
from tkinter.filedialog import askopenfilename
from pathlib import Path
from PIL import Image, ImageTk
import os
import tkinter.ttk as ttk
from tkinter import messagebox  # Import the messagebox module
from tktooltip import ToolTip
from lib.DatabaseManager import Schedule, Faculty, Course, Classroom, TimeSlot

#import the generate_scheduler() function from lib/scheduler.py
from lib.Scheduler import CourseScheduler
import threading 

# Instantiate the scheduler
scheduler = CourseScheduler()

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

tree = None

def update_treeview():
    global tree

    tree.delete(*tree.get_children())
    for entry in scheduler.return_schedule():  # Use the scheduler instance
        tree.insert("", "end", values=entry)




def update_conflict_treeview():
    """Populates the conflict tree view with detected conflicts."""
    global conflict_tree

    # Clear existing entries in the conflict tree view
    conflict_tree.delete(*conflict_tree.get_children())

    # Retrieve conflicts from the scheduler
    conflicts = scheduler.validate_faculty_preferences()

    # Populate the conflict tree view
    for conflict in conflicts:
        conflict_type = conflict.get("type", "Unknown")
        course = conflict.get("course", "N/A")
        professor = conflict.get("professor", "N/A")  # Get the professor's name

        # Insert the conflict into the tree view
        conflict_tree.insert("", "end", values=(professor, conflict_type, course))


def make_treeview_editable():
    def on_double_click(event):
        # Get the selected item and column
        region = tree.identify("region", event.x, event.y)
        if region != "cell":
            return  # Only allow editing cells
        row_id = tree.identify_row(event.y)
        column_id = tree.identify_column(event.x)

        # Get the current value of the cell
        item = tree.item(row_id)
        column_index = int(column_id[1:]) - 1  # Convert column ID (e.g., "#1") to index
        current_value = item["values"][column_index]

        # Get the column name
        column_name = tree["columns"][column_index]

        # Create a Combobox for editing
        combobox = ttk.Combobox(tree, state="readonly")
        combobox.place(x=event.x, y=event.y, width=tree.column(column_name, "width"))

        # Ensure the Combobox is on top of other elements
        combobox.lift()

        # Populate the Combobox with options dynamically based on the column
        if column_name == "Course ID":
            column_values = [course.CourseID for course in scheduler.db.get_course()]
        elif column_name == "Day":
            # Use a set to remove duplicate days
            column_values = sorted({timeslot.Days for timeslot in scheduler.db.get_timeslot()})
        elif column_name == "Time":
            # Use a set to remove duplicate start times
            column_values = sorted({timeslot.StartTime for timeslot in scheduler.db.get_timeslot()})
        elif column_name == "Professor":
            column_values = [faculty.Name for faculty in scheduler.db.get_faculty()]
        elif column_name == "Room":
            column_values = [classroom.RoomID for classroom in scheduler.db.get_classrooms()]
        else:
            column_values = []  # Default to an empty list if the column is not recognized

        combobox["values"] = sorted(column_values)

        # Set the current value in the Combobox
        combobox.set(current_value)

        # Handle selection
        def on_select(event):
            new_value = combobox.get()
            tree.set(row_id, column_name, new_value)  # Update the Treeview

            # Compare the new value with the database value
            schedule_entry = scheduler.db.session.query(Schedule).filter(Schedule.Course == item["values"][0]).first()
            if schedule_entry:
                db_value = None
                if column_name == "Day":
                    timeslot = scheduler.db.session.query(TimeSlot).filter(TimeSlot.SlotID == schedule_entry.TimeSlot).first()
                    db_value = timeslot.Days if timeslot else None
                elif column_name == "Time":
                    timeslot = scheduler.db.session.query(TimeSlot).filter(TimeSlot.SlotID == schedule_entry.TimeSlot).first()
                    db_value = timeslot.StartTime if timeslot else None
                elif column_name == "Professor":
                    professor = scheduler.db.session.query(Faculty).filter(Faculty.FacultyID == schedule_entry.Professor).first()
                    db_value = professor.Name if professor else None
                elif column_name == "Room":
                    db_value = schedule_entry.Classroom

                # Highlight the row if the new value differs from the database value
                if new_value != db_value:
                    tree.item(row_id, tags=("edited",))
                else:
                    tree.item(row_id, tags=())  # Remove the tag if the value matches the database

            combobox.destroy()  # Remove the Combobox

        combobox.bind("<<ComboboxSelected>>", on_select)

        # Close the Combobox when clicking outside of it
        def close_combobox(event):
            # Check if the click is outside the Combobox
            if combobox.winfo_exists():
                widget_under_cursor = combobox.winfo_containing(event.x_root, event.y_root)
                if widget_under_cursor is None or widget_under_cursor != combobox:
                    # Set the current value of the Combobox to the Treeview
                    new_value = combobox.get()
                    tree.set(row_id, column_name, new_value)
                    combobox.destroy()

        # Bind the click event to the root window
        tree.winfo_toplevel().bind("<Button-1>", close_combobox, add="+")

        # Unbind the click event when the Combobox is destroyed
        # def on_destroy(event):
        #     tree.winfo_toplevel().unbind("<Button-1>", close_combobox)

        # combobox.bind("<Destroy>", on_destroy)

    # Bind the double-click event to the Treeview
    tree.bind("<Double-1>", on_double_click)

    tree.tag_configure("edited", background="yellow")


def update_database_from_treeview():
    print("[INFO] Updating database with Treeview data...")
    has_updates = False  # Track if any updates are made

    for row in tree.get_children():
        # Check if the row has the "edited" tag
        if "edited" not in tree.item(row, "tags"):
            continue  # Skip rows that haven't been edited

        # Get the values from the Treeview row
        row_values = tree.item(row, "values")
        course_id, day, time, professor, room = row_values

        print(f"[INFO] Processing edited row: Course ID: {course_id}, Day: {day}, Time: {time}, Professor: {professor}, Room: {room}")

        # Retrieve the current schedule entry
        schedule_entry = scheduler.db.session.query(Schedule).filter(Schedule.Course == course_id).first()
        if not schedule_entry:
            warning_message = f"No matching Schedule entry found for Course ID: {course_id}."
            print(f"[WARN] {warning_message}")
            messagebox.showwarning("Update Warning", warning_message)
            continue

        # Perform conflict checks before making any updates
        # Check for TimeSlot conflicts
        timeslot = scheduler.db.session.query(TimeSlot).filter(
            TimeSlot.Days == day, TimeSlot.StartTime == time
        ).first()
        if not timeslot:
            print(f"[WARN] No matching TimeSlot found for Day: {day}, Time: {time}.")
            continue

        # Check for Professor conflicts
        professor_entry = scheduler.db.session.query(Faculty).filter(Faculty.Name == professor).first()
        if professor_entry:
            conflicting_schedule = scheduler.db.session.query(Schedule).join(TimeSlot).filter(
                Schedule.Professor == professor_entry.FacultyID,
                TimeSlot.StartTime == time,
                Schedule.SchedID != schedule_entry.SchedID  # Exclude the current entry
            ).all()  # Retrieve all potential conflicts

            for conflict in conflicting_schedule:
                conflict_timeslot = scheduler.db.session.query(TimeSlot).filter(TimeSlot.SlotID == conflict.TimeSlot).first()
                if conflict_timeslot:
                    # Check for overlapping days
                    current_days = set(day for day in day)  # Convert current days to a set
                    conflict_days = set(day for day in conflict_timeslot.Days)  # Convert conflict days to a set
                    if current_days & conflict_days:  # Check for intersection
                        error_message = (
                            f"Conflict detected: Professor {professor} is already assigned to "
                            f"Course ID {conflict.Course} at overlapping days {current_days & conflict_days} "
                            f"and Time: {time}. Update aborted."
                        )
                        print(f"[ERROR] {error_message}")
                        messagebox.showerror("Update Error", error_message)
                        continue
        else:
            warning_message = f"No matching Professor found for Name: {professor}."
            print(f"[WARN] {warning_message}")
            messagebox.showwarning("Update Warning", warning_message)
            continue

        # Check for Room conflicts and capacity
        room_entry = scheduler.db.session.query(Classroom).filter(Classroom.RoomID == room).first()
        if room_entry:
            course_entry = scheduler.db.session.query(Course).filter(Course.CourseID == course_id).first()
            if course_entry and course_entry.MaxEnrollment > room_entry.Capacity:
                error_message = (
                    f"Room capacity exceeded: Room {room} has a maximum capacity of {room_entry.Capacity}, "
                    f"but Course {course_id} requires {course_entry.MaxEnrollment}. Update aborted."
                )
                print(f"[ERROR] {error_message}")
                messagebox.showerror("Update Error", error_message)
                continue

            conflicting_schedule = scheduler.db.session.query(Schedule).join(TimeSlot).filter(
                Schedule.Classroom == room_entry.RoomID,
                TimeSlot.Days == day,
                TimeSlot.StartTime == time,
                Schedule.SchedID != schedule_entry.SchedID  # Exclude the current entry
            ).first()

            if conflicting_schedule:
                error_message = (
                    f"Conflict detected: Room {room} is already assigned to "
                    f"Course ID {conflicting_schedule.Course} at Day: {day}, Time: {time}. "
                    f"Update aborted."
                )
                print(f"[ERROR] {error_message}")
                messagebox.showerror("Update Error", error_message)
                continue
        else:
            warning_message = f"No matching Room found for RoomID: {room}."
            print(f"[WARN] {warning_message}")
            messagebox.showwarning("Update Warning", warning_message)
            continue

        # If no conflicts are detected, proceed with the updates
        schedule_entry.TimeSlot = timeslot.SlotID
        schedule_entry.Professor = professor_entry.FacultyID
        schedule_entry.Classroom = room_entry.RoomID
        print(f"[INFO] Updated Schedule for Course ID {course_id}: TimeSlot={timeslot.SlotID}, "
              f"Professor={professor_entry.FacultyID}, Room={room_entry.RoomID}.")
        has_updates = True

        # Remove the 'edited' tag from the row
        tree.item(row, tags=())

    if has_updates:
        # Commit the changes to the database only if updates were made
        scheduler.db.safe_commit()
        print("[INFO] Database update complete.")

        # Run conflict detection again and update the conflict tree view
        print("[INFO] Running conflict detection...")
        update_conflict_treeview()
        print("[INFO] Conflict tree view updated.")
    else:
        print("[INFO] No changes detected. Database update skipped.")


# ---------------------------
# StartPage: Frame 2
# ---------------------------
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        OUTPUT_PATH = Path(__file__).parent
        ASSETS_PATH = OUTPUT_PATH / Path(r"assets/frame_start")
        def relative_to_assets(path: str) -> Path:
            return ASSETS_PATH / Path(path)

        orig_width, orig_height = 1455, 1041
        new_width, new_height = 800, 600
        scale_x, scale_y = new_width / orig_width, new_height / orig_height

        style = ttk.Style()
        # Without changing the overall theme, simply ensure the progress bar's background is blue:
        style.configure("CustomBlue.Horizontal.TProgressbar", background="#79BCF7")

        canvas = Canvas(self, bg="#FFFFFF", height=orig_width, width=orig_height,
                        bd=0, highlightthickness=0, relief="ridge")
        canvas.place(x=0, y=0)
        
        canvas.create_rectangle(0.0, 1.0, 235.0, 1042.0, fill="#79BCF7", outline="")
        
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
        
        # Start Button
        button_image_6 = scaled_photoimage(str(relative_to_assets("button_6.png")), scale_x, scale_y)
        button_6 = Button(self, image=button_image_6, borderwidth=0, highlightthickness=0,
                          command=self.runScheduler, relief="flat")
        button_6.image = button_image_6
        button_6.place(x=1100.0 * scale_x, y=36.0 * scale_y, width=206.0 * scale_x, height=101.0 * scale_y)
        ToolTip(button_6, msg="Click to Generate Schedule", delay=0.5)

        #  CANCLE bottom
        # button_image_7 = scaled_photoimage(str(relative_to_assets("button_7.png")), scale_x, scale_y)
        # button_7 = Button(self, image=button_image_7, borderwidth=0, highlightthickness=0,
        #                   command=lambda: print("button_7 clicked"), relief="flat")
        # button_7.image = button_image_7
        # button_7.place(x=1224.0 * scale_x, y=36.0 * scale_y, width=200.0 * scale_x, height=112.0 * scale_y)
        
       # Status and conflict summary text
        # canvas.create_text(2000.0 * scale_x, 270.0 * scale_y, anchor="nw",
        #                    text="Status:", fill="#094478",
        #                    font=("Jomolhari Regular", int(20 * scale_y)))
        canvas.create_rectangle(935.0, 339.0, 1435.0, 818.0, fill="#FFFFFF", outline="")
        canvas.create_text(1064.0, 339.0, anchor="nw",
                           text="Conflict  Summary：", fill="#094478",
                           font=("Jomolhari Regular", int(20 * -1)))
        

        #conflict_tree section
        conflict_columns = ("Faculty", "Type", "Course")
        global conflict_tree
        conflict_tree = ttk.Treeview(self, columns=conflict_columns, show="headings")
        for col in conflict_columns:
            conflict_tree.heading(col, text=col)
            conflict_tree.column(col, width=80, anchor="center")
        canvas.create_window(950.0, 380.0, anchor="nw", width=450.0, height=350.0, window=conflict_tree)
        conflict_scroll = ttk.Scrollbar(self, orient="vertical", command=conflict_tree.yview)
        conflict_tree.configure(yscrollcommand=conflict_scroll.set)
        conflict_scroll.place(x=1400.0 * scale_x, y=365.0 * scale_y, height=400.0 * scale_y)        

        # canvas.create_text(1800.0 * scale_x, 350.0 * scale_y, anchor="nw",
        #                    text="status info", fill="#000000",
        #                    font=("Jomolhari Regular", int(15 * scale_y)))
        
        # # Lower right button
        # button_image_8 = scaled_photoimage(str(relative_to_assets("button_8.png")), scale_x, scale_y)
        # button_8 = Button(self, image=button_image_8, borderwidth=0, highlightthickness=0,
        #                   command=lambda: print("button_8 clicked"), relief="flat")
        # button_8.image = button_image_8
        # button_8.place(x=1206.0 * scale_x, y=737.0 * scale_y, width=200.0 * scale_x, height=65.0 * scale_y)
        
        # Automatically Resolve Button
        #button_image_8 = scaled_photoimage(str(relative_to_assets("button_8.png")), scale_x, scale_y)
        #button_8 = Button(self, image=button_image_8, borderwidth=0, highlightthickness=0,
        #                  command=lambda: print("button_8 clicked"), relief="flat")
        #button_8.image = button_image_8
        #button_8.place(x=1090.0 * scale_x, y=737.0 * scale_y, width=200.0 * scale_x, height=65.0 * scale_y)
        #ToolTip(button_8, msg="Resolve All Conflicts", delay=1.0)




#******************************************view conflict************************************************
        # button_image_9 = scaled_photoimage(str(relative_to_assets("button_9.png")), scale_x, scale_y)
        # button_9 = Button(self, image=button_image_9, borderwidth=0, highlightthickness=0,
        #               command=lambda: controller.show_frame("ConflictPage"), relief="flat")
        # button_9.image = button_image_9
        # button_9.place(x=972.0 * scale_x, y=741.0 * scale_y, width=200.0 * scale_x, height=61.0 * scale_y)
        
        # Back Button
        # button_image_10 = scaled_photoimage(str(relative_to_assets("button_10.png")), scale_x, scale_y)
        # button_10 = Button(self, image=button_image_10, borderwidth=0, highlightthickness=0,
        #                    command=lambda: print("button_10 clicked"), relief="flat")
        # button_10.image = button_image_10
        # button_10.place(x=942.0 * scale_x, y=893.0 * scale_y, width=200.0 * scale_x, height=101.0 * scale_y)
        # #ToolTip(button_10, msg="Back", delay=0.5)

        
         # Update Button
        button_image_11 = scaled_photoimage(str(relative_to_assets("button_11.png")), scale_x, scale_y)
        button_11 = Button(
            self,
            image=button_image_11,
            borderwidth=0,
            highlightthickness=0,
            command=update_database_from_treeview,  # Call the update function
            relief="flat"
        )
        button_11.image = button_image_11
        button_11.place(x=1224.0 * scale_x, y=893.0 * scale_y, width=200.0 * scale_x, height=101.0 * scale_y)
        ToolTip(button_11, msg="Apply Schedule Changes", delay=0.5)

        
        #logo iamge
        img1 = scaled_photoimage(str(relative_to_assets("image_1.png")), scale_x, scale_y)
        canvas.create_image(215.0 * scale_x, 1700.0 * scale_y, image=img1)
        canvas.image = img1




        # Divider
        canvas.create_rectangle(916.98816, 153.4765, 1455.01141, 154.4765, fill="#094478", outline="")
        canvas.create_rectangle(918.0, 314.0, 1456.02325, 315.0, fill="#094478", outline="")
        
        # Table section
        columns = ("Course ID", "Day", "Time", "Professor", "Room")
        global tree #Use global var so it can be updated when the scheduler is run
        tree = ttk.Treeview(self, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=30, anchor="center")
        courses = [
            # ("CS 115", "Intro to Programming", "9:00 AM - 10:30 AM", "Room 341", "Dr. Echo", "Mon, Wed"),
            # ("CS 310", "Data Structures", "10:45 AM - 12:15 PM", "Room 243", "Dr. Juliet", "Tue, Thu"),
            # ("CS 382", "Algorithms", "1:00 PM - 2:30 PM", "Room 341", "Dr. Lima", "Mon, Wed, Fri"),
            # ("CS 419", "Artificial Intelligence", "2:45 PM - 4:15 PM", "Room 134", "Dr. Lima", "Tue, Thu"),
            # ("CS 438", "Machine Learning", "4:30 PM - 6:00 PM", "Room 241", "Dr. November", "Mon, Wed"),
            # ("CS 452", "Computer Security", "6:15 PM - 7:45 PM", "Room 244", "Dr. Foxtrot", "Tue, Thu"),
            # ("CS 501", "Advanced Programming", "8:00 AM - 9:30 AM", "Room 244", "Dr. November", "Mon, Wed"),
            # ("CS 558", "Cryptography", "9:45 AM - 11:15 AM", "Room 244", "Dr. Hotel", "Tue, Thu"),
            # ("CS 572", "Deep Learning", "11:30 AM - 1:00 PM", "Room 244", "Dr. Dog", "Mon, Wed, Fri"),
        ]
        for course in courses:
            tree.insert("", "end", values=course)
        tree_scroll = ttk.Scrollbar(self, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=tree_scroll.set)
        canvas.create_window(240, 9, width=671, height=1026, anchor="nw", window=tree)
        tree_scroll.place(x=911.0 * scale_x, y=9 * scale_y, height=1026 * scale_y)
        
        make_treeview_editable()
      
        canvas.scale("all", 0, 0, scale_x, scale_y)

        # Add progress bar widget:
        self.scheduleProgress = ttk.Progressbar(self,
                                                style="CustomBlue.Horizontal.TProgressbar",
                                                orient="horizontal",
                                                length=200,
                                                mode="determinate")  # Or "indeterminate"
        self.scheduleProgress['value'] = 0  # Only visible in "determinate" mode
        self.scheduleProgress.place(x=1020.0 * scale_x,
                                    y=210.0 * scale_y)
        canvas.create_text(1020.0 * scale_x + 100, 210.0 * scale_y - 20,
                           text="Status:", fill="#094478",
                           font=("Jomolhari Regular", int(20 * -1)),
                           anchor="center")
    def updateProgress(self, value):
        """Update the progress bar value."""
        print(f"UpdateProgress: {value}%")
        self.scheduleProgress['value'] = value
        self.update_idletasks()

    def runScheduler(self):
        def scheduler_worker():
            # If schedule is empty, generate it; otherwise, show popup info.
            if scheduler.is_schedule_empty():
                scheduler.generate_schedule(update_callback=lambda prog: self.scheduleProgress.configure(value=prog))
                conflicts = scheduler.validate_faculty_preferences()
                if conflicts:
                    print("Conflicts found:")
                    for conflict in conflicts:
                        print(conflict)
                else:
                    print("No faculty preference conflicts found.")
            else:
                print("Schedule already exists.")
                self.scheduleProgress['value'] = 100
                messagebox.showinfo("Info", "A schedule already exists. Please delete the existing schedule if you want to generate a new one.")
            
            update_treeview()
            update_conflict_treeview()

        threading.Thread(target=scheduler_worker, daemon=True).start()

