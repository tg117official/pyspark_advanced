# Comprehensive Intermediate-Level Exercise

# Problem: Process student records and identify scholarship candidates.

def calculate_totals_and_averages(students):
    """Calculate total and average marks for each student."""
    for student in students:
        total = sum(student['marks'].values())
        average = total / len(student['marks'])
        student['total'] = total
        student['average'] = average
    return students


def find_scholarship_candidates(students):
    """Identify students who qualify for a scholarship."""
    candidates = []
    for student in students:
        if student['average'] >= 85 and student['attendance'] >= 90:
            candidates.append(student)
    return candidates


def sort_students_by_total(students):
    """Sort students by total marks in descending order."""
    return sorted(students, key=lambda x: x['total'], reverse=True)


if __name__ == "__main__":
    import pdb

    pdb.set_trace()  # Start debugging here

    # List of student records
    student_records = [
        {"name": "Alice", "marks": {"math": 90, "science": 85, "english": 88}, "attendance": 95},
        {"name": "Bob", "marks": {"math": 78, "science": 80, "english": 79}, "attendance": 85},
        {"name": "Charlie", "marks": {"math": 92, "science": 89, "english": 91}, "attendance": 98},
        {"name": "Diana", "marks": {"math": 88, "science": 76, "english": 90}, "attendance": 93},
    ]

    # Step 1: Calculate totals and averages
    student_records = calculate_totals_and_averages(student_records)

    # Step 2: Find scholarship candidates
    scholarship_candidates = find_scholarship_candidates(student_records)

    # Step 3: Sort students by total marks
    sorted_students = sort_students_by_total(student_records)

    # Output results
    print("Processed Student Records:")
    for student in sorted_students:
        print(
            f"{student['name']}: Total={student['total']}, Average={student['average']:.2f}, Attendance={student['attendance']}%")

    print("\nScholarship Candidates:")
    for candidate in scholarship_candidates:
        print(f"{candidate['name']}: Average={candidate['average']:.2f}, Attendance={candidate['attendance']}%")
