from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, and_, or_
from .DatabaseManager import DatabaseManager, Faculty, Course, TimeSlot, Schedule, Classroom, Preference  # Assuming database_manager.py contains the schema

import logging
from datetime import datetime

# ============================
# CLASS: CourseScheduler
# ============================
# This class is responsible for managing the scheduling of courses, professors, and classrooms.
# It interacts with the database to retrieve data, apply scheduling logic, and store the final schedule.
class CourseScheduler:
    def __init__(self, db_url="sqlite:///course.db"):
        # Initialize the database connection and session
        self.db = DatabaseManager(db_url)
        self.db.start_session()
        self.session = self.db.session

    # ============================
    # METHOD: is_schedule_empty
    # ============================
    # Checks if the schedule table in the database is empty.
    def is_schedule_empty(self):
        return self.session.query(Schedule).count() == 0

    # ============================
    # METHOD: get_sorted_courses
    # ============================
    # Retrieves all courses from the database, sorted by:
    # 1. Whether the associated faculty member has a preference.
    # 2. Whether the course has required rooms.
    # 3. Faculty priority (ascending order).
    def get_sorted_courses(self, session):
        query = session.query(Course).outerjoin(
            Faculty,
            or_(
                Course.CourseID == Faculty.Class1,
                Course.CourseID == Faculty.Class2,
                Course.CourseID == Faculty.Class3,
                Course.CourseID == Faculty.Class4,
                Course.CourseID == Faculty.Class5
            )
        ).order_by(
            or_(
                Course.ReqRoom1.isnot(None),
                Course.ReqRoom2.isnot(None),
                Course.ReqRoom3.isnot(None),
                Course.ReqRoom4.isnot(None),
                Course.ReqRoom5.isnot(None)
            ).desc(),
            Faculty.Priority.asc().nulls_last()
        )
        return query.all()

    # ============================
    # METHOD: get_preferred_slots
    # ============================
    # Retrieves the preferred time slots for a given professor based on their preferences for days and times.
    def get_preferred_slots(self, professor):
        all_slots = self.session.query(TimeSlot).all()  # Get all available time slots
        prioritized_slots = []

        # Query day preferences for the professor, ordered by their priority
        dayPreferences = self.session.query(Preference).filter(
            Preference.FacultyID == professor.FacultyID, Preference.PreferenceType == "Day"
        ).order_by(Preference.PreferenceID).all()  # Ensure days are processed in the order they were added

        # Query time preferences for the professor, ordered by their priority
        timePreferences = self.session.query(Preference).filter(
            Preference.FacultyID == professor.FacultyID, Preference.PreferenceType == "Time"
        ).order_by(Preference.PreferenceID).all()  # Ensure times are processed in the order they were added

        print(f"Day Preferences for Professor {professor.Name}: {[day.PreferenceValue for day in dayPreferences]}") # Debugging output
        print(f"Time Preferences for Professor {professor.Name}: {[time.PreferenceValue for time in timePreferences]}") # Debugging output

        # Helper function to check if two day patterns overlap
        def days_overlap(slot_days, preferred_days):
            # Convert slot_days and preferred_days into sets of individual days
            slot_days_set = set(slot_days)  # e.g., "MW" → {'M', 'W'}
            for day_pattern in preferred_days:
                preferred_days_set = set(day_pattern)  # e.g., "MTWF" → {'M', 'T', 'W', 'F'}
                # Check if there is any overlap between the two sets
                if slot_days_set & preferred_days_set:  # Intersection of the two sets
                    return True
            return False

        # Filter slots based on day preferences in order of priority
        prioritized_day_slots = []
        if dayPreferences:
            for day in dayPreferences:  # Process days in the order they are stored
                prioritized_day_slots += [
                    slot for slot in all_slots if days_overlap(slot.Days, [day.PreferenceValue])
                ]
        else:
            prioritized_day_slots = all_slots

        # Process time preferences in order of priority
        for time in timePreferences:
            if time.PreferenceValue == "Morning":
                prioritized_slots += [
                    slot for slot in prioritized_day_slots
                    if datetime.strptime(slot.StartTime, "%H:%M") < datetime.strptime("12:00", "%H:%M")    # Check if the start time is before noon
                    and datetime.strptime(slot.EndTime, "%H:%M") <= datetime.strptime("12:00", "%H:%M")    # Check if the end time is before noon
                ]
            elif time.PreferenceValue == "Afternoon":
                prioritized_slots += [
                    slot for slot in prioritized_day_slots
                    if datetime.strptime("12:00", "%H:%M") <= datetime.strptime(slot.StartTime, "%H:%M") < datetime.strptime("17:00", "%H:%M")   # Check if the start time is between noon and 5 PM
                    and datetime.strptime(slot.EndTime, "%H:%M") <= datetime.strptime("17:00", "%H:%M")   # Check if the end time is before 5 PM
                ]
            elif time.PreferenceValue == "Evening":
                prioritized_slots += [
                    slot for slot in prioritized_day_slots
                    if datetime.strptime(slot.StartTime, "%H:%M") >= datetime.strptime("17:00", "%H:%M") # Check if the start time is after 5 PM
                ]

        # If no slots match the time preferences, fall back to day preferences only
        if not prioritized_slots:
            prioritized_slots = prioritized_day_slots

        # Remove slots where the professor is already scheduled
        filtered_slots = []
        for slot in prioritized_slots:
            if not self.is_professor_occupied(professor, slot):
                filtered_slots.append(slot)

        print(f"Prioritized slots for Professor {professor.Name}: {[slot.StartTime + '-' + slot.EndTime for slot in filtered_slots]}") # Debugging output
        return filtered_slots

    # ============================
    # METHOD: is_professor_occupied
    # ============================
    # Checks if a professor is already scheduled for a given time slot.
    def is_professor_occupied(self, professor, timeslot):
        # Query all schedules for the professor
        conflicting_schedules = self.session.query(Schedule).filter(
            Schedule.Professor == professor.FacultyID
        ).all()

        # Check for conflicts with existing schedules
        for schedule in conflicting_schedules:
            existing_timeslot = self.session.query(TimeSlot).filter(
                TimeSlot.SlotID == schedule.TimeSlot
            ).first()

            # Check if the days overlap
            existing_days_set = set(existing_timeslot.Days)  # e.g., "MWF" → {'M', 'W', 'F'}
            current_days_set = set(timeslot.Days)  # e.g., "MW" → {'M', 'W'}
            if existing_days_set & current_days_set:  # Check if there is any overlap in days
                # Check if the times overlap
                existing_start = datetime.strptime(existing_timeslot.StartTime, "%H:%M")
                existing_end = datetime.strptime(existing_timeslot.EndTime, "%H:%M")
                current_start = datetime.strptime(timeslot.StartTime, "%H:%M")
                current_end = datetime.strptime(timeslot.EndTime, "%H:%M")

                if (current_start < existing_end and current_end > existing_start):  # Time overlap
                    print(f"Conflict detected for Professor {professor.Name}: "
                          f"Existing Timeslot {existing_timeslot.Days} {existing_timeslot.StartTime}-{existing_timeslot.EndTime} "
                          f"conflicts with Current Timeslot {timeslot.Days} {timeslot.StartTime}-{timeslot.EndTime}") # Debugging output
                    return True

        return False

    # ============================
    # METHOD: is_room_occupied
    # ============================
    # Checks if a room is already occupied during a given time slot.
    def is_room_occupied(self, room, timeslot):
        # Query all schedules for the room
        conflicting_schedules = self.session.query(Schedule).filter(
            Schedule.Classroom == room.RoomID
        ).all()

        # Check for conflicts with existing schedules
        for schedule in conflicting_schedules:
            existing_timeslot = self.session.query(TimeSlot).filter(
                TimeSlot.SlotID == schedule.TimeSlot
            ).first()

            # Check if the days overlap
            existing_days_set = set(existing_timeslot.Days)  # e.g., "MWF" → {'M', 'W', 'F'}
            current_days_set = set(timeslot.Days)  # e.g., "MW" → {'M', 'W'}
            if existing_days_set & current_days_set:  # Check if there is any overlap in days
                # Check if the times overlap
                existing_start = datetime.strptime(existing_timeslot.StartTime, "%H:%M")
                existing_end = datetime.strptime(existing_timeslot.EndTime, "%H:%M")
                current_start = datetime.strptime(timeslot.StartTime, "%H:%M")
                current_end = datetime.strptime(timeslot.EndTime, "%H:%M")

                if (current_start < existing_end and current_end > existing_start):  # Time overlap
                    print(f"Room {room.RoomID} is occupied during {existing_timeslot.Days} "
                          f"{existing_timeslot.StartTime}-{existing_timeslot.EndTime}")
                    return True

        return False

    # ============================
    # METHOD: generate_schedule
    # ============================
    # Generates the schedule by assigning courses to professors, time slots, and rooms.
    def generate_schedule(self, update_callback=None):
        sorted_courses = self.get_sorted_courses(self.session)  # Get sorted courses
        all_faculty = self.db.get_faculty()  # Get all faculty members

        #Vars for progress bar
        num_courses = len(sorted_courses)
        progress_increment = 100 / num_courses if num_courses > 0 else 100


        # Iterate over each course to assign it
        for idx, course in enumerate(sorted_courses):
            print(f"Scheduling: CourseID: {course.CourseID}, MaxEnrollment: {course.MaxEnrollment}")  # Debugging output
            for professor in (p for p in all_faculty if course.CourseID in (p.Class1, p.Class2, p.Class3, p.Class4, p.Class5)):  # Get professors for the course
                preferred_timeslots = self.get_preferred_slots(professor)  # Use get_preferred_slots to get preferred time slots for the professor

                # Handle required rooms
                required_rooms = [
                    course.ReqRoom1, course.ReqRoom2, course.ReqRoom3, course.ReqRoom4, course.ReqRoom5  # Get required rooms
                ]
                required_rooms = [room for room in required_rooms if room is not None]  # Filter out None values

                final_timeslot = None  # Initialize final timeslot
                final_room = None  # Initialize final room

                # Check preferred time slots and required rooms
                for slot in preferred_timeslots:
                    if self.is_professor_occupied(professor, slot):  # Check if the professor is already occupied
                        #print(f"Professor {professor.Name} is occupied during {slot.Days} {slot.StartTime}-{slot.EndTime}")
                        continue

                    for room_id in required_rooms:
                        room = self.session.query(Classroom).filter(Classroom.RoomID == room_id).first()  # Get the room object
                        if room and room.Department == course.Department:  # Check if the room matches the course's department
                            if room.Capacity >= course.MaxEnrollment and not self.is_room_occupied(room, slot):  # Check if the room is available
                                final_timeslot = slot  # Assign the timeslot
                                final_room = room  # Assign the room
                                break
                    if final_timeslot:  # If a suitable timeslot and room are found, break out of the loop
                        break

                # If no required room is available, find any suitable room within preferred time slots
                if not final_timeslot:
                    for slot in preferred_timeslots:  # Iterate over preferred timeslots again
                        if self.is_professor_occupied(professor, slot):  # Check if the professor is already occupied
                            #print(f"Professor {professor.Name} is occupied during {slot.Days} {slot.StartTime}-{slot.EndTime}")
                            continue

                        for room in self.db.get_classrooms():  # Get all classrooms
                            if room.Department == course.Department:  # Check if the room matches the course's department
                                if room.Capacity >= course.MaxEnrollment and not self.is_room_occupied(room, slot):  # Check if the room is available
                                    final_timeslot = slot  # Assign the timeslot
                                    final_room = room  # Assign the room
                                    break
                        if final_timeslot:
                            break

                # If no preferred time slots are available, skip the assignment
                if not final_timeslot:
                    #print(f"FAILED TO ASSIGN: CourseID: {course.CourseID}, Professor: {professor.Name} (No preferred time slots available)")  # Debugging output
                    continue

                # Commit to the schedule table
                if final_timeslot and final_room:  # If a suitable timeslot and room are found
                    self.db.add_schedule(final_timeslot, professor, course, final_room)  # Add to the schedule
                    #print(f"ASSIGNED: CourseID: {course.CourseID}, Professor: {professor.Name}, "
                          #f"Timeslot: {final_timeslot.Days} {final_timeslot.StartTime}-{final_timeslot.EndTime}, "
                          #f"Room: {final_room.RoomID}")
                else:
                    #print(f"FAILED TO ASSIGN: CourseID: {course.CourseID}, Professor: {professor.Name}")  # Debugging output
                    pass
            #Update progress if a callback is provided
            if update_callback:
                progress = (idx + 1) / len(sorted_courses) * 100
                print(f"Progress: {progress:.2f}%")  # Debugging output
                update_callback(progress)
    # ============================
    # METHOD: return_schedule
    # ============================
    # Retrieves the final schedule and converts it into a user-friendly format.
    def return_schedule(self):
        schedule = self.session.query(Schedule).all() # Get all schedule entries
        formatted_schedule = [] # Initialize an empty list to store the formatted schedule

        # Convert IDs to actual values for the user
        for entry in schedule:
            timeslot = self.session.query(TimeSlot).filter(TimeSlot.SlotID == entry.TimeSlot).first() # Get the timeslot object
            timeslot_days = timeslot.Days # Get the days of the timeslot
            timeslot_starttime = timeslot.StartTime # Get the start time of the timeslot

            professor = self.session.query(Faculty).filter(Faculty.FacultyID == entry.Professor).first() # Get the professor object
            professor_name = professor.Name # Get the name of the professor

            formatted_schedule.append([entry.Course, timeslot_days, timeslot_starttime, professor_name, entry.Classroom]) # Append the formatted entry to the list

        return formatted_schedule # Return the formatted schedule

    # ============================
    # METHOD: validate_faculty_preferences
    # ============================
    # Validates if the assigned schedule respects the faculty's preferences for rooms, times, and days.
    def validate_faculty_preferences(self):
        conflicts = []  # List to store conflicts

        # Retrieve the schedule
        schedule = self.session.query(Schedule).all()

        # Dictionary to track room bookings by day and time
        room_bookings = {}

        for entry in schedule:
            # Get faculty, timeslot, room, and course details
            professor = self.session.query(Faculty).filter(Faculty.FacultyID == entry.Professor).first()
            timeslot = self.session.query(TimeSlot).filter(TimeSlot.SlotID == entry.TimeSlot).first()
            room = self.session.query(Classroom).filter(Classroom.RoomID == entry.Classroom).first()
            course = self.session.query(Course).filter(Course.CourseID == entry.Course).first()

            # Retrieve faculty preferences
            room_preferences = self.session.query(Preference).filter(
                Preference.FacultyID == professor.FacultyID,
                Preference.PreferenceType == "Room"
            ).all()
            time_preferences = self.session.query(Preference).filter(
                Preference.FacultyID == professor.FacultyID,
                Preference.PreferenceType == "Time"
            ).all()
            day_preferences = self.session.query(Preference).filter(
                Preference.FacultyID == professor.FacultyID,
                Preference.PreferenceType == "Day"
            ).all()

            # Check room preference
            preferred_rooms = [pref.PreferenceValue for pref in room_preferences]
            if preferred_rooms and room.RoomID not in preferred_rooms:
                conflicts.append({
                    "type": "Room Pref",
                    "course": course.CourseID,
                    "professor": professor.Name,
                    "assigned_room": room.RoomID,
                    "preferred_rooms": preferred_rooms
                })

            # Check time preference
            preferred_times = []
            for time_pref in time_preferences:
                if time_pref.PreferenceValue == "Morning":
                    preferred_times.append(("00:00", "12:00"))
                elif time_pref.PreferenceValue == "Afternoon":
                    preferred_times.append(("12:00", "17:00"))
                elif time_pref.PreferenceValue == "Evening":
                    preferred_times.append(("17:00", "23:59"))

            assigned_start = datetime.strptime(timeslot.StartTime, "%H:%M")
            assigned_end = datetime.strptime(timeslot.EndTime, "%H:%M")
            time_conflict = True
            for start, end in preferred_times:
                pref_start = datetime.strptime(start, "%H:%M")
                pref_end = datetime.strptime(end, "%H:%M")
                if pref_start <= assigned_start and assigned_end <= pref_end:
                    time_conflict = False
                    break

            if time_conflict:
                conflicts.append({
                    "type": "Time Pref",
                    "course": course.CourseID,
                    "professor": professor.Name,
                    "assigned_timeslot": f"{timeslot.Days} {timeslot.StartTime}-{timeslot.EndTime}",
                    "preferred_times": [f"{start}-{end}" for start, end in preferred_times]
                })

            # Check day preference
            preferred_days = [pref.PreferenceValue for pref in day_preferences]
            assigned_days = set(timeslot.Days)  # e.g., "MWF" → {'M', 'W', 'F'}
            day_conflict = True
            for day_pattern in preferred_days:
                preferred_days_set = set(day_pattern)  # e.g., "MTWF" → {'M', 'T', 'W', 'F'}
                if assigned_days & preferred_days_set:  # Check for overlap
                    day_conflict = False
                    break

            if day_conflict:
                conflicts.append({
                    "type": "Day Pref",
                    "course": course.CourseID,
                    "professor": professor.Name,
                    "assigned_days": timeslot.Days,
                    "preferred_days": preferred_days
                })

            # Check required rooms
            required_rooms = [course.ReqRoom1, course.ReqRoom2, course.ReqRoom3, course.ReqRoom4, course.ReqRoom5]
            required_rooms = [room_id for room_id in required_rooms if room_id is not None]  # Filter out None values

            if required_rooms and room.RoomID not in required_rooms:
                conflicts.append({
                    "type": "ReqRoom",
                    "course": course.CourseID,
                    "assigned_room": room.RoomID,
                    "required_rooms": required_rooms
                })

            # Check for double-booked rooms
            booking_key = (room.RoomID, frozenset(timeslot.Days), timeslot.StartTime, timeslot.EndTime)
            if booking_key in room_bookings:
                conflicts.append({
                    "type": "Double Booked Room",
                    "room": room.RoomID,
                    "conflicting_courses": [room_bookings[booking_key], course.CourseID],
                    "timeslot": f"{timeslot.Days} {timeslot.StartTime}-{timeslot.EndTime}"
                })
            else:
                room_bookings[booking_key] = course.CourseID

        return conflicts

