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
import re
from datetime import datetime
import tkinter.messagebox as mbox

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
class ViewPageTimes(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        OUTPUT_PATH = Path(__file__).parent
        ASSETS_PATH = OUTPUT_PATH / Path(r"assets/frame_view_times")

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

        # Replace the old single-column treeview with a multi-column treeview that doesn't show the SlotID
        self.columns_times = ("Days", "Start Time", "End Time")
        self.tree_Time = ttk.Treeview(self, columns=self.columns_times, show="headings", height=10)
        for col in self.columns_times:
            self.tree_Time.heading(col, text=col, command=lambda _col=col: self.sort_treeview(_col, False))
            self.tree_Time.column(col, width=int(1150 * scale_x)//len(self.columns_times), anchor="center")
        self.tree_Time.place(x=271.0 * scale_x, y=124.0 * scale_y, width=1150.0 * scale_x, height=700.0 * scale_y)
        
        self.scrollbar_times = ttk.Scrollbar(self, orient="vertical", command=self.tree_Time.yview)
        self.tree_Time.configure(yscrollcommand=self.scrollbar_times.set)
        self.scrollbar_times.place(x=271.0 * scale_x + 1150.0 * scale_x, y=124.0 * scale_y, width=15, height=700.0 * scale_y)
        
        self.tree_Time.tag_configure("evenrow", background="#E6F2FF")
        self.tree_Time.tag_configure("oddrow", background="#FFFFFF")
        
        # Update the add_time function to call update_treeview after DB insertion
        def add_time():
            # Retrieve values from the input fields
            days = entry.get().strip()
            start_time = entry2.get().strip()
            end_time = entry3.get().strip()

            # Ensure all fields are filled
            if not (days and start_time and end_time):
                mbox.showerror("Missing Field", "Please fill in Days, Start Time, and End Time.")
                return

            # Validate days: Must only contain M, T, W, R, F with each letter only once
            if not re.fullmatch(r"(?!.*(.).*\1)[MTWRF]+", days):
                mbox.showerror("Invalid Days", "Days must only contain the letters M, T, W, R, F with no duplicates.")
                return

            # Validate start and end times using the 24hr format HH:MM
            try:
                start_dt = datetime.strptime(start_time, "%H:%M")
            except ValueError:
                mbox.showerror("Invalid Start Time", "Please enter a valid start time in 24hr format (HH:MM).")
                return

            try:
                end_dt = datetime.strptime(end_time, "%H:%M")
            except ValueError:
                mbox.showerror("Invalid End Time", "Please enter a valid end time in 24hr format (HH:MM).")
                return

            if end_dt <= start_dt:
                mbox.showerror("Time Order Error", "End time must be after start time. \nPlease also be sure to use the 24hr format instead of 12hr format.")
                return

            # Check for duplicate timeslot in the database
            db = DatabaseManager()
            db.start_session()
            existing_slots = db.get_timeslot()
            for slot in existing_slots:
                if slot.Days == days and slot.StartTime == start_time and slot.EndTime == end_time:
                    mbox.showerror("Duplicate Timeslot", "This timeslot already exists in the database.")
                    db.end_session()
                    return

            # Add the new timeslot since all validations passed
            try:
                db.add_timeslot(days=days, start_time=start_time, end_time=end_time)
                db.end_session()
                # Refresh the treeview after DB insertion
                self.update_treeview()
                # Clear the input fields
                entry.delete(0, "end")
                entry2.delete(0, "end")
                entry3.delete(0, "end")
            except Exception as e:
                db.end_session()
                mbox.showerror("Error Adding Timeslot", f"Error adding timeslot: {e}")
    
        btn13_img = scaled_photoimage(str(relative_to_assets("button_13.png")), scale_x, scale_y)
        btn13 = Button(self, image=btn13_img, borderwidth=0, highlightthickness=0, command=add_time)
        btn13.image = btn13_img
        btn13.place(x=1192.0 * scale_x, y=935.0 * scale_y, width=200.0 * scale_x, height=80.0 * scale_y)

#——————————————————————————————————————————————————
#          USER add PART
#——————————————————————————————————————————————————

        canvas.create_rectangle(258.0* scale_x,845.0 * scale_y,1431.0* scale_x, 1032.0 * scale_y, fill="#DAEBFA", outline="")
        #----------------------------------------------------------------------------------------------------------------
        canvas.create_text(  277.0* scale_x,  873.0 * scale_y, anchor="nw", text="Days   ：", fill="#094478", font=("Jomolhari Regular",9))
        entry = Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=0, font=("Arial", int(16 * scale_y)))
        entry.place(x=401.0 * scale_x, y=864.0 * scale_y, width=260 * scale_x, height=50 * scale_y)
        #----------------------------------------------------------------------------------------------------------------
        canvas.create_text( 277.0* scale_x,973.0 * scale_y, anchor="nw", text="Start Time：", fill="#094478", font=("Jomolhari Regular",9))
        entry2 = Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=0, font=("Arial", int(16 * scale_y)))
        entry2.place(x=401.0 * scale_x, y=965.0 * scale_y, width=260 * scale_x, height=50 * scale_y)
        #----------------------------------------------------------------------------------------------------------------
        canvas.create_text( 727.0* scale_x,974.0 * scale_y, anchor="nw", text="End Time：", fill="#094478", font=("Jomolhari Regular",9))
        entry3 = Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=0, font=("Arial", int(16 * scale_y)))
        entry3.place(x=844.0 * scale_x, y=965.0 * scale_y, width=260 * scale_x, height=50 * scale_y)
        #----------------------------------------------------------------------------------------------------------------

        self.tree_Time.bind("<Button-3>", self.show_context_menu)

    # In update_treeview, store the SlotID as the item iid:
    def update_treeview(self):
        # Clear the existing data in the Treeview
        for item in self.tree_Time.get_children():
            self.tree_Time.delete(item)

        # Fetch timeslots from the database and populate the treeview
        db = DatabaseManager()
        db.start_session()
        timeslots = db.get_timeslot()
        db.end_session()

        for i, slot in enumerate(timeslots):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.tree_Time.insert("", "end", iid=slot.SlotID, values=(
                slot.Days,
                slot.StartTime,
                slot.EndTime
            ), tags=(tag,))

    # Add these methods for the right-click deletion:
    def show_context_menu(self, event):
        # Identify the row under the pointer
        item = self.tree_Time.identify_row(event.y)
        if item:
            # Create a context menu
            menu = tk.Menu(self, tearoff=0)
            menu.add_command(label="Delete", command=lambda: self.delete_item(item))
            menu.post(event.x_root, event.y_root)

    def delete_item(self, item):
        vals = self.tree_Time.item(item, 'values')  # (Days, Start Time, End Time)
        if not vals or len(vals) < 3:
            print("Cannot determine timeslot details.")
            return
        days, start_time, end_time = vals[0], vals[1], vals[2]
        try:
            db = DatabaseManager()
            db.start_session()
            db.delete_timeslot_by_values(days, start_time, end_time)
            db.end_session()
            self.update_treeview()
        except Exception as e:
            print(f"Error deleting timeslot: {e}")

    def sort_treeview(self, col, reverse):
        # Get values and item ids from treeview
        l = [(self.tree_Time.set(k, col), k) for k in self.tree_Time.get_children('')]
        try:
            l.sort(key=lambda t: float(t[0]) if t[0].replace('.','',1).isdigit() else t[0], reverse=reverse)
        except Exception:
            l.sort(reverse=reverse)
        for index, (val, k) in enumerate(l):
            self.tree_Time.move(k, '', index)
        self.tree_Time.heading(col, command=lambda: self.sort_treeview(col, not reverse))


    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.update_treeview()










