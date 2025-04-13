import csv
import random

class main:

    classNumber = [ "CS 118", "CS 279", "CS 211", "CS 108", "CS 275", "CS 170", "CS 149", "CS 203", "CS 117", "CS 121",
                    "CS 257", "CS 113", "CS 228", "CS 124", "CS 158", "CS 244", "CS 133", "CS 218", "CS 204", "CS 241",
                    "CS 297", "CS 199", "CS 232", "CS 242", "CS 216", "CS 259", "CS 186", "CS 265", "CS 135", "CS 264"]

    professor1 = [ "Dr. Fred Wilcox", "Dr. Cora Morris", "Dr. Keiran Clarke", "Dr. Christian Mcguire", "Dr. Will Garcia",
                "Dr. Christine French", "Dr. Doris Sawyer", "Dr. Rehan Richard", "Dr. Sahar Case", "Dr. Aoife Best",
                "Dr. Dawid Carlson", "Dr. Alfie Wiley", "Dr. Astrid Baird", "Dr. Taya Branch", "Dr. Darcy Pearson",
                "Dr. Ollie Wade", "Dr. Velma Barr", "Dr. Sophia Pollard", "Dr. Alexandre Grimes", "Dr. Maliha Deleon" ]


    professor = [ "Dr. Whitaker", "Dr. Hensley", "Dr. Caldwell", "Dr. Montoya", "Dr. Vasquez", 
    "Dr. Laramie", "Dr. Corbin", "Dr. Aldridge", "Dr. Fenwick", "Dr. Noble", 
    "Dr. Ashford", "Dr. Winslow", "Dr. Mercer", "Dr. Ellery", "Dr. Huxley", 
    "Dr. Boone", "Dr. Colby", "Dr. Langford", "Dr. Riggs", "Dr. Navarro", 
    "Dr. Ezra Whitaker", "Dr. Junia", "Dr. Eamon", "Dr. Silas", "Dr. Felix", 
    "Dr. Alina", "Dr. Greta", "Dr. Nabil", "Dr. Layla", "Dr. Saoirse", 
    "Dr. Milan", "Dr. Nico", "Dr. Ingrid", "Dr. Zaria", "Dr. Ronan", "Dr. Jett", 
    "Dr. Myrtle", "Dr. Leona", "Dr. Emilien", "Dr. Navarro", 
    "Dr. Zeke", "Dr. Kip", "Dr. Skip"]

    preferences = ["Evening classes only", "None", "Morning classes only",
                       "All Mon-Wed classes", "All Tue-Thur classes"]

    day = ["MW", "TR", "MWF", "MTWF", "F"]

    times = ["8:00 AM - 9:20 AM", "9:40 AM - 11:00 AM", "11:20 AM - 12:40 PM", 
             "1:00 PM - 2:20 PM", "2:40 PM - 4:00 PM", "4:20 PM - 5:40 PM",
             "6:00 PM - 7:20 PM", "7:40 PM - 9:00 PM"]

    rooms = ["101", "102", "103", "104", "105", "106", "107", "108", "109", "110"]


    prefData = []
    roomData = []
    # header = ["Professor", "Class 1", "Class 2", "Class 3", "Class 4", "Preferences"]
    # prefData.append(header)

    for _ in range(random.randint(0, 4)):
        selected_class = random.choice(classNumber)
        selected_room = random.choice(rooms)
        row1 = f"{selected_class} must be taught in Technology Hall Room {selected_room}"
        roomData.append([row1])


    for prof in professor:
        num_classes = random.randint(1, 4)
        selected_classes = random.sample(classNumber, num_classes)
        row = [prof] + selected_classes + [""] * (4 - num_classes)  # pad with empty strings
        row.append(random.choice(preferences))
        prefData.append(row)

    # Write data to a CSV file
    with open('testFile_CS.csv', mode='w', newline='') as file:
        writer = csv.writer(file)


        writer.writerow(["Location: Technology Hall"])
        writer.writerow(["Courses Offered:"])
        writer.writerow(["\n"])

        writer.writerow(["classNumber:"])
        for i in range(0, len(classNumber), 5):
            writer.writerow(classNumber[i:i+5])

        writer.writerow(["\n"])
        writer.writerow(["Classroom Preferences:"])
        writer.writerow(["\n"])
        writer.writerows(roomData)
        writer.writerow(["\n"])
        writer.writerow(["Faculty Assignments:"])
        writer.writerow(["\n"])
        #writer.writerow(["day:"] + day)
        #writer.writerow(["times:"] + times)

        writer.writerows(prefData)