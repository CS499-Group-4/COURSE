from sqlalchemy import Column, Integer, String, Enum, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import IntegrityError


#from colorama import Fore, Style, init

Base = declarative_base()


class Preference(Base):
    __tablename__ = 'preference'
    PreferenceID = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    FacultyID = Column(Integer, ForeignKey('faculty.FacultyID'), nullable=False)
    PreferenceType = Column(String, nullable=False)  # 'Room', 'Day', 'Time')
    PreferenceValue = Column(String, nullable=False)  # e.g., RoomID or FacultyID

# Faculty table
class Faculty(Base):
    __tablename__ = 'faculty'
    FacultyID = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    Name = Column(String, nullable=False, unique=True)
    Priority = Column(Integer, nullable=True, default=None)  # Default priority
    Class1 = Column(String, nullable=True)
    Class2 = Column(String, nullable=True)
    Class3 = Column(String, nullable=True)
    Class4 = Column(String, nullable=True)
    Class5 = Column(String, nullable=True)
    #All preferences are stored in the preference table


# Classroom table
class Classroom(Base):
    __tablename__ = 'classroom'
    RoomID = Column(String, primary_key=True, unique=True)
    Department = Column(String, nullable=False)  # e.g., CS, ECE
    Building = Column(String, nullable=False)
    Room = Column(String, nullable=False)
    Capacity = Column(Integer, nullable=False)

# Course table
class Course(Base):
    __tablename__ = 'course'
    CourseID = Column(String, primary_key=True, unique=True)
    Department = Column(String, nullable=False)  # e.g., CS, ECE
    MaxEnrollment = Column(Integer, nullable=False)
    ReqRoom1 = Column(Integer, nullable=True)
    ReqRoom2 = Column(Integer, nullable=True)
    ReqRoom3 = Column(Integer, nullable=True)
    ReqRoom4 = Column(Integer, nullable=True)
    ReqRoom5 = Column(Integer, nullable=True)
    # ReqRoom = Column(Integer, ForeignKey('classroom.RoomID'), nullable=True)  # Uncomment for foreign key

# TimeSlot table
class TimeSlot(Base):
    __tablename__ = 'timeslot'
    SlotID = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    Days = Column(String, nullable=False)  # MW/TR
    StartTime = Column(String, nullable=False)
    EndTime = Column(String, nullable=False)

# Conflict table
class ScheduleConflict(Base):
    __tablename__ = 'schedule_conflict'
    ConflictID = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    SchedID = Column(Integer, ForeignKey('schedule.SchedID'), nullable=False)
    GroupID = Column(Integer, ForeignKey('conflict_group.GroupID'), nullable=False)

# Conflict Group table
class ConflictGroup(Base):
    __tablename__ = 'conflict_group'
    GroupID = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    Type = Column(String, nullable=False)  # Room, Professor, Preference (probably will be enum later)


# Schedule table
class Schedule(Base):
    __tablename__ = 'schedule'
    SchedID = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    TimeSlot = Column(Integer, ForeignKey('timeslot.SlotID'), nullable=True)
    Professor = Column(Integer, ForeignKey('faculty.FacultyID'), nullable=False)
    Course = Column(Integer, ForeignKey('course.CourseID'), nullable=False)
    Classroom = Column(Integer, ForeignKey('classroom.RoomID'),nullable=True)

class DatabaseManager:
    def __init__(self, database_url="sqlite:///Course.db"):
        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine)
        # self.session = sessionmaker(bind=self.engine) #create session
        # self.session = self.session() #start session

    # Ends the session
    def end_session(self):
        self.session.close()

    # Starts the session
    def start_session(self):
        self.session = sessionmaker(bind=self.engine)
        self.session = self.session()

    # Commits transactions for the DB, while catching/handling errors
    def safe_commit(self):
        try:
            self.session.commit()
        except IntegrityError as e:
            print("\n[WARN] IntegrityError occurred:")
            print(f"    {e.orig.args[0]}")
            print("    Please check constraints like unique or foreign key violations.\n")
            self.session.rollback()
        except Exception as e:
            print("\n[ERROR] An unexpected error occurred:")
            print(f"    {str(e)}\n")
            self.session.rollback()


    # Functions for adding entries to the database
    def add_faculty(self, name, priority, class1=None, class2=None, class3=None, class4=None, class5=None):
        faculty = Faculty(Name=name, Priority=priority, Class1=class1, Class2=class2, Class3=class3, Class4=class4, Class5=class5)
        self.session.add(faculty)
        self.safe_commit()

    #Function for adding entry for faculty for the ui button
    def add_faculty_ui(self, name, priority, class_ids=None):
        # Ensure class_ids is a list and pad it to match the number of class columns
        class_ids = class_ids or []  # Default to an empty list if None
        class_ids = (class_ids + [None] * 5)[:5]  # Pad with None to ensure exactly 5 elements

        # Map the list elements to the respective class columns
        faculty = Faculty(
            Name=name,
            Priority=priority,
            Class1=class_ids[0],
            Class2=class_ids[1],
            Class3=class_ids[2],
            Class4=class_ids[3],
            Class5=class_ids[4]
        )
        self.session.add(faculty)
        self.safe_commit()

    # Add preferences to the database
    def add_preference(self, faculty_name, preference_type, preference_value):
        #return the facultyID from entry where name = faculty_name
        facultyID = self.session.query(Faculty).filter_by(Name=faculty_name).first()
        if facultyID is None:
            print(f"[WARN] Faculty {faculty_name} not found when trying to add preference.")
            return
        facultyID = facultyID.FacultyID
        if preference_type not in ['Room', 'Day', 'Time']:
            print(f"[WARN] Invalid preference type: {preference_type}. Must be 'Room', 'Day', or 'Time'.")
            return
        
        if preference_type == 'Room':
            preferenceValue = preference_value
        elif preference_type == 'Day':
            # query db all unique "days" values in the timeslot table
            days = self.session.query(TimeSlot.Days).distinct().all()
            # convert to list of strings
            days = [day[0] for day in days]
            if preference_value not in days:
                print(f"[WARN] Invalid day preference: {preference_value}. Must be one of {days}.")
                return
            preferenceValue = preference_value
        elif preference_type == 'Time':
            if preference_value not in ['Morning', 'Afternoon', 'Evening']:
                print(f"[WARN] Invalid time preference: {preference_value}. Must be 'Morning', 'Afternoon', or 'Evening'.")
                return
            preferenceValue = preference_value

        preference = Preference(FacultyID=facultyID, PreferenceType=preference_type, PreferenceValue=preferenceValue)
        self.session.add(preference)
        self.safe_commit()
        

    def add_classroom(self, room_id, department, building, room, capacity):
        classroom = Classroom(RoomID=room_id, Department=department, Building=building, Room=room, Capacity=capacity)
        self.session.add(classroom)
        self.safe_commit()

    def add_course(self, course_id, department, max_enrollment, req_room1=None, req_room2=None, req_room3=None, req_room4=None, req_room5=None):
        course = Course(CourseID=course_id, Department=department, MaxEnrollment=max_enrollment, ReqRoom1=req_room1, ReqRoom2=req_room2, ReqRoom3=req_room3, ReqRoom4=req_room4, ReqRoom5=req_room5)
        self.session.add(course)
        self.safe_commit()

    def add_timeslot(self, days, start_time, end_time):
        timeslot = TimeSlot(Days=days, StartTime=start_time, EndTime=end_time)
        # Check if the timeslot already exists
        existing_timeslot = self.session.query(TimeSlot).filter_by(Days=days, StartTime=start_time, EndTime=end_time).first()
        if existing_timeslot:
            print(f"[WARN] Timeslot {days} {start_time} - {end_time} already exists.")
            return
        self.session.add(timeslot)
        self.safe_commit()

    def add_conflict_group(self, conflict_type):
        conflict_group = ConflictGroup(Type=conflict_type)
        self.session.add(conflict_group)
        self.safe_commit()

    def add_schedule_conflict(self, sched_id, group_id):
        conflict = ScheduleConflict(SchedID=sched_id, GroupID=group_id)
        self.session.add(conflict)
        self.safe_commit()

    def add_schedule(self, timeslot, faculty, course, classroom):
        schedule = Schedule(TimeSlot=timeslot.SlotID, Professor=faculty.FacultyID, Course=course.CourseID, Classroom=classroom.RoomID)
        self.session.add(schedule)
        self.safe_commit()

    def delete_timeslot(self, slot_id):
        timeslot = self.session.query(TimeSlot).filter_by(SlotID=slot_id).first()
        if timeslot:
            self.session.delete(timeslot)
            self.safe_commit()

    def delete_timeslot_by_values(self, days, start_time, end_time):
        timeslot = self.session.query(TimeSlot).filter_by(
            Days=days, StartTime=start_time, EndTime=end_time
        ).first()
        if timeslot:
            self.session.delete(timeslot)
            self.safe_commit()

    def delete_faculty(self, faculty_id):
        faculty = self.session.query(Faculty).filter_by(FacultyID=faculty_id).first()
        if faculty:
            self.session.delete(faculty)
            self.safe_commit()

    def delete_faculty_by_values(self, name, priority, class1, class2, class3, class4, class5):
        faculty = self.session.query(Faculty).filter_by(
            Name=name,
            Priority=priority,
            Class1=class1,
            Class2=class2,
            Class3=class3,
            Class4=class4,
            Class5=class5
        ).first()
        if faculty:
            self.session.delete(faculty)
            self.safe_commit()

    def delete_course(self, course_id):
        course = self.session.query(Course).filter_by(CourseID=course_id).first()
        if course:
            self.session.delete(course)
            self.safe_commit()

    def delete_preference(self, preference_id):
        preference = self.session.query(Preference).filter_by(PreferenceID=preference_id).first()
        if preference:
            self.session.delete(preference)
            self.safe_commit()

    def delete_preference_by_values(self, faculty_name, pref_type, pref_value):
        # First, lookup the FacultyID for the given name:
        faculty = self.session.query(Faculty).filter_by(Name=faculty_name).first()
        if not faculty:
            print(f"[WARN] No faculty found with the name {faculty_name}.")
            return
        preference = self.session.query(Preference).filter_by(
            FacultyID=faculty.FacultyID,
            PreferenceType=pref_type,
            PreferenceValue=pref_value
        ).first()
        if preference:
            self.session.delete(preference)
            self.safe_commit()

    def delete_classroom(self, room_id):
        classroom = self.session.query(Classroom).filter_by(RoomID=room_id).first()
        if classroom:
            self.session.delete(classroom)
            self.safe_commit()

    # Simple query functions
    def get_faculty(self):
        return self.session.query(Faculty).all()

    def get_classrooms(self):
        return self.session.query(Classroom).all()
    
    def get_course(self):
        return self.session.query(Course).all()
    
    def get_timeslot(self):
        return self.session.query(TimeSlot).all()
    
    def get_conflict(self):
        return self.session.query(ScheduleConflict).all()

    def get_conflictGroup(self):
        return self.session.query(ConflictGroup).all()
    
    def get_preferences(self):
        return self.session.query(
            Faculty.Name.label("ProfessorName"),
            Preference.PreferenceType.label("PreferenceType"),
            Preference.PreferenceValue.label("PreferenceValue")
        ).join(Faculty, Faculty.FacultyID == Preference.FacultyID).all()



# # Example usage
# if __name__ == "__main__":
#     # Replace 'sqlite:///test.db' with your actual database URL
#     session = setup_database('sqlite:///test.db')
#     add_faculty(session, name="Dr. Smith", class1="Math 101", preference="Morning")
#     add_classroom(session, room_id="SH101", building="Science Hall", room="101")
#     add_course(session, course_id= "Bio 101", name="Biology 101", req_room=1)
#     add_timeslot(session, days="MW", start_time="10:00 AM")
#     add_conflict(session, severity="H", conflict_type="Room")
#     add_schedule(session, timeslot=1, faculty=1, course=1, classroom=1, conflict=1)