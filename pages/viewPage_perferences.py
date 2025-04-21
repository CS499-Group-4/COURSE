import tkinter as tk
from tkinter import Canvas, Button, Entry, Label, ttk
from tkinter.filedialog import askopenfilename
from pathlib import Path
from PIL import Image, ImageTk
import os
import tkinter.ttk as ttk
from tktooltip import ToolTip
from lib.CSV_Parser import parse_csv_2
from lib.DatabaseManager import DatabaseManager, Classroom  # Ensure Classroom is imported
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
class ViewPagePreference(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        OUTPUT_PATH = Path(__file__).parent
        ASSETS_PATH = OUTPUT_PATH / Path(r"assets/frame_view_preference")

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

        self.columns5 = ("Faculty Name", "Preference Type", "Preference Value")
        self.tree_Perferences = ttk.Treeview(self, columns=self.columns5, show="headings", height=10)
        for col in self.columns5:
            self.tree_Perferences.heading(col, text=col, command=lambda _col=col: self.sort_treeview(_col, False))
            self.tree_Perferences.column(col, width=int(1150 * scale_x)//len(self.columns5), anchor="center")
        self.tree_Perferences.place(x=271.0 * scale_x, y=124.0 * scale_y, width=1150.0 * scale_x, height=700.0 * scale_y)

        self.tree_Perferences.tag_configure("evenrow", background="#E6F2FF")
        self.tree_Perferences.tag_configure("oddrow", background="#FFFFFF")

        self.scrollbar_preferences = ttk.Scrollbar(self, orient="vertical", command=self.tree_Perferences.yview)
        self.tree_Perferences.configure(yscrollcommand=self.scrollbar_preferences.set)
        self.scrollbar_preferences.place(x=271.0 * scale_x + 1150.0 * scale_x, y=124.0 * scale_y, width=15, height=700.0 * scale_y)

        def add_preference():
            # Retrieve values from the input fields
            name = entry.get().strip()
            preference_type = dropdown_preference.get().strip()
            preference_value = entry3.get().strip()

            # Validate all fields are filled
            if not (name and preference_type and preference_value):
                mbox.showerror("Missing Field", "Please fill in all required fields: Name, Preference Type, and Preference.")
                return

            db = DatabaseManager()
            db.start_session()

            # Validate that the professor exists in the database
            faculties = db.get_faculty()
            if not any(fac.Name.lower() == name.lower() for fac in faculties):
                mbox.showerror("Invalid Professor", f"Professor '{name}' does not exist in the database.")
                db.end_session()
                return

            # Validate a valid preference type is selected (Room, Day, or Time)
            if preference_type.lower() not in {"room", "day", "time"}:
                mbox.showerror("Invalid Preference Type", "Please select a valid Preference Type: Room, Day, or Time.")
                db.end_session()
                return

            # Process based on the selected Preference Type
            if preference_type.lower() == "room":
                # Check if room exists; if not, warn user but still proceed
                room = db.session.query(Classroom).filter_by(RoomID=preference_value.upper()).first()
                if not room:
                    mbox.showwarning(
                        "Room Not Found",
                        f"Room '{preference_value}' does not exist in the database. "
                        "It will need to be added on the Rooms tab in order to be assigned."
                    )
                preference_value = preference_value.upper()
            elif preference_type.lower() == "day":
                # Must be a valid combination of letters: M, T, W, R, F with no duplicates
                if not re.fullmatch(r"(?!.*(.).*\1)[MTWRF]+", preference_value.upper()):
                    mbox.showerror("Invalid Day", "Preference for Day must only contain the letters M, T, W, R, F with no duplicates.")
                    db.end_session()
                    return
                preference_value = preference_value.upper()
            elif preference_type.lower() == "time":
                # Must be one of morning, afternoon, or evening, stored with first letter capitalized
                valid_times = {"morning", "afternoon", "evening"}
                if preference_value.lower() not in valid_times:
                    mbox.showerror("Invalid Time", "Preference for Time must be one of: morning, afternoon, or evening.")
                    db.end_session()
                    return
                preference_value = preference_value.lower().capitalize()

            try:
                # Capitalize the preference type when storing it
                db.add_preference(faculty_name=name, preference_type=preference_type.capitalize(), preference_value=preference_value)
                db.end_session()
                # Refresh the Preferences treeview
                self.update_treeview()
                # Clear the input fields
                entry.delete(0, "end")
                dropdown_preference.set("Select Type")
                entry3.delete(0, "end")
            except Exception as e:
                db.end_session()
                mbox.showerror("Error Adding Preference", f"Error adding preference: {e}")


        btn13_img = scaled_photoimage(str(relative_to_assets("button_13.png")), scale_x, scale_y)
        btn13 = Button(self, image=btn13_img, borderwidth=0, highlightthickness=0, command=add_preference)
        btn13.image = btn13_img
        btn13.place(x=1192.0 * scale_x, y=935.0 * scale_y, width=200.0 * scale_x, height=80.0 * scale_y)
        ToolTip(btn13, msg="Add new data to system", delay=0.5)

#——————————————————————————————————————————————————
#          USER add PART
#——————————————————————————————————————————————————

        canvas.create_rectangle(258.0* scale_x,845.0 * scale_y,1431.0* scale_x, 1032.0 * scale_y, fill="#DAEBFA", outline="")
        #----------------------------------------------------------------------------------------------------------------
        canvas.create_text(  278.0* scale_x,  883.0 * scale_y, anchor="nw", text="Name     ：", fill="#094478", font=("Jomolhari Regular",9))
        entry = Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=0, font=("Arial", int(16 * scale_y)))
        entry.place(x=412.0 * scale_x, y=874.0 * scale_y, width=280 * scale_x, height=50 * scale_y)
        ToolTip(entry, msg="Enter Name of Professor with a Preference \nExample: Dr. Beats", delay=0.5)
        #----------------------------------------------------------------------------------------------------------------
        canvas.create_text( 707.0* scale_x,883.0 * scale_y, anchor="nw", text="Preference Type：", fill="#094478", font=("Jomolhari Regular",9))
        preference_options = ["Room", "Day", "Time"]
        dropdown_preference = ttk.Combobox(self, values=preference_options, state="readonly", font=("Arial", int(16 * scale_y)))
        dropdown_preference.set("Select Type")
        dropdown_preference.place(x=883.0 * scale_x, y=874.0 * scale_y, width=280 * scale_x, height=50 * scale_y)
        #----------------------------------------------------------------------------------------------------------------
        canvas.create_text( 273.0* scale_x,969.0 * scale_y, anchor="nw", text="Preference ：", fill="#094478", font=("Jomolhari Regular",9))
        entry3 = Entry(self, bd=0, bg="#FFFFFF", fg="#000000", highlightthickness=0, font=("Arial", int(16 * scale_y)))
        entry3.place(x=412.0 * scale_x, y=955.0 * scale_y, width=751 * scale_x, height=50 * scale_y)
        ToolTip(entry3, msg="Enter Preference \nDay Example: M/W/T/R/F \nTime Example: Evening \nRoom Example: OKT 125", delay=0.5)
        #----------------------------------------------------------------------------------------------------------------
        self.tree_Perferences.bind("<Button-3>", self.show_context_menu)



    def update_treeview(self):
        for item in self.tree_Perferences.get_children():
            self.tree_Perferences.delete(item)
        db = DatabaseManager()
        db.start_session()
        preferences = db.get_preferences()
        db.end_session()
        for i, pref in enumerate(preferences):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            self.tree_Perferences.insert("", "end", values=(
                pref.ProfessorName,
                pref.PreferenceType,
                pref.PreferenceValue
            ), tags=(tag,))
    
    def show_context_menu(self, event):
        item = self.tree_Perferences.identify_row(event.y)
        if (item):
            menu = tk.Menu(self, tearoff=0)
            menu.add_command(label="Delete", command=lambda: self.delete_item(item))
            menu.post(event.x_root, event.y_root)
    
    def delete_item(self, item):
        vals = self.tree_Perferences.item(item, 'values')  # (Faculty Name, Preference Type, Preference Value)
        if not vals or len(vals) < 3:
            print("Cannot determine preference details.")
            return
        faculty_name, pref_type, pref_value = vals
        try:
            db = DatabaseManager()
            db.start_session()
            db.delete_preference_by_values(faculty_name, pref_type, pref_value)
            db.end_session()
            self.update_treeview()
        except Exception as e:
            print(f"Error deleting preference: {e}")
    
    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.update_treeview()

    def sort_treeview(self, col, reverse):
        # Get values from treeview
        l = [(self.tree_Perferences.set(k, col), k) for k in self.tree_Perferences.get_children('')]
        try:
            l.sort(key=lambda t: float(t[0]) if t[0].replace('.','',1).isdigit() else t[0], reverse=reverse)
        except Exception:
            l.sort(reverse=reverse)
        # Rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            self.tree_Perferences.move(k, '', index)
        # Reverse sort next time
        self.tree_Perferences.heading(col, command=lambda: self.sort_treeview(col, not reverse))











