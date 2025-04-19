<img src="https://github.com/user-attachments/assets/e1b85d21-63d4-44ac-8c50-8ff701847f0d" alt="course_logo" height="200">

 Course Scheduling System

 <img src="https://github.com/user-attachments/assets/fd1f1438-dd6f-477c-af18-4e988dd09942" alt="course_logo" height="80">



**University of Alabama in Huntsville**  \
**CS 499 Spring 2025**

---

## 📑 Table of Contents
- [📌 Project Overview](#project-overview)
- [👥 Team Members](#team-members)
- [⏰ Timeline](#timeline)
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

# 🧑‍💻 User Manual
1. Go to the **Upload** tab to upload the `.csv` files  
2. Click **Confirm** to add files to the schedule generator  
3. Use **View Files** to manually add additional information not previously uploaded  
4. Navigate the tabs at the top of **View Files** to add specific data (Courses, Faculty, etc.)  
    > Click **Add** to insert entries  
    > Right-click on data rows to **Delete** entries  
5. Select **Generate Schedule** from the sidebar and press **Start** to generate the schedule  
6. Review schedule conflicts under **Conflict Summary**  
7. Navigate to **Export Schedule**, choose a filter (optional)  
8. Click **Export** to download the schedule as both `.csv` and `.pdf`  
    > Tooltips are available by hovering over buttons and fields for additional help

---

# 🗂 Source Files and Folder Structure

## 🖥 Pages

This project is organized using modular page-based Tkinter views. Each of these is implemented as a `tk.Frame` class and rendered by a central `controller`.

- `homePage.py` – main welcome screen.
- `uploadPage.py` – for uploading and parsing CSV files.
- `viewPage.py` – base class for view pages.
- `viewPage_overall.py` – overall summary view.
- `viewPage_course.py` – displays list of courses.
- `viewPage_faculty.py` – displays faculty and class assignments.
- `viewPage_preference.py` – professor preferences (time, room, day).
- `viewPage_rooms.py` – manage classrooms.
- `viewPage_times.py` – manage timeslots.
- `startPage.py` – runs the scheduler and allows editing results.
- `exportPage.py` – export to CSV/PDF with filters.
- `settingPage.py` – UI for future display/font/theme settings (WIP).

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

