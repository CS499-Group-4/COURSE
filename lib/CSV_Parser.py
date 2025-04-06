# The purpose of this code is to parse the .csv that we generate into organized data. 
# James Kennedy 2025
# CS 499-01

import csv
from lib.DatabaseManager import DatabaseManager, Course

class Faculty:
    def __init__(self, faculty_id, name, courses, preference):
        # Assign faculty details with support for multiple courses, days, times, and classrooms
        self.FacultyID = faculty_id
        self.Name = name
        self.Courses = courses  # List of courses taught by the faculty
        self.Preference = {
            "priority": preference.get("priority", 0),  # Relative priority
            "days": preference.get("days", []),  # List of preferred days
            "times": preference.get("times", []),  # List of preferred times
            "classrooms": preference.get("classrooms", [])  # List of preferred classrooms
        }

    def print_details(self):
        # Display all faculty information
        print(f"Faculty ID: {self.FacultyID}")
        print(f"Name: {self.Name}")
        print(f"Courses: {', '.join(self.Courses)}")
        print(f"Preference:")
        print(f"  Priority: {self.Preference['priority']}")
        print(f"  Days: {', '.join(self.Preference['days'])}")
        print(f"  Times: {', '.join(self.Preference['times'])}")
        print(f"  Classrooms: {', '.join(self.Preference['classrooms'])}")
        print("---")

#——————————————————————————————————————————————————————
#                         parse_csv
#——————————————————————————————————————————————————————
def parse_csv(file_path):
    # Initialize data storage containers
    faculty_list = []
    classroom_data = []
    course_data = []
    timeslot_data = []

    # Initialize DatabaseManager
    db_manager = DatabaseManager()
    db_manager.start_session()

    # Read the CSV file
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)

    # Parse timeslot data first
    timeslot_start = next(i for i, row in enumerate(rows) if row[0] == "Options for Days to teach")
    days = [d for d in rows[timeslot_start][1:] if d]  # Extract days from the header row
    start_times = [t for t in rows[timeslot_start + 1][1:] if t]  # Extract start times
    end_times = [t for t in rows[timeslot_start + 2][1:] if t]  # Extract end times

    # Create timeslots for every combination of day, start time, and end time
    for day in days:
        for start_time, end_time in zip(start_times, end_times):
            timeslot_data.append({
                "day": day,
                "start_time": start_time,
                "end_time": end_time
            })

            # Add timeslot to the database
            db_manager.add_timeslot(day, start_time, end_time)

    # Parse faculty data
    i = 0
    while i < len(rows):
        row = rows[i]
        if row[0] == "Professor Name":
            name = row[1]
            i += 1
            priority = int(rows[i][1]) if rows[i][1] else 0  # Default priority to 0 if blank
            i += 1
            courses = [c for c in rows[i][1:] if c]  # Filter out blank spaces
            i += 1
            preferred_days = [d for d in rows[i][1:] if d]  # Filter out blank spaces
            i += 1
            preferred_times = [t for t in rows[i][1:] if t]  # Filter out blank spaces
            i += 1
            preferred_classrooms = [c for c in rows[i][1:] if c]  # Filter out blank spaces
            i += 2  # Skip empty rows

            # Create Faculty object
            faculty = Faculty(
                faculty_id=len(faculty_list) + 1,
                name=name,
                courses=courses,
                preference={
                    "priority": priority,
                    "days": preferred_days,
                    "times": preferred_times,
                    "classrooms": preferred_classrooms
                }
            )
            faculty_list.append(faculty)

            # Add faculty to the database
            db_manager.add_faculty(
                name=faculty.Name,
                priority=faculty.Preference["priority"],
                class1=faculty.Courses[0] if len(faculty.Courses) > 0 else None,
                class2=faculty.Courses[1] if len(faculty.Courses) > 1 else None,
                class3=faculty.Courses[2] if len(faculty.Courses) > 2 else None,
                class4=faculty.Courses[3] if len(faculty.Courses) > 3 else None,
                class5=faculty.Courses[4] if len(faculty.Courses) > 4 else None
            )

            # Add preferences to the database
            for day in preferred_days:
                db_manager.add_preference(faculty_name=faculty.Name, preference_type="Day", preference_value=day)
            for time in preferred_times:
                db_manager.add_preference(faculty_name=faculty.Name, preference_type="Time", preference_value=time)
            for room in preferred_classrooms:
                db_manager.add_preference(faculty_name=faculty.Name, preference_type="Room", preference_value=room)

        else:
            i += 1

    # Parse classroom data
    classroom_start = next(i for i, row in enumerate(rows) if row[0] == "Classrooms available")
    classroom_rows = rows[classroom_start + 1:classroom_start + 5]  # Extract rows for classroom attributes
    room_ids = rows[classroom_start][1:]  # Extract room IDs from the header row

    for col_index, room_id in enumerate(room_ids):
        if room_id:  # Skip empty columns
            try:
                classroom = {
                    "room_id": room_id,
                    "department": classroom_rows[0][col_index + 1],  # Department of the classroom
                    "building": classroom_rows[1][col_index + 1],    # Building of the classroom
                    "seats": int(classroom_rows[2][col_index + 1]) if classroom_rows[2][col_index + 1] else 0  # Seats
                }
                classroom_data.append(classroom)

                # Add classroom to the database
                db_manager.add_classroom(
                    room_id=classroom["room_id"],
                    department=classroom["department"],
                    building=classroom["building"],
                    room=classroom["room_id"],
                    capacity=classroom["seats"]
                )
            except (IndexError, ValueError):
                print(f"Skipping invalid classroom column: {room_id}")

    # Parse course data
    course_start = next(i for i, row in enumerate(rows) if row[0] == "Course Id")
    course_rows = rows[course_start + 1:course_start + 4]  # Extract rows for course attributes
    course_ids = rows[course_start][1:]  # Extract course IDs from the header row

    for col_index, course_id in enumerate(course_ids):
        if course_id:  # Skip empty columns
            try:
                course = {
                    "course_id": course_id,
                    "department": course_rows[0][col_index + 1],  # Department of the course
                    "max_enrollment": int(course_rows[1][col_index + 1]) if course_rows[1][col_index + 1] else 0,  # Max enrollment
                    "required_rooms": [course_rows[2][col_index + 1]] if course_rows[2][col_index + 1] else []  # Required rooms (if any)
                }
                course_data.append(course)

                # Add course to the database
                db_manager.add_course(
                    course_id=course["course_id"],
                    department=course["department"],
                    max_enrollment=course["max_enrollment"],
                    req_room1=course["required_rooms"][0] if len(course["required_rooms"]) > 0 else None,
                    req_room2=course["required_rooms"][1] if len(course["required_rooms"]) > 1 else None,
                    req_room3=course["required_rooms"][2] if len(course["required_rooms"]) > 2 else None,
                    req_room4=course["required_rooms"][3] if len(course["required_rooms"]) > 3 else None,
                    req_room5=course["required_rooms"][4] if len(course["required_rooms"]) > 4 else None
                )
            except (IndexError, ValueError):
                print(f"Skipping invalid course column: {course_id}")

    # Print parsed data
    print("\nParsed Faculty Data:")
    for faculty in faculty_list:
        faculty.print_details()

    print("\nParsed Classroom Data:")
    for classroom in classroom_data:
        print(f"Room ID: {classroom['room_id']}, Department: {classroom['department']}, "
              f"Building: {classroom['building']}, Seats: {classroom['seats']}")

    print("\nParsed Course Data:")
    for course in course_data:
        print(f"Course ID: {course['course_id']}, Department: {course['department']}, "
              f"Max Enrollment: {course['max_enrollment']}, Required Rooms: {', '.join(course['required_rooms'])}")

    print("\nParsed Timeslot Data:")
    for timeslot in timeslot_data:
        print(f"Day: {timeslot['day']}, Start Time: {timeslot['start_time']}, End Time: {timeslot['end_time']}")

    return faculty_list, classroom_data, course_data, timeslot_data


if __name__ == "__main__":
    # Define the file path
    file_path = 'CSVFile.csv'

    try:
        # Parse the CSV file
        faculty_list, classroom_data, course_data, timeslot_data = parse_csv(file_path)

        # Initialize DatabaseManager and start session
        db_manager = DatabaseManager()
        db_manager.start_session()

        # Print data from the database
        print("\nData from the database:")

        print("\nFaculty:")
        for faculty in db_manager.get_faculty():
            print(f"Faculty ID: {faculty.FacultyID}, Name: {faculty.Name}, Priority: {faculty.Priority}, "
                  f"Classes: {faculty.Class1}, {faculty.Class2}, {faculty.Class3}, {faculty.Class4}, {faculty.Class5}")

        print("\nClassrooms:")
        for classroom in db_manager.get_classrooms():
            print(f"RoomID: {classroom.RoomID}, Department: {classroom.Department}, "
                  f"Building: {classroom.Building}, Capacity: {classroom.Capacity}")

        print("\nCourses:")
        for course in db_manager.get_course():
            required_rooms = [
                course.ReqRoom1,
                course.ReqRoom2,
                course.ReqRoom3,
                course.ReqRoom4,
                course.ReqRoom5
            ]
            # Filter out None values from the required rooms
            required_rooms = [room for room in required_rooms if room is not None]
            print(f"CourseID: {course.CourseID}, Department: {course.Department}, "
                  f"MaxEnrollment: {course.MaxEnrollment}, Required Rooms: {', '.join(required_rooms)}")

        print("\nTimeslots:")
        for timeslot in db_manager.get_timeslots():
            print(f"Day: {timeslot.Day}, Start Time: {timeslot.StartTime}, End Time: {timeslot.EndTime}")

        # End the database session
        db_manager.end_session()

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")




#——————————————————————————————————————————————————————
#                         parse_csv_2
#——————————————————————————————————————————————————————
        
def parse_csv_2(file_path, insert_into_db=True):
    db_manager = DatabaseManager()
    db_manager.start_session()

    faculty_list = []
    course_data = []
    classroom_data = []
    timeslot_data = []
    classroom_preferences = []
    preference_data = []

    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    department_line = next((line for line in lines if line.startswith("Department:")), None)
    location_line = next((line for line in lines if line.startswith("Location:")), None)
    department = department_line.split(":")[1].strip() if department_line else "Unknown"
    location = location_line.split(":")[1].strip() if location_line else "Unknown"

    start = lines.index("Courses Offered") + 1
    end = lines.index("Classroom Preferences:")
    course_lines = lines[start:end]
    course_ids = []
    for line in course_lines:
        entries = [c.strip() for c in line.split(",") if c.strip()]
        course_ids.extend(entries)
        for cid in entries:
            if insert_into_db:
                db_manager.add_course(course_id=cid, department=department, max_enrollment=0)
            course_data.append({
                "course_id": cid,
                "department": department,
                "max_enrollment": 0,
                "required_rooms": []
            })

    start = lines.index("Classroom Preferences:") + 1
    end = lines.index("Faculty Assignments:")
    for line in lines[start:end]:
        if "must be taught in" in line:
            course, rest = line.split(" must be taught in ")
            building, room = [x.strip() for x in rest.split(",")]
            classroom_id = room.replace("room", "").strip()
            full_room_id = f"{location.split()[0]}{classroom_id}"
            classroom_preferences.append((course.strip(), full_room_id))
            if insert_into_db:
                db_manager.add_classroom(
                    room_id=full_room_id,
                    department=department,
                    building=building,
                    room=full_room_id,
                    capacity=0
                )
            classroom_data.append({
                "room_id": full_room_id,
                "department": department,
                "building": building,
                "seats": 0
            })

    for course in course_data:
        course_id = course["course_id"]
        for cid, room_id in classroom_preferences:
            if cid == course_id:
                course["required_rooms"].append(room_id)
                if insert_into_db:
                    db_manager.add_course(
                        course_id=course_id,
                        department=department,
                        max_enrollment=0,
                        req_room1=room_id
                    )

    start = lines.index("Faculty Assignments:") + 1
    for line in lines[start:]:
        if not line.strip():
            continue
        if "- Preference:" in line:
            base, pref_str = line.split(" - Preference:")
            pref_str = pref_str.strip()
        else:
            base = line
            pref_str = "None"

        name_and_courses = [x.strip() for x in base.split(",")]
        name = name_and_courses[0]
        courses = name_and_courses[1:]

        pref_struct = {
            "priority": 0,
            "days": [],
            "times": [],
            "classrooms": []
        }

        pref_added = False

        if "Morning" in pref_str:
            pref_struct["times"].append("Morning")
            if insert_into_db:
                db_manager.add_preference(name, "Time", "Morning")
            preference_data.append(f"{name} prefers Time: Morning")
            pref_added = True
        if "Afternoon" in pref_str:
            pref_struct["times"].append("Afternoon")
            if insert_into_db:
                db_manager.add_preference(name, "Time", "Afternoon")
            preference_data.append(f"{name} prefers Time: Afternoon")
            pref_added = True
        if "Evening" in pref_str:
            pref_struct["times"].append("Evening")
            if insert_into_db:
                db_manager.add_preference(name, "Time", "Evening")
            preference_data.append(f"{name} prefers Time: Evening")
            pref_added = True
        if "Mon-Wed" in pref_str:
            pref_struct["days"].append("MW")
            if insert_into_db:
                db_manager.add_preference(name, "Day", "MW")
            preference_data.append(f"{name} prefers Day: MW")
            pref_added = True
        if "Tues-Thurs" in pref_str:
            pref_struct["days"].append("TR")
            if insert_into_db:
                db_manager.add_preference(name, "Day", "TR")
            preference_data.append(f"{name} prefers Day: TR")
            pref_added = True

        if not pref_added:
            preference_data.append(f"{name} has no specific preference")

        if insert_into_db:
            db_manager.add_faculty(
                name=name,
                priority=pref_struct["priority"],
                class1=courses[0] if len(courses) > 0 else None,
                class2=courses[1] if len(courses) > 1 else None,
                class3=courses[2] if len(courses) > 2 else None,
                class4=courses[3] if len(courses) > 3 else None,
                class5=courses[4] if len(courses) > 4 else None
            )

        faculty_obj = type("Faculty", (), {
            "FacultyID": None,
            "Name": name,
            "Courses": courses,
            "Preference": pref_struct
        })()
        faculty_list.append(faculty_obj)

    default_timeslots = [
        ("MW", "08:00", "09:15"), ("MW", "09:35", "10:50"), ("MW", "11:10", "12:25"),
        ("MW", "12:45", "14:00"), ("MW", "14:20", "15:35"), ("MW", "15:55", "17:10"),
        ("MW", "17:30", "18:45"), ("MW", "19:05", "20:20"),
        ("TR", "08:00", "09:15"), ("TR", "09:35", "10:50"), ("TR", "11:10", "12:25"),
        ("TR", "12:45", "14:00"), ("TR", "14:20", "15:35"), ("TR", "15:55", "17:10"),
        ("TR", "17:30", "18:45"), ("TR", "19:05", "20:20")
    ]
    for days, start, end in default_timeslots:
        if insert_into_db:
            db_manager.add_timeslot(days, start, end)
        timeslot_data.append({"day": days, "start_time": start, "end_time": end})

    print("parse_csv_2(): Data import completed")
    return faculty_list, classroom_data, course_data, timeslot_data, preference_data
