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

                self.canvas.itemconfigure(self.success_img_id, state='hidden')
                self.canvas.itemconfigure(self.failed_img_id, state='hidden')
                self.canvas.itemconfigure(self.uploading_img_id, state='normal')
                try:
                    # Parse the CSV file and populate the database
                    parse_csv(file_path)

                try:
                    os.makedirs("uploads", exist_ok=True)
                    target_path = os.path.join("uploads", selected_name)
                    shutil.copy(file_path, target_path)
                    #**************************************************************************************************************************
                    parse_csv_2(target_path)
                    #**************************************************************************************************************************

                    # Prompt success
                    self.canvas.itemconfigure(self.uploading_img_id, state='hidden')
                    self.canvas.itemconfigure(self.success_img_id, state='normal')
                    messagebox.showinfo("Upload Successfully", f"{selected_name} The database has been successfully imported。")
                    self.notify_view_page_refresh()
                    



                except Exception as e:
                    print(f"Error parsing CSV: {e}")
                    self.canvas.itemconfigure(self.uploading_img_id, state='hidden')
                    self.canvas.itemconfigure(self.failed_img_id, state='normal')
                    messagebox.showerror("Upload failed", f"Unable to parse the file：\n{e}")


        self.file_tree = ttk.Treeview(self, columns=("filename", "action"), show="headings", height=8)
        self.file_tree.heading("filename", text="Uploaded Files")
        self.file_tree.column("filename", width=420, anchor="center")
        self.file_tree.heading("action", text="Action")
        self.file_tree.column("action", width=180, anchor="center")
        self.file_tree.place(x=280 * scale_x, y=250 * scale_y, width=600, height=400)
        



        self.refresh_file_list()




        # File refresh button
        refresh_img = scaled_photoimage(str(relative_to_assets("refresh_button.png")), scale_x, scale_y)
        refresh_btn = Button(self, image=refresh_img, borderwidth=0, highlightthickness=0,
                             command=self.refresh_file_list, relief="flat")
        refresh_btn.image = refresh_img
        refresh_btn.place(x=452.0 * scale_x, y=958.0 * scale_y, width=290 * scale_x, height=69 * scale_y)

        self.refresh_file_list()


         #file confirm Button
        confirm_img = scaled_photoimage(str(relative_to_assets("confirm_button.png")), scale_x, scale_y)
        confirm_btn = Button(self, image=confirm_img, borderwidth=0, highlightthickness=0,
                             command=self.refresh_file_list, relief="flat")
        confirm_btn.image = confirm_img
        confirm_btn.place(x=918.0 * scale_x, y=958.0 * scale_y, width=290 * scale_x, height=69 * scale_y)

        
        # File upload button: covers a large area, click to trigger upload
        btn6_img = scaled_photoimage(str(relative_to_assets("button_6.png")), scale_x, scale_y)
        btn6 = Button(self, image=btn6_img, borderwidth=0, highlightthickness=0,
                      command=upload_file, relief="flat")
        btn6.image = btn6_img
        btn6.place(x=250.0 * scale_x, y=25.0 * scale_y, width=1177.0 * scale_x, height=211.0 * scale_y)
        


        
        # self.canvas.create_text(481.0 * scale_x, 452.0 * scale_y, anchor="nw",
        #                    text="File name", fill="#094478", font=("Roboto Black", int(20 * scale_y)))
        # self.canvas.create_text(482.0 * scale_x, 615.0 * scale_y, anchor="nw",
        #                    text="File name", fill="#094478", font=("Roboto Black", int(20 * scale_y)))




        #logo img
        img1 = scaled_photoimage(str(relative_to_assets("image_1.png")), scale_x, scale_y)
        self.canvas.create_image(215.0 * scale_x, 1700.0 * scale_y, image=img1)
        self.canvas.image = img1
        
       # upload success img ✅
        img2 = scaled_photoimage(str(relative_to_assets("image_2.png")), scale_x, scale_y)
        self.success_img_id = self.canvas.create_image(
            372.0 * scale_x, 322.0 * scale_y, image=img2, state='hidden'
        )
        self.canvas.image2 = img2  

        # uploading img ⏳
        img3 = scaled_photoimage(str(relative_to_assets("image_3.png")), scale_x, scale_y)
        self.uploading_img_id = self.canvas.create_image(
            372.0 * scale_x, 467.0 * scale_y, image=img3, state='hidden'
        )
        self.canvas.image3 = img3

        # upload failed img ❌
        img4 = scaled_photoimage(str(relative_to_assets("image_4.png")), scale_x, scale_y)
        self.failed_img_id = self.canvas.create_image(
            372.0 * scale_x, 633.0 * scale_y, image=img4, state='hidden'
        )
        self.canvas.image4 = img4

        
        self.canvas.scale("all", 0, 0, scale_x, scale_y)
        

    def notify_view_page_refresh(self):
        try:
            view_page = self.controller.frames["ViewPageOverall"]
            view_page.refresh_file_dropdown()
        except Exception as e:
                
            print("refresh ViewPageOverall failed:", e)
            

    def refresh_file_list(self):
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)

        if not os.path.exists("uploads"):
            os.makedirs("uploads")

        for file in os.listdir("uploads"):
            self.file_tree.insert("", "end", values=(file, "Delete"))

        # Add delete button click event
        def on_tree_click(event):
            selected = self.file_tree.selection()
            if selected:
                item = self.file_tree.item(selected[0])
                filename = item["values"][0]
                column = self.file_tree.identify_column(event.x)
                if column == "#2":  # Delete action
                    full_path = os.path.join("uploads", filename)
                    if os.path.exists(full_path):
                        os.remove(full_path)
                        self.refresh_file_list()
                        self.notify_view_page_refresh()
                        messagebox.showinfo("Deleted", f"File '{filename}' has been deleted.")

        self.file_tree.bind("<ButtonRelease-1>", on_tree_click)


