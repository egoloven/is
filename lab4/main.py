def is_safe(assignment, subject, period, teacher_availability, teachers):
    if period in assignment.values():
        return False

    if period not in teacher_availability[teachers[subject]]:
        return False

    return True

def timetable_schedule_util(assignment, subjects, periods, teacher_availability, teachers):
    if len(assignment) == len(subjects):
        return assignment

    for subject in subjects:
        if subject not in assignment:
            for period in periods:
                if is_safe(assignment, subject, period, teacher_availability, teachers):
                    assignment[subject] = period
                    result = timetable_schedule_util(assignment, subjects, periods, teacher_availability, teachers)
                    if result:
                        return result
                    del assignment[subject]

    return None

def timetable_schedule(subjects, periods, teachers, teacher_availability):
    return timetable_schedule_util({}, subjects, periods, teacher_availability, teachers)

# Define the subjects, periods, teachers, and teacher availability
subjects = ["Math", "Science", "English", "History", "PE"]
periods = [1, 2, 3, 4, 5]

teachers = {
    "Math": "Mr. Smith",
    "Science": "Mrs. Johnson",
    "English": "Ms. Brown",
    "History": "Mr. Davis",
    "PE": "Coach Martin"
}

teacher_availability = {
    "Mr. Smith": [1, 2, 4, 5],
    "Mrs. Johnson": [2, 3, 4, 5],
    "Ms. Brown": [1, 3, 4, 5],
    "Mr. Davis": [1, 2, 3, 4],
    "Coach Martin": [1, 2, 3, 5]
}

# Get the timetable schedule
solution = timetable_schedule(subjects, periods, teachers, teacher_availability)

# Print the timetable solution
if solution:
    print("Timetable Solution:")
    for subject, period in solution.items():
        print(f"{subject}: Period {period}")
else:
    print("No timetable solution found.")
