import tkinter as tk
from tkinter import Canvas, Button, Entry, Label, ttk
from tkinter.filedialog import askopenfilename
from pathlib import Path
from PIL import Image, ImageTk
import os
from lib.DatabaseManager import DatabaseManager, Preference  # Import the DatabaseManager and Preference classes
from lib.CSV_Parser import parse_csv  # Import the parse_csv function
from tkinter import messagebox
#?????????????????????????????????????????????????????????????????????????????????
from lib.CSV_Parser import parse_csv_2
import shutil
import json  # Add this import at the top if not already imported

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
# UploadPage: Frame 1
# ---------------------------
class UploadPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        OUTPUT_PATH = Path(__file__).parent
        ASSETS_PATH = OUTPUT_PATH / Path(r"assets/frame_upload")
        def relative_to_assets(path: str) -> Path:
            return ASSETS_PATH / Path(path)

        orig_width = 1455
        orig_height = 1041
        new_width = 800
        new_height = 600
        scale_x = new_width / orig_width
        scale_y = new_height / orig_height

        self.canvas = Canvas(self, bg="#FFFFFF", height=orig_height, width=orig_width,
                             bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)
        self.canvas.create_rectangle(0.0, 1.0, 235.0, 1042.0, fill="#79BCF7", outline="")

        # Ensure uploads folder exists and set state file in that folder.
        os.makedirs("uploads", exist_ok=True)
        self.state_file = os.path.join("uploads", "uploads_state.json")
        self.file_state = self.load_state()

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
        
       # File upload part: display the selected file name
        self.selected_file_text_id = self.canvas.create_text(
            481.0 * scale_x, 299.0 * scale_y,
            anchor="nw", text="File name", fill="#094478",
            font=("Roboto Black", int(20 * scale_y))
        )
        
        def upload_file():
            file_path = askopenfilename(
                title="Choose file",
                filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))
            )
            if file_path:
                selected_name = os.path.basename(file_path)
                print("Chosen file path:", file_path)
                self.canvas.itemconfig(self.selected_file_text_id, text=selected_name)

                # Hide any previous images
                self.canvas.itemconfigure(self.success_img_id, state='hidden')
                self.canvas.itemconfigure(self.failed_img_id, state='hidden')
                self.canvas.itemconfigure(self.uploading_img_id, state='normal')
                
                # Copy file to uploads folder
                os.makedirs("uploads", exist_ok=True)
                target_path = os.path.join("uploads", selected_name)
                shutil.copy(file_path, target_path)

                # Add the file to the treeview and persist its state.
                self.add_file_entry(selected_name, target_path)
                
                # Finished uploading image indicator
                self.canvas.itemconfigure(self.uploading_img_id, state='hidden')

        # Treeview with 3 columns; "filepath" is hidden.
        self.file_tree = ttk.Treeview(self, columns=("filename", "filepath", "action"),
                                      show="headings", height=8)
        self.file_tree.heading("filename", text="Uploaded Files")
        self.file_tree.column("filename", width=420, anchor="center")
        self.file_tree.heading("filepath", text="File Path")
        self.file_tree.column("filepath", width=0, stretch=False)
        self.file_tree.heading("action", text="Action")
        self.file_tree.column("action", width=180, anchor="center")
        # Display only filename and action columns
        self.file_tree["displaycolumns"] = ("filename", "action")
        self.file_tree.place(x=280 * scale_x, y=250 * scale_y, width=600, height=400)

        # Set tag styles: not_parsed (orange) and parsed (green)
        self.file_tree.tag_configure("not_parsed", background="orange")
        self.file_tree.tag_configure("parsed", background="lightgreen")
        
        # Bind click event for delete action
        self.file_tree.bind("<ButtonRelease-1>", self.on_tree_click)

        self.refresh_file_list()

        # Confirm button now triggers parsing of files.
        confirm_img = scaled_photoimage(str(relative_to_assets("confirm_button.png")), scale_x, scale_y)
        confirm_btn = Button(self, image=confirm_img, borderwidth=0, highlightthickness=0,
                             command=self.confirm_upload, relief="flat")
        confirm_btn.image = confirm_img
        # Center the confirm button horizontally within an 800-pixel wide area:
        # Calculate the center based on the upload button's position and width:
        upload_x = 250 * scale_x
        upload_width = 1177 * scale_x
        confirm_width = 290 * scale_x
        center_x = upload_x + (upload_width - confirm_width) / 2

        confirm_btn.place(x=center_x, y=958.0 * scale_y, width=confirm_width, height=69 * scale_y)

        # File upload button covers a large area.
        btn6_img = scaled_photoimage(str(relative_to_assets("button_6.png")), scale_x, scale_y)
        btn6 = Button(self, image=btn6_img, borderwidth=0, highlightthickness=0,
                      command=upload_file, relief="flat")
        btn6.image = btn6_img
        btn6.place(x=250.0 * scale_x, y=25.0 * scale_y, width=1177.0 * scale_x, height=211.0 * scale_y)
        
        # ...existing image items for logo, success, uploading, failed images...
        img1 = scaled_photoimage(str(relative_to_assets("image_1.png")), scale_x, scale_y)
        self.canvas.create_image(215.0 * scale_x, 1700.0 * scale_y, image=img1)
        self.canvas.image = img1
       
        img2 = scaled_photoimage(str(relative_to_assets("image_2.png")), scale_x, scale_y)
        self.success_img_id = self.canvas.create_image(
            372.0 * scale_x, 322.0 * scale_y, image=img2, state='hidden'
        )
        self.canvas.image2 = img2  

        img3 = scaled_photoimage(str(relative_to_assets("image_3.png")), scale_x, scale_y)
        self.uploading_img_id = self.canvas.create_image(
            372.0 * scale_x, 467.0 * scale_y, image=img3, state='hidden'
        )
        self.canvas.image3 = img3

        img4 = scaled_photoimage(str(relative_to_assets("image_4.png")), scale_x, scale_y)
        self.failed_img_id = self.canvas.create_image(
            372.0 * scale_x, 633.0 * scale_y, image=img4, state='hidden'
        )
        self.canvas.image4 = img4

        self.canvas.scale("all", 0, 0, scale_x, scale_y)

    def load_state(self):
        if os.path.exists(self.state_file):
            with open(self.state_file, "r") as f:
                return json.load(f)
        return {}  # state as a dict mapping file paths to {"filename":..., "status":...}

    def save_state(self):
        with open(self.state_file, "w") as f:
            json.dump(self.file_state, f)

    def add_file_entry(self, filename, filepath):
        # Avoid duplicate entries by checking the file path in our state.
        for item in self.file_tree.get_children():
            vals = self.file_tree.item(item, "values")
            if len(vals) >= 2 and vals[1] == filepath:
                messagebox.showwarning("Duplicate File", f"File '{filename}' is already imported.")
                return
        self.file_state[filepath] = {"filename": filename, "status": "not_parsed"}
        self.save_state()
        self.file_tree.insert("", "end", values=(filename, filepath, "Delete"), tags=("not_parsed",))
    
    def refresh_file_list(self):
        # Clear current entries in treeview.
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)
        os.makedirs("uploads", exist_ok=True)
        # Reload state.
        self.file_state = self.load_state()
        remove_list = []
        for filepath, info in self.file_state.items():
            if not os.path.exists(filepath):
                remove_list.append(filepath)
                continue
            tag = "parsed" if info["status"] == "parsed" else "not_parsed"
            action = "Parsed" if info["status"] == "parsed" else "Delete"
            self.file_tree.insert("", "end", values=(info["filename"], filepath, action), tags=(tag,))
        # Remove missing files from state.
        for fp in remove_list:
            del self.file_state[fp]
        self.save_state()
    
    def on_tree_click(self, event):
        selected = self.file_tree.selection()
        if selected:
            item = selected[0]
            vals = self.file_tree.item(item, "values")
            column = self.file_tree.identify_column(event.x)
            if column == "#2":
                if vals[2] == "Delete":
                    full_path = vals[1]
                    if os.path.exists(full_path):
                        os.remove(full_path)
                    self.file_tree.delete(item)
                    if full_path in self.file_state:
                        del self.file_state[full_path]
                        self.save_state()
                    try:
                        self.notify_view_page_refresh()
                    except Exception as e:
                        print("Failed to refresh view page:", e)
                    messagebox.showinfo("Deleted", f"File '{vals[0]}' has been deleted.")
    
    def confirm_upload(self):
        # When the user confirms, parse files and then lazily mark the database as initialized
        for item in self.file_tree.get_children():
            vals = self.file_tree.item(item, "values")
            filename, filepath, action_text = vals
            if not os.path.exists(filepath):
                messagebox.showerror("Error", f"File '{filename}' does not exist. Removing from list.")
                self.file_tree.delete(item)
                if filepath in self.file_state:
                    del self.file_state[filepath]
                    self.save_state()
                continue
            try:
                # Attempt to parse the file
                parse_csv_2(filepath)
                self.file_tree.item(item, values=(filename, filepath, "Parsed"), tags=("parsed",))
                if filepath in self.file_state:
                    self.file_state[filepath]["status"] = "parsed"
                    self.save_state()
                # Lazy DB initialization: only mark as initialized on a successful parse.
                if not getattr(self.controller, "db_initialized", False):
                    self.controller.db_initialized = True
                    print("Database initialized on first parse.")
                # Optionally call refresh on other pages now that the DB is available.
                self.notify_view_page_refresh()
            except Exception as e:
                messagebox.showerror("Parse Error", f"Error parsing '{filename}': {e}")

    def notify_view_page_refresh(self):
        # Only try to refresh database-dependent pages if the DB flag is set.
        if getattr(self.controller, "db_initialized", False):
            try:
                view_page = self.controller.frames.get("ViewPageOverall")
                if view_page:
                    view_page.refresh_file_dropdown()
            except Exception as e:
                print("Failed to refresh view page:", e)
        else:
            print("Database not yet initialized; skipping view page refresh.")


