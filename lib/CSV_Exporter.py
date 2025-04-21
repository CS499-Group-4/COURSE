import csv
import re
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



    
    schedules = query.order_by(Schedule.Course).all()


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


def export_schedule_to_html(output_file, filter_type=None, filter_value=None):
    """
    Export the schedule to an HTML file containing a preformatted plaintext block.
    The plaintext format uses fixed-width formatting with columns:
      SBJ   Crse   Sec   Days   Time          Instructor           Location
    The CourseID (e.g., "CS 155-01") is parsed to extract:
      - SBJ: the alphabetic subject (e.g., "CS")
      - Crse: the numeric course number (e.g., "155")
      - Sec: the two-digit section (e.g., "01")
    Time is shown as StartTime-EndTime.

    This implementation forces every field into a fixed width.
    The header is bold onscreen and divider lines are added below the header and at the bottom.
    """
    import re
    from lib.DatabaseManager import DatabaseManager, Faculty, Course, Classroom, TimeSlot, Schedule
    db_manager = DatabaseManager()
    db_manager.start_session()

    # Helper: force fixed width (truncate if needed, pad if short)
    def format_field(value, width):
        value = str(value)
        if len(value) > width:
            return value[:width]
        else:
            return value.ljust(width)

    # Define fixed widths for each field
    widths = {"sbj":10, "crse":10, "sec":10, "days":10, "time":15, "instr":20, "loc":10}

    query = db_manager.session.query(Schedule)
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

    schedules = query.order_by(Schedule.Course).all()

    # Build header line using fixed widths:
    header_line = (
        f"{format_field('SBJ', widths['sbj'])} "
        f"{format_field('Crse', widths['crse'])} "
        f"{format_field('Sec', widths['sec'])} "
        f"{format_field('Days', widths['days'])} "
        f"{format_field('Time', widths['time'])}    "
        f"{format_field('Instructor', widths['instr'])} "
        f"{format_field('Location', widths['loc'])}"
    )
    # Wrap the header in bold tags:
    header_bold = f"<b>{header_line}</b>"

    # Build a divider for each column and join them with a gap
    divider = " ".join("-" * widths[col] for col in ["sbj", "crse", "sec", "days", "time", "instr", "loc"])

    # Start building the text lines (with header and divider)
    lines = [header_bold, divider]

    for schedule in schedules:
        faculty = db_manager.session.query(Faculty).filter_by(FacultyID=schedule.Professor).first()
        course = db_manager.session.query(Course).filter_by(CourseID=schedule.Course).first()
        classroom = db_manager.session.query(Classroom).filter_by(RoomID=schedule.Classroom).first()
        timeslot = db_manager.session.query(TimeSlot).filter_by(SlotID=schedule.TimeSlot).first()

        faculty_name = faculty.Name if faculty else "N/A"
        course_id = course.CourseID if course else "N/A"
        room = classroom.RoomID if classroom else "N/A"
        days = timeslot.Days if timeslot else "N/A"
        start_time = timeslot.StartTime if timeslot else "N/A"
        end_time = timeslot.EndTime if timeslot else "N/A"
        time_str = f"{start_time}-{end_time}"

        # Parse the CourseID; expect format like "CS 155-01"
        m = re.match(r'^([A-Za-z]+)\s*(\d+)-(\d+)$', course_id)
        if m:
            sbj = m.group(1)
            crse = m.group(2)
            sec = m.group(3)
        else:
            sbj, crse, sec = "N/A", "N/A", "N/A"

        line = (
            f"{format_field(sbj, widths['sbj'])} "
            f"{format_field(crse, widths['crse'])} "
            f"{format_field(sec, widths['sec'])} "
            f"{format_field(days, widths['days'])} "
            f"{format_field(time_str, widths['time'])}    "
            f"{format_field(faculty_name, widths['instr'])} "
            f"{format_field(room, widths['loc'])}"
        )
        lines.append(line)

    # Add a divider line after the data rows.
    lines.append(divider)

    db_manager.end_session()

    # Wrap the plaintext lines inside <pre> tags within a simple HTML structure.
    html_lines = [
        "<html>",
        "<head><meta charset='utf-8'><title>Schedule Export</title></head>",
        "<body>",
        "<pre>"
    ]
    html_lines.extend(lines)
    html_lines.extend(["</pre>", "</body>", "</html>"])

    with open(output_file, "w", encoding="utf-8") as f:
        for line in html_lines:
            f.write(line + "\n")

    print(f"Schedule successfully exported to {output_file}")

# Example usage
if __name__ == "__main__":
    export_schedule_to_csv_and_pdf("schedule_output.csv")
    export_schedule_to_txt("schedule_output.txt")
    export_schedule_to_html("schedule_output.html")