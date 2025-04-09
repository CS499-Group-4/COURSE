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

    
    professor = [ "Dr. Wilcox", "Dr. Morris", "Dr. Clarke", "Dr. Mcguire", "Dr. Garcia", 
                      "Dr. French", "Dr. Sawyer", "Dr. Richard", "Dr. Case", "Dr. Best", 
                      "Dr. Carlson", "Dr. Wiley", "Dr. Baird", "Dr. Branch", "Dr. Pearson", 
                      "Dr. Wade", "Dr. Barr", "Dr. Pollard", "Dr. Grimes", "Dr. Deleon", 
                      "Dr. Fred Wilcox", "Dr. Cora", "Dr. Keiran", "Dr. Christian", "Dr. Will", 
                      "Dr. Christine", "Dr. Doris", "Dr. Rehan", "Dr. Sahar", "Dr. Aoife", 
                      "Dr. Dawid", "Dr. Alfie", "Dr. Astrid", "Dr. Taya", "Dr. Darcy", "Dr. Ollie", 
                      "Dr. Velma", "Dr. Sophia", "Dr. Alexandre", "Dr. Deleon", 
                      "Dr. Dude", "Dr. Broham", "Dr. Guy" ]
    
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
    with open('professors_classes.csv', mode='w', newline='') as file:
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
