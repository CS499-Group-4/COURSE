# The purpose of this code is to parse the .csv that we generate into organized data. 
# James Kennedy 2025
# CS 499-01

import csv
from lib.DatabaseManager import DatabaseManager, Course
from datetime import datetime

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

            # Reorder timeslot data based on the preferred times
            ordered_timeslots = []
            for preferred_time in preferred_times:
                if preferred_time == "Morning":
                    ordered_timeslots += [
                        {"start_time": start_time, "end_time": end_time}
                        for start_time, end_time in zip(start_times, end_times)
                        if datetime.strptime(start_time, "%H:%M") < datetime.strptime("12:00", "%H:%M")
                        and datetime.strptime(end_time, "%H:%M") <= datetime.strptime("12:00", "%H:%M")
                    ]
                elif preferred_time == "Afternoon":
                    ordered_timeslots += [
                        {"start_time": start_time, "end_time": end_time}
                        for start_time, end_time in zip(start_times, end_times)
                        if datetime.strptime("12:00", "%H:%M") <= datetime.strptime(start_time, "%H:%M") < datetime.strptime("17:00", "%H:%M")
                        and datetime.strptime(end_time, "%H:%M") <= datetime.strptime("17:00", "%H:%M")
                    ]
                elif preferred_time == "Evening":
                    ordered_timeslots += [
                        {"start_time": start_time, "end_time": end_time}
                        for start_time, end_time in zip(start_times, end_times)
                        if datetime.strptime(start_time, "%H:%M") >= datetime.strptime("17:00", "%H:%M")
                    ]

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