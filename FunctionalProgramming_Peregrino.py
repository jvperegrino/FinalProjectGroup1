from functools import reduce

students = [
    {
        "id": "2026-001", "name": "Juan Dela Cruz", "program": "BSCS", "year": 4,
        "grades": [85, 91, 88, 76, 92], "attendance": 94, "project": 89
    },
    {
        "id": "2026-002", "name": "Maria Santos", "program": "BSIT", "year": 4,
        "grades": [92, 95, 90, 88, 94], "attendance": 98, "project": 96
    },
    {
        "id": "2026-003", "name": "Pedro Reyes", "program": "BSCS", "year": 3,
        "grades": [72, 78, 75, 81, 79], "attendance": 85, "project": 80
    },
    {
        "id": "2026-004", "name": "Ana Garcia", "program": "BSIS", "year": 4,
        "grades": [89, 94, 91, 95, 90], "attendance": 97, "project": 93
    },
    {
        "id": "2026-005", "name": "Luis Mendoza", "program": "BSCS", "year": 2,
        "grades": [68, 74, 70, 73, 71], "attendance": 79, "project": 75
    },
    {
        "id": "2026-006", "name": "Sofia Ramos", "program": "BSIT", "year": 3,
        "grades": [84, 87, 90, 86, 89], "attendance": 93, "project": 91
    },
    {
        "id": "2026-007", "name": "Mark Villanueva", "program": "BSIS", "year": 2,
        "grades": [77, 82, 79, 75, 80], "attendance": 88, "project": 84
    },
    {
        "id": "2026-008", "name": "Liza Fernandez", "program": "BSCS", "year": 4,
        "grades": [93, 89, 96, 91, 94], "attendance": 99, "project": 95
    }
]

#function to get average grade
#reduce() sum all numerical value inside grade list
def average_grades(grades):
    total = reduce(lambda x, y: x + y, grades)
    return total / len(grades)
#reduce add first 2 numbers in grades, adds it to 3rd number, and repeat until all grades are summed

#function to get student rate
def stud_rate(rate):
    if 95 <= rate <= 100:
        return "Outstanding"
    elif 90 <= rate < 95:
        return "Excellent"
    elif 85 <= rate < 90:
        return "Very Good"
    elif 80 <= rate < 85:
        return "Good"
    elif 75 <= rate < 79.99:
        return "Satisfactory"
    else:
        return "Needs Improvement"
#stud_rate(if_passed_or_not)

#one function's output will be input for the next function
def compose(*functions):
    return lambda data: reduce(lambda pipeline2, pipeline1: pipeline1(pipeline2), functions, data)
#chains multiple functions together into 1 function pipeline
#data variable waits for input data from other functions; initializer in reduce()
#pipeline1 = next function
#pipeline2 = accumulator


per_stud_info = lambda s: {
    "Student Name": s["name"],
    "Program": s["program"],
    "Average Grade": round(average_grades(s["grades"]), 2),
    "Attendance": s["attendance"],
    "Project Score": s["project"]
}
#calculate final rating per student
per_stud_rate = lambda s: {
    **s,
    "Final rate": round((0.60 * s["Average Grade"]) + (0.20 * s["Attendance"]) + (0.20 * s["Project Score"]), 2)
}

per_stud_class = lambda s: {
    **s,
    "Classification": stud_rate(s["Final rate"])
}

per_stud_blueprint = compose(per_stud_info, per_stud_rate, per_stud_class)

#map transform student record
neat_stud_list = list(map(per_stud_blueprint, students))
per_stud_avg = list(map(lambda s: f"{s['name']}: {average_grades(s['grades']):.2f}", students))
hi_perf_studs = list(filter(
    lambda s: s["Final rate"] >= 90 and s["Attendance"] >= 90 and s["Project Score"] >= 90,
    neat_stud_list
))

stud_at_risk = lambda s: (
    (1 if s["Average Grade"] < 80 else 0) +
    (1 if s["Attendance"] < 85 else 0) +
    (1 if s["Project Score"] < 80 else 0)
) >= 2

neat_studs_risk = list(filter(stud_at_risk, neat_stud_list))


#sorted() to rank students
stud_rank = sorted(neat_stud_list, key=lambda s: s["Final rate"], reverse=True)

top_student = reduce(
    lambda a, b: a if a["Final rate"] > b["Final rate"] else b,
    neat_stud_list
)
top_student_block = f"Top Student: {top_student['Student Name']} ({top_student['Program']}) - Final rate: {top_student['Final rate']:.2f}"


#using filter(), map(), and reduce() to calculate
all_rates = list(map(lambda s: s["Final rate"], neat_stud_list))

overall_avg = round(reduce(lambda x, y: x + y, all_rates) / len(all_rates), 2)
highest_rate = reduce(lambda a, b: a if a > b else b, all_rates)
lowest_rate = reduce(lambda a, b: a if a < b else b, all_rates)

passed_students = list(filter(lambda s: s["Final rate"] >= 75, neat_stud_list))
failed_students = list(filter(lambda s: s["Final rate"] < 75, neat_stud_list))

num_passed = len(passed_students)
num_failed = len(failed_students)

global_metrics_block = (
    f"Overall Average Rating:  {overall_avg:.2f}\n"
    f"Highest Final Rating:    {highest_rate:.2f}\n"
    f"Lowest Final Rating:     {lowest_rate:.2f}\n"
    f"Students Passed (>= 75): {num_passed}\n"
    f"Students Failed (< 75):  {num_failed}"
)


def per_stud_metrics(dataset):
    if not dataset:
        return {"count": 0, "avg": 0.0, "max": 0.0, "min": 0.0}
    rates = list(map(lambda s: s["Final rate"], dataset))
    total_rate = reduce(lambda x, y: x + y, rates)
    max_rate = reduce(lambda a, b: a if a > b else b, rates)
    min_rate = reduce(lambda a, b: a if a < b else b, rates)
    
    return {
        "count": len(dataset),
        "avg": round(total_rate / len(dataset), 2),
        "max": max_rate,
        "min": min_rate
    }

bscs_studs = list(filter(lambda s: s["Program"] == "BSCS", neat_stud_list))
bsit_studs = list(filter(lambda s: s["Program"] == "BSIT", neat_stud_list))
bsis_studs = list(filter(lambda s: s["Program"] == "BSIS", neat_stud_list))

metrics_bscs = per_stud_metrics(bscs_studs)
metrics_bsit = per_stud_metrics(bsit_studs)
metrics_bsis = per_stud_metrics(bsis_studs)


neat_show_studs = lambda s: (
    f"Name: {s['Student Name']}\n"
    f"Program: {s['Program']}\n"
    f"Average Grade: {s['Average Grade']:.2f}\n"
    f"Attendance: {s['Attendance']}\n"
    f"Project: {s['Project Score']}\n"
    f"Final rate: {s['Final rate']:.2f}\n"
    f"Classification: {s['Classification']}\n"
    f"----------------------------------------------------------------------"
)
per_stud_block = "\n".join(map(neat_show_studs, neat_stud_list))

rank_row = lambda item: f"{item[0] + 1}. {item[1]['Student Name']:<25} - {item[1]['Final rate']:.2f}"
per_stud_rank = "\n".join(map(rank_row, enumerate(stud_rank)))

studs_row = lambda s: f"- {s['Student Name']} ({s['Program']}) - Final rate: {s['Final rate']:.2f}"
hi_perf_studs_block = "\n".join(map(studs_row, hi_perf_studs)) if hi_perf_studs else "None"
per_stud_risk = "\n".join(map(studs_row, neat_studs_risk)) if neat_studs_risk else "None"

#program analytics
prog_ana = lambda name, m: (
    f"{name}\n"
    f"Students: {m['count']}\n"
    f"Average: {m['avg']:.2f}\n"
    f"Highest: {m['max']:.2f}\n"
    f"Lowest: {m['min']:.2f}"
)


print("--- TASK 1 Nested List Processing ---")
print("\n".join(per_stud_avg))
print("\n" + "="*70 + "\n")

final_output = (
    f"======================================================================\n"
    f"                  FUNCTIONAL STUDENT PERFORMANCE ANALYZER             \n"
    f"======================================================================\n\n"
    f"STUDENT PERFORMANCE\n"
    f"----------------------------------------------------------------------\n"
    f"{per_stud_block}\n\n"
    f"======================================================================\n"
    f"                           OVERALL METRICS                            \n"
    f"======================================================================\n"
    f"{global_metrics_block}\n\n"
    f"======================================================================\n"
    f"                           TOP STUDENT                                \n"
    f"======================================================================\n"
    f"{top_student_block}\n\n"
    f"======================================================================\n"
    f"                           STUDENT RANKING                            \n"
    f"======================================================================\n"
    f"{per_stud_rank}\n\n"
    f"----------------------------------------------------------------------\n"
    f"                           HIGH PERFORMERS                            \n"
    f"======================================================================\n"
    f"{hi_perf_studs_block}\n\n"
    f"----------------------------------------------------------------------\n"
    f"                          AT-RISK STUDENTS                            \n"
    f"======================================================================\n"
    f"{per_stud_risk}\n\n"
    f"----------------------------------------------------------------------\n"
    f"                           PROGRAM ANALYSIS                           \n"
    f"----------------------------------------------------------------------\n"
    f"{prog_ana('BSCS', metrics_bscs)}\n\n"
    f"{prog_ana('BSIT', metrics_bsit)}\n\n"
    f"{prog_ana('BSIS', metrics_bsis)}"
)

print(final_output)
