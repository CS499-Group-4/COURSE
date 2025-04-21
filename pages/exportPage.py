import tkinter as tk
from tkinter import Canvas, Button, Entry, Label, ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from pathlib import Path
from PIL import Image, ImageTk
import os
import tkinter.ttk as ttk
from lib.CSV_Exporter import export_schedule_to_csv_and_pdf,export_schedule_to_html
from lib.DatabaseManager import DatabaseManager, Schedule, Course, TimeSlot, Faculty, Classroom
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
class ExportPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.db_manager = DatabaseManager()  # Initialize the database manager
        self.db_manager.start_session()  # Start the database session
        OUTPUT_PATH = Path(__file__).parent
        ASSETS_PATH = OUTPUT_PATH / Path(r"assets/frame_export")

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



#______________________________________________________________MAYBE_____________________________________________________________
        # #search icon
        # entry_image_1 = scaled_photoimage(str(relative_to_assets("entry_1.png")), scale_x, scale_y)
        # entry_bg_1 = canvas.create_image(1301.0 * scale_x, 40.5 * scale_y, image=entry_image_1)
        # self.entry_1 = Entry(self, bd=0, bg="#FFFFFF", fg="#000716", highlightthickness=0)
        # self.entry_1.place(x=1167.0 * scale_x, y=14.0 * scale_y, width=268.0 * scale_x, height=51.0 * scale_y)
        # self.entry_1.bind("<KeyRelease>", self.filter_table)
        # image_2 = scaled_photoimage(str(relative_to_assets("image_2.png")), scale_x, scale_y)
        # canvas.create_image(2050.0 * scale_x, 70.0 * scale_y, image=image_2)
        # canvas.image = image_2
        # #ToolTip(image_2, msg="Click to Search Schedule", delay=0.5)
# ______________________________________________________________MAYBE_____________________________________________________________





        canvas.create_text(1980.0 * scale_x, 195.0 * scale_y, anchor="nw",
                           text="SORT BY:", fill="#094478",
                           font=("Jomolhari Regular", int(18* scale_y)))
        
        # Export Button
        button_image_6 = scaled_photoimage(str(relative_to_assets("button_6.png")), scale_x, scale_y)
        button_6 = Button(
            self,
            image=button_image_6,
            borderwidth=0,
            highlightthickness=0,
            command=self.export_schedule,  # Call the export_schedule method
            relief="flat"
        )
        button_6.image = button_image_6
        button_6.place(x=1167.0 * scale_x, y=864.0 * scale_y, width=200.0 * scale_x, height=101.0 * scale_y)
        ToolTip(button_6, msg="Export Schedule to .csv and .pdf", delay=0.5)

        # Dropdown Menu 1: Sort Options (only Faculty, Room, and Department)
        sort_options = ["All", "Faculty", "Room", "Department"]
        self.sort_var = tk.StringVar()
        self.sort_var.set("All")  # Default value
        dropdown1 = ttk.OptionMenu(self, self.sort_var, sort_options[0], *sort_options, command=self.update_dropdown2)
        dropdown1.place(x=1204.0 * scale_x, y=107.0 * scale_y, width=150.0 * scale_x, height=55.0 * scale_y)

        # Dropdown Menu 2: Dynamic Options
        self.dropdown2_var = tk.StringVar()
        self.dropdown2_var.set("N/A")  # Default value
        self.dropdown2 = ttk.OptionMenu(self, self.dropdown2_var, "N/A")
        self.dropdown2.place(x=1204.0 * scale_x, y=157.0 * scale_y, width=150.0 * scale_x, height=55.0 * scale_y)
        # Refresh table when second dropdown changes
        self.dropdown2_var.trace("w", lambda *args: self.populate_schedule())

        # Table section
        self.columns = ("Course ID", "Day", "Time", "Professor", "Room")
        global tree
        tree = ttk.Treeview(self, columns=self.columns, show="headings")
        for col in self.columns:
            tree.heading(col, text=col, command=lambda _col=col: self.sort_treeview(_col, False))
            tree.column(col, width=30, anchor="center")
        # Initially empty; it will be populated when the page is shown
        self.courses = []  
        tree_scroll = ttk.Scrollbar(self, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=tree_scroll.set)
        canvas.create_window(240, 9, width=801, height=1026, anchor="nw", window=tree)
        tree_scroll.place(x=555, y=6, height=590)
        self.tree = tree
        
        canvas.scale("all", 0, 0, scale_x, scale_y)
    
    def populate_schedule(self):
        """
        Query the full schedule from the database and insert rows into the treeview.
        Apply additional filtering based on the drop down selections.
        """
        try:
            query = self.db_manager.session.query(
                Course.CourseID,
                TimeSlot.Days,
                TimeSlot.StartTime,
                TimeSlot.EndTime,
                Faculty.Name,
                Classroom.RoomID
            ).join(
                Schedule, Schedule.Course == Course.CourseID
            ).join(
                TimeSlot, Schedule.TimeSlot == TimeSlot.SlotID
            ).join(
                Faculty, Schedule.Professor == Faculty.FacultyID
            ).join(
                Classroom, Schedule.Classroom == Classroom.RoomID
            )
            filter_type = self.sort_var.get()      # e.g., "Faculty", "Room", "Department" or "All"
            filter_value = self.dropdown2_var.get()  # value selected in dropdown2
            if filter_type != "All" and filter_value != "N/A":
                if filter_type == "Faculty":
                    query = query.filter(Faculty.Name == filter_value)
                elif filter_type == "Room":
                    query = query.filter(Classroom.RoomID == filter_value)
                elif filter_type == "Department":
                    query = query.filter(Course.Department == filter_value)
            results = query.all()
        except Exception as e:
            print("[ERROR] Querying schedule failed:", e)
            results = []
        
        # Clear the treeview before inserting new rows.
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Insert each row.
        for course_id, days, start_time, end_time, faculty_name, room_id in results:
            time_str = f"{start_time}-{end_time}"
            self.tree.insert("", "end", values=(course_id, days, time_str, faculty_name, room_id))
        
        self.sort_treeview("Course ID", False)

    def tkraise(self, *args, **kwargs):
        # When the page is shown, populate the schedule.
        super().tkraise(*args, **kwargs)
        self.populate_schedule()

    def export_schedule(self):
        # Prompt the user to select a file location
        output_file = asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Save Schedule as CSV"
        )
        if output_file:
            # Determine the filter type and value based on dropdown selections
            filter_type = self.sort_var.get()  # Dropdown 1 selection
            filter_value = self.dropdown2_var.get()  # Dropdown 2 selection

            # Call the export function with filters
            try:
                export_schedule_to_csv_and_pdf(output_file, filter_type=filter_type, filter_value=filter_value)
                export_schedule_to_html(output_file.replace('.csv', '.html'), filter_type=filter_type, filter_value=filter_value)
                print(f"[INFO] Schedule successfully exported to {output_file}")
            except Exception as e:
                print(f"[ERROR] Failed to export schedule: {e}")

    def update_dropdown2(self, selected_option):
        # Update the second dropdown menu options based on the first dropdown.
        if selected_option == "All":
            self.update_dropdown2_options(["N/A"])
        elif selected_option == "Faculty":
            faculty = self.db_manager.get_faculty()
            faculty_names = [f.Name for f in faculty]
            self.update_dropdown2_options(faculty_names)
        elif selected_option == "Room":
            classrooms = self.db_manager.get_classrooms()
            room_ids = [c.RoomID for c in classrooms]
            self.update_dropdown2_options(room_ids)
        elif selected_option == "Department":
            courses = self.db_manager.get_course()
            departments = list(set(c.Department for c in courses))
            self.update_dropdown2_options(departments)
        # Refresh the table
        self.populate_schedule()

    def update_dropdown2_options(self, options):
        # Update the options in the second dropdown menu.
        menu = self.dropdown2["menu"]
        menu.delete(0, "end")  # Clear existing options
        for option in options:
            menu.add_command(label=option, command=lambda value=option: self.dropdown2_var.set(value))
        self.dropdown2_var.set(options[0])  # Set the first option as the default

    def sort_treeview(self, col, reverse):
        # Get the data to sort: a list of tuples (value, item)
        l = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        try:
            l.sort(key=lambda t: float(t[0]) if t[0].replace('.', '', 1).isdigit() else t[0],
                   reverse=reverse)
        except Exception:
            l.sort(reverse=reverse)
        # Rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            self.tree.move(k, '', index)
        # Reset the heading so that clicking it reverses the sort
        self.tree.heading(col, command=lambda: self.sort_treeview(col, not reverse))
