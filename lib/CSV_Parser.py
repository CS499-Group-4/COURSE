# The purpose of this code is to parse the .csv that we generate into organized data. 
# James Kennedy 2025
# CS 499-01

import csv
import re
from lib.DatabaseManager import DatabaseManager, Course

class Faculty:
    def __init__(self, faculty_id, name, classes, preference):
        # Assign faculty details with support for fewer than 3 classes, assigning an id to faculty as they are parsed in
        self.FacultyID = faculty_id
        self.Name = name
        self.Class1 = classes[0] if len(classes) > 0 else None
        self.Class2 = classes[1] if len(classes) > 1 else None
        self.Class3 = classes[2] if len(classes) > 2 else None
        self.Preference = preference

    def print_details(self):
        # Display all faculty information
        print(f"Faculty ID: {self.FacultyID}")
        print(f"Name: {self.Name}")
        print(f"Classes: {self.Class1}, {self.Class2}, {self.Class3}")
        print(f"Preference: {self.Preference}")
        print("---")


def parse_csv(file_path):
    # Initialize data storage containers
    faculty_list = []
    classroom_preferences = {}
    courses_offered = []

    # Initialize DatabaseManager
    db_manager = DatabaseManager()
    db_manager.start_session()

    # Read entire file as text lines
    with open(file_path, 'r') as csvfile:
        content = csvfile.read().splitlines()

    # Extract department and location information
    department = content[0].split(': ')[1].strip()
    location = content[1].split(': ')[1].strip()

    # Parse courses using regex to extract precise course codes
    courses_section = content[content.index('Courses Offered') + 1:]
    course_pattern = r'CS \d{3}'  # Matches course codes like CS 499 or ECE 101
    for line in courses_section:
        if 'Classroom Preferences:' in line:
            break
        courses = re.findall(course_pattern, line)
        courses_offered.extend(courses)

    # Extract classroom preferences if available
    pref_start = content.index('Classroom Preferences:')
    if pref_start < len(content) - 1:
        pref_lines = content[pref_start + 1:]
        for pref_line in pref_lines:
            if 'must be taught in' in pref_line:
                course, room_info = pref_line.split(' must be taught in ')
                room_parts = room_info.split(', ')
                building = room_parts[0].strip()
                room = room_parts[1].strip()
                classroom_preferences[course.strip()] = (building, room)

    # Parse faculty assignments with detailed information extraction
    faculty_section = content[content.index('Faculty Assignments:') + 1:]
    for line in faculty_section:
        if line.strip():
            # Split faculty information into components
            parts = line.split(' - ')
            faculty_info = parts[0]
            preference = parts[1].split(': ')[1] if len(parts) > 1 else None

            # Separate name and assigned classes
            name_classes = faculty_info.split(', ')
            name = name_classes[0]
            classes = name_classes[1:]

            # Create Faculty object and add to list
            faculty_list.append(Faculty(
                faculty_id=len(faculty_list) + 1,
                name=name,
                classes=classes,
                preference=preference
            ))

    # Add parsed data to the database
    for course in courses_offered:
        db_manager.add_course(course, None)

    for course in courses_offered:
        req_room = classroom_preferences.get(course, None)
        if req_room is not None:
            building, room = req_room
            # Extract the room number from the tuple and remove any unwanted text
            room_number = room.split()[-1]  # Get the last part after splitting by spaces
            # Get the building abbreviation
            building_abbr = building_abbreviations.get(building, "")
            # Construct the full room assignment
            req_room = f"{building_abbr}{room_number}"
        print(f"Updating course: {course}, ReqRoom: {req_room}")  # Debug print

        # Query the course and update the ReqRoom value
        course_to_update = db_manager.session.query(Course).filter_by(CourseID=course).first()
        if course_to_update:
            course_to_update.ReqRoom = req_room
            db_manager.safe_commit()

    for faculty in faculty_list:
        db_manager.add_faculty(
            name=faculty.Name,
            class1=faculty.Class1,
            class2=faculty.Class2,
            class3=faculty.Class3,
            preference=faculty.Preference
        )

    # Add timeslots to the database
    timeslots = [
        ("MW", "08:00"), ("MW", "09:35"), ("MW", "11:10"), ("MW", "12:45"),
        ("MW", "14:20"), ("MW", "15:55"), ("MW", "17:30"), ("MW", "19:05"),
        ("TR", "08:00"), ("TR", "09:35"), ("TR", "11:10"), ("TR", "12:45"),
        ("TR", "14:20"), ("TR", "15:55"), ("TR", "17:30"), ("TR", "19:05")
    ]

    for days, start_time in timeslots:
        db_manager.add_timeslot(days, start_time)

    # Add classrooms to the database
    classrooms = [
        "OKT131", "OKT132", "OKT133", "OKT134", "OKT241", "OKT242", "OKT243", "OKT244",
        "OKT341", "OKT342", "OKT343", "OKT344", "OKT451", "OKT452", "OKT453", "OKT454"
    ]
    for room in classrooms:
        db_manager.add_classroom(room_id=room, building="Technology Hall", room=room)

    return department, location, courses_offered, classroom_preferences, faculty_list


# Define a mapping of building names to their abbreviations
building_abbreviations = {
    "Technology Hall": "OKT",
    # Add other buildings and their abbreviations here if needed
}

if __name__ == "__main__":
    # Define the file path
    file_path = 'Dept1ClassData.csv'

    try:
        # Parse the CSV file
        department, location, courses_offered, classroom_preferences, faculty_list = parse_csv(file_path)

        # Initialize DatabaseManager and start session
        db_manager = DatabaseManager()
        db_manager.start_session()

        # Add parsed data to the database
        for course in courses_offered:
            db_manager.add_course(course, None)

        for course in courses_offered:
            req_room = classroom_preferences.get(course, None)
            if req_room is not None:
                building, room = req_room
                room_number = room.split()[-1]
                building_abbr = building_abbreviations.get(building, "")
                req_room = f"{building_abbr}{room_number}"
                print(f"Updating course: {course}, ReqRoom: {req_room}")
                course_to_update = db_manager.session.query(Course).filter_by(CourseID=course).first()
                if course_to_update:
                    course_to_update.ReqRoom = req_room
                    db_manager.safe_commit()

        for faculty in faculty_list:
            db_manager.add_faculty(
                name=faculty.Name,
                class1=faculty.Class1,
                class2=faculty.Class2,
                class3=faculty.Class3,
                preference=faculty.Preference
            )

        # Add timeslots to the database
        timeslots = [
            ("MW", "08:00"), ("MW", "09:35"), ("MW", "11:10"), ("MW", "12:45"),
            ("MW", "14:20"), ("MW", "15:55"), ("MW", "17:30"), ("MW", "19:05"),
            ("TR", "08:00"), ("TR", "09:35"), ("TR", "11:10"), ("TR", "12:45"),
            ("TR", "14:20"), ("TR", "15:55"), ("TR", "17:30"), ("TR", "19:05")
        ]
        for days, start_time in timeslots:
            db_manager.add_timeslot(days, start_time)

        # Add classrooms to the database
        classrooms = [
            "OKT131", "OKT132", "OKT133", "OKT134", "OKT241", "OKT242", "OKT243", "OKT244",
            "OKT341", "OKT342", "OKT343", "OKT344", "OKT451", "OKT452", "OKT453", "OKT454"
        ]
        for room in classrooms:
            db_manager.add_classroom(room_id=room, building="Technology Hall", room=room)

        # Print data from the database
        print("\nData from the database:")
        print("\nFaculty:")
        for faculty in db_manager.get_faculty():
            print(f"Faculty ID: {faculty.FacultyID}, Name: {faculty.Name}")

        print("\nClassrooms:")
        for classroom in db_manager.get_classroom():
            print(f"RoomID: {classroom.RoomID}, Building: {classroom.Building}")

        print("\nCourses:")
        for course in db_manager.get_course():
            print(f"CourseID: {course.CourseID}, ReqRoom: {course.ReqRoom}")

        print("\nTimeslots:")
        for timeslot in db_manager.get_timeslot():
            print(f"SlotID: {timeslot.SlotID}, Days: {timeslot.Days}")

        # End the database session
        db_manager.end_session()

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")