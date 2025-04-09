import csv
from lib.DatabaseManager import DatabaseManager, Faculty, Course, Classroom, TimeSlot, Schedule

def export_schedule_to_csv(output_file):
    # Initialize DatabaseManager
    db_manager = DatabaseManager()
    db_manager.start_session()

    # Query the schedule table
    schedules = db_manager.session.query(Schedule).all()

    # Open the CSV file for writing
    with open(output_file, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Write the header row
        writer.writerow(["Faculty Name", "Course ID", "Classroom", "Days", "Start Time", "End Time"])

        # Write the schedule data
        for schedule in schedules:
            # Retrieve related data
            faculty = db_manager.session.query(Faculty).filter_by(FacultyID=schedule.Professor).first()
            course = db_manager.session.query(Course).filter_by(CourseID=schedule.Course).first()
            classroom = db_manager.session.query(Classroom).filter_by(RoomID=schedule.Classroom).first()
            timeslot = db_manager.session.query(TimeSlot).filter_by(SlotID=schedule.TimeSlot).first()

            # Extract details
            faculty_name = faculty.Name if faculty else "N/A"
            course_id = course.CourseID if course else "N/A"
            classroom_id = classroom.RoomID if classroom else "N/A"
            days = timeslot.Days if timeslot else "N/A"
            start_time = timeslot.StartTime if timeslot else "N/A"
            end_time = timeslot.EndTime if timeslot else "N/A"

            # Write the row to the CSV file
            writer.writerow([faculty_name, course_id, classroom_id, days, start_time, end_time])

    print(f"Schedule successfully exported to {output_file}")

# Example usage
if __name__ == "__main__":
    export_schedule_to_csv("schedule_output.csv")