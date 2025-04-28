# <img src="https://github.com/user-attachments/assets/e1b85d21-63d4-44ac-8c50-8ff701847f0d" alt="course_logo" height="50">  Course Scheduling System

 <img src="https://github.com/user-attachments/assets/fd1f1438-dd6f-477c-af18-4e988dd09942" alt="course_logo" height="80">



**University of Alabama in Huntsville**  \
**CS 499 Spring 2025**

---

## 📑 Table of Contents
- [📌 Project Overview](#project-overview)
- [👥 Team Members](#team-members)
- [⏰ Timeline](#timeline)
- [🔨 Building The Executable](#Building-The-Executable)
- [🧑‍💻 User Manual](#user-manual)
- [🗂 Source Files and Folder Structure](#source-files-and-folder-structure)
  - [🖥 Pages](#pages)
  - [⚙️ Logic / Utils](#logic--utils)
  - [🖼 Assets](#assets)
- [📦 Dependencies](#dependencies)
- [🧰 Scheduling Algorithm Details](#scheduling-algorithm-details)

---

## 📌 Project Overview
This system is a desktop application designed for university course scheduling. It allows administrative users to import course and faculty data, automatically generate a schedule that avoids room/time conflicts, and provide an interface for viewing, editing, and exporting that schedule. 
The application was built using Python with the Tkinter GUI toolkit and SQLAlchemy ORM for database interaction.

---

## 👥 Team Members
- Tristan McGinnis: Team Lead  
- James Kennedy: Technical Writer  
- Jinyan Fu  
- Elisabeth Elgin

---

## ⏰ Timeline
Start Date: 1/12/2025  \
Finalized: 4/27/2025

---
# 🔨 Building The Executable
1. Ensure you're on a windows machine with Python3 installed (this should be default with any standard windows install)
2. In the COURSE folder, run **Build.bat**
3. After completion, the executable can be found in the **build** folder

---

# 🧑‍💻 User Manual
1. Go to the **Upload** tab to upload the `.csv` files  
2. Click **Confirm** to add files to the schedule generator  
3. Use **View Files** to manually add additional information not previously uploaded  
4. Navigate the tabs at the top of **View Files** to add specific data (Courses, Faculty, etc.)  
    > Click **Add** to insert entries  
    > Right-click on data rows to **Delete** entries  
5. Select **Generate Schedule** from the sidebar and press **Start** to generate the schedule  
6. Double-Clock on values to make changes to the schedule to make desired changes and/or resolve conflicts.
    > Select **Update** to commit changes to the schedule. Erorrs or warnings will show here if some changes cannot be made.
    > In case you'd like to revert changes that were unable to be committed, you can select **Start** again to revert uncommitted changes.
7. Review schedule conflicts under **Conflict Summary**  
8. Navigate to **Export Schedule**, choose a filter (optional)  
9. Click **Export** to download the schedule as both `.csv` and `.pdf`  
    > Tooltips are available by hovering over buttons and fields for additional help

### Resetting to generate a new schedule
When you've finished generating your schedule or would like to undo your progress thus far to restart you must:
1. Close the application
2. In the application's directory remove the following:
    > course.db file
    > uploads folder
3. Relaunch the app and it's ready to go again!

---

# 🗂 Source Files and Folder Structure

## 🖥 Pages

This project is organized using modular page-based Tkinter views. Each of these is implemented as a `tk.Frame` class and rendered by a central `controller`.

- `homePage.py`– Welcome page with application overview and navigation panel. Contains logo, usage instructions, and navigation buttons on the left.
  
  <img src="https://github.com/user-attachments/assets/a29aae77-d47f-4671-a866-00a9cd19ca4c" alt="course_logo" height="400">

- `uploadPage.py` –  File uploader with drag-and-drop support. Shows files in a Treeview, with "Confirm" to parse and load data. Uploads are remembered across sessions.
  
   <img src="https://github.com/user-attachments/assets/e3fcd682-ff75-415c-92c6-8f2e72d3d896" alt="course_logo" height="400">

- `viewPage_overall.py` – Dashboard-like view that shows a summary of all courses, faculty, rooms, preferences, and time slots.
  
   <img src="https://github.com/user-attachments/assets/2e9dba73-fd46-4eac-b8dd-b6fe971eee88" alt="course_logo" height="400">

- `viewPage_course.py` –  Dedicated view to see, add, and remove course entries, including course ID, department, capacity, and required rooms
  
   <img src="https://github.com/user-attachments/assets/1fa19dc8-eae6-4759-8477-5a0dbf3d85aa" alt="course_logo" height="400">

- `viewPage_faculty.py` – View and manage professor records. Allows assigning up to five courses per professor with priorities.
  
   <img src="https://github.com/user-attachments/assets/eea0d853-76a6-4521-9013-d9544076ec72" alt="course_logo" height="400">

- `viewPage_preference.py` – Set room, day, and time preferences for each faculty member. Preferences are stored in the database and used during scheduling.
  
   <img src="https://github.com/user-attachments/assets/c65335f8-97e8-4694-bb95-df680676c6a3" alt="course_logo" height="400">

- `viewPage_rooms.py` – List and manage classroom records including room ID, department, building, and capacity.
  
   <img src="https://github.com/user-attachments/assets/1aca7cba-f039-45f6-9478-1ecc21079bce" alt="course_logo" height="400">

- `viewPage_times.py` – Define and manage available time slots. Each slot includes days, start time, and end time.
  
   <img src="https://github.com/user-attachments/assets/c45f41cb-ae6b-42a9-89f8-8cfb8af395a8" alt="course_logo" height="400">

- `startPage.py` – Scheduler runner. Lets the user start the auto-scheduling process, review scheduling status, and inspect conflict groups.
  
   <img src="https://github.com/user-attachments/assets/de59c76d-6b13-45d0-be89-d5d07287bd9f" alt="course_logo" height="400">

- `exportPage.py` – Lets the user filter the final schedule by Faculty, Room, or Department and export it to both CSV and PDF. Includes two dropdowns and a TreeView for review.
  
   <img src="https://github.com/user-attachments/assets/7e25b19b-6632-4e74-bf89-ab6c84865805" alt="course_logo" height="400">

- `settingPage.py` – Allows the user to customize font and font size to their preference.
  
   <img src="https://github.com/user-attachments/assets/56d72729-ed38-45d6-b9b7-91ed030b68f9" alt="course_logo" height="400">



## ⚙️ Logic / Utils

- `Scheduler.py` – generates conflict-aware schedules with:

  - Prioritized time slot assignment.
  - Faculty preference validation (room, day, time).
  - Course → Professor → Room allocation logic.
  - Conflict detection (room double-booking, room capacity, professor overlap).

- `CSV_Parser.py` – parses input from:

  - Spreadsheet-style CSV (`parse_csv`)
  - old parse no longer use (`parse_csv_2`) 

- `CSV_Exporter.py` – generates `.csv` and `.pdf` exports of scheduled data using FPDF.

  - Supports filtering by Faculty, Room, or Department.
  - Outputs include: course ID, assigned room, timeslot, instructor, capacity.

- `DatabaseManager.py` – ORM-based DB manager built on SQLAlchemy:

  - Defines table schemas for `Faculty`, `Course`, `Classroom`, `TimeSlot`, `Preference`, `Schedule`.
  - CRUD operations for each table.
  - Robust integrity checking and rollback support.

## 🖼 Assets

Assets are organized into folders by view:

- `frame_export/`, `frame_setting/`, `frame_start/`, `frame_upload/`
- `frame_view/`, `frame_view_course/`, `frame_view_faculty/`, `frame_view_overall/`
- `frame_view_preference/`, `frame_view_rooms/`, `frame_view_times/`
- `framehome/`

**Design tools used:**

- UI prototyped in **Figma**
- Converted to Python with [Tkinter Designer](https://github.com/ParthJadhav/Tkinter-Designer)
- Icons sourced from [IconFinder](https://www.iconfinder.com/)

**Color Palette:**

- `#0A4578` – Deep Blue
- `#7ABDF8` – Light Blue
- `#FFFFFF` – White
- `#DAEBFA` – Soft Blue
- `#A3D1F9` – Mid Blue

## 📦 Dependencies

Listed in `venv_requirements.txt`:

```txt
altgraph==0.17.4
fpdf==1.7.2
greenlet==3.1.1
packaging==24.2
pefile==2023.2.7
pillow==11.1.0
pyinstaller==6.12.0
pyinstaller-hooks-contrib==2025.2
pywin32-ctypes==0.2.3
setuptools==78.1.0
SQLAlchemy==2.0.40
tkinter-tooltip==3.1.2
tkinterdnd2==0.4.3
typing_extensions==4.13.1
```

These packages enable:

- GUI: `tkinter`, `tkinter-tooltip`, `tkinterdnd2`
- Database: `SQLAlchemy`
- Export: `fpdf`, `csv`
- Image handling: `pillow`
- Packaging: `pyinstaller`

---

# 🧰 Scheduling Algorithm Details

Location: `lib/Scheduler.py`

### Steps:
1. **Sort** courses with required room or faculty preferences
2. **Assign** timeslots based on time/day preferences
3. **Verify** room and professor availability
4. **Fallback** to non-preferred options if needed
5. **Commit** valid schedule entry to the database
6. **Detect conflicts** with `validate_faculty_preferences()`
   - Room mismatch with preference or course requirement
   - Professor double-booking
   - Room capacity overflow
   - Time/day preference violations

---

💡 **Note:** The `SettingPage` is currently under construction. Features like font/theme toggles and layout preferences will be added in future updates.

