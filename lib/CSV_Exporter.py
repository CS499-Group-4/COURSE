import csv
from fpdf import FPDF  # Import FPDF for PDF generation
from lib.DatabaseManager import DatabaseManager, Faculty, Course, Classroom, TimeSlot, Schedule

def export_schedule_to_csv_and_pdf(output_file, filter_type=None, filter_value=None):
    # Initialize DatabaseManager
    db_manager = DatabaseManager()
    db_manager.start_session()

    # Query the schedule table
    query = db_manager.session.query(Schedule)

    # Apply filters based on the user's selection
    if filter_type == "Faculty":
        faculty = db_manager.session.query(Faculty).filter_by(Name=filter_value).first()
        if faculty:
            query = query.filter(Schedule.Professor == faculty.FacultyID)
    elif filter_type == "Room":
        query = query.filter(Schedule.Classroom == filter_value)
    elif filter_type == "Department":
        courses = db_manager.session.query(Course).filter_by(Department=filter_value).all()
        course_ids = [course.CourseID for course in courses]
        query = query.filter(Schedule.Course.in_(course_ids))

    schedules = query.all()

    # Open the CSV file for writing
    with open(output_file, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Write the header row
        header = [
            "Faculty Name", "Course ID", "Classroom", "Days", "Start Time", "End Time",
            "Room Capacity", "Course Max Enroll"
        ]
        writer.writerow(header)

        # Write the filtered schedule data
        rows = []
        for schedule in schedules:
            # Retrieve related data
            faculty = db_manager.session.query(Faculty).filter_by(FacultyID=schedule.Professor).first()  # Get faculty details
            course = db_manager.session.query(Course).filter_by(CourseID=schedule.Course).first()  # Get course details
            classroom = db_manager.session.query(Classroom).filter_by(RoomID=schedule.Classroom).first()  # Get classroom details
            timeslot = db_manager.session.query(TimeSlot).filter_by(SlotID=schedule.TimeSlot).first()  # Get timeslot details

            # Extract details
            faculty_name = faculty.Name if faculty else "N/A"
            course_id = course.CourseID if course else "N/A"
            classroom_id = classroom.RoomID if classroom else "N/A"
            days = timeslot.Days if timeslot else "N/A"
            start_time = timeslot.StartTime if timeslot else "N/A"
            end_time = timeslot.EndTime if timeslot else "N/A"
            room_capacity = classroom.Capacity if classroom else "N/A"
            course_max_enrollment = course.MaxEnrollment if course else "N/A"

            # Write the row to the CSV file
            row = [
                faculty_name, course_id, classroom_id, days, start_time, end_time,
                room_capacity, course_max_enrollment
            ]
            writer.writerow(row)
            rows.append(row)

    print(f"Filtered schedule successfully exported to {output_file}")

    # Generate PDF from the CSV data
    pdf_file = output_file.replace('.csv', '.pdf')
    pdf = FPDF(orientation='L')  # Set orientation to Landscape
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=10)  # Reduce font size to fit more content

    # Calculate column width dynamically based on page width
    page_width = pdf.w - 2 * pdf.l_margin  # Page width minus margins
    col_width = page_width / len(header)  # Divide evenly among columns

    # Add header to the PDF
    pdf.set_font("Arial", style="B", size=10)
    for col in header:
        pdf.cell(col_width, 10, col, border=1)
    pdf.ln()

    # Add rows to the PDF
    pdf.set_font("Arial", size=10)
    for row in rows:
        for col in row:
            pdf.cell(col_width, 10, str(col), border=1)
        pdf.ln()

    pdf.output(pdf_file)
    print(f"Filtered schedule successfully exported to {pdf_file}")

# Example usage
if __name__ == "__main__":
    export_schedule_to_csv_and_pdf("schedule_output.csv")