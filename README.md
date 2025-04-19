# 📘 Course Scheduling System
**University of Alabama in Huntsville** <br/>
**CS 499 Spring 2025**


## 📌 Project Overview
This system is a desktop application designed for university course scheduling.\ It allows administrative users to import course and faculty data, automatically generate a schedule that avoids room/time conflicts, and provide an interface for viewing, editing, and exporting that schedule. 
The application was built using Python with the Tkinter GUI toolkit and SQLAlchemy ORM for database interaction.

## 👥 Team Members
Tristan McGinnis: Team Lead\
James Kennedy: Technical Write\
Jinyan Fu\
Elisabeth Elgin

## 🕒 Timeline
Start Date: 1/12/2025 \
Finalized: 4/27/2025



# 🧑‍💻 User Manual
Step 1: Upload CSV
Navigate to Upload Page → Click upload button → Select .csv file (e.g., Dept1ClassData.csv)

Step 2: Generate Schedule
Go to Start Page → Click “Generate Schedule” → View conflict summary if needed

Step 3: View Schedule
Use View Page tabs (Overall/Course/Faculty/Preference/Room/Time) for categorized views

Step 4: Export Schedule
Go to Export Page → Filter results or click export button to save as .csv

Step 5: Customize Settings
Use Setting Page to update fonts or default display behavior



# 🗂 Source Files and Folder Structure
### COURSE.py                 
### PAGES:
   homePage.py              <br/>
   uploadPage.py            <br/>
   startPage.py             <br/>
   viewPage_overall.py      <br/>
   viewPage_course.py       <br/>
   viewPage_faculty.py      <br/>
   viewPage_perferences.py  <br/>
   viewPage_rooms.py        <br/>
   viewPage_times.py        <br/>
   exportPage.py            <br/>
   settingPage.py           <br/>
### lib
   CSV_Parser.py          <br/>
   DatabaseManager.py     <br/>
   Scheduler.py          <br/>

# 📖 Requirements Data Source Format







📈 Page Descriptions







🧰 Scheduling Algorithm Details














