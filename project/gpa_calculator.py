#
# Calculates the GPA for individual sections.
# Groups sections and calculates group GPAs.
#

import pandas as pd

def grade_to_gpa(grade):
    conversion = {
        'A': 4.00,
        'A-': 3.67,
        'B+': 3.33,
        'B': 3.00,
        'B-': 2.67,
        'C+': 2.33,
        'C': 2.00,
        'C-': 1.67,
        'D+': 1.33,
        'D': 1.00,
        'D-': 0.67,
        'F': 0.00
    }

    if grade.strip() in ['I', 'W', 'P', 'NP']:
        return None

    return conversion.get(grade.strip(), None)

def calcGPA(df, course_dict):
    temp = df.copy()
    
    temp['GPA'] = temp['Grade'].apply(grade_to_gpa)

    result = []

    for course, sections in course_dict.items():
        course_df = temp[temp['Class'] == course]

        course_avg = course_df['GPA'].mean()
        result.append([course, 'Course Average', course_avg])

        for section in sections:
            section_df = course_df[course_df['Section'] == section]
            section_avg = section_df['GPA'].mean()
            result.append([course, section, section_avg])

    result_df = pd.DataFrame(result, columns=['Course', 'Section', 'Average'])

    return result_df