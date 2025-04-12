""""
Purpose:
 - Checks if section/group GPA differences are statistically significant.
 - Uses z-tests for comparisons.

Functions in this program:
 Grade Conversion: The grade_to_gpa function maps letter grades to GPA ints
 Data Extraction: get_section_gpa_data extracts GPA data for a specific section from the DataFrame.
 Z-Test Calculation: perform_z_test computes the z-score and p-value between two GPA samples.
 Significance Check: is_significant_difference uses the above functions to check if the GPA difference between two sects
"""

import numpy as np
from scipy import stats
import pandas as pd


def grade_to_gpa(grade):    #Converts a letter to GPA 
    conversion = {
        'A': (4.00),
        'A-': (3.67),
        'B+': (3.33),
        'B': (3.00),
        'B-': (2.67),
        'C+': (2.33),
        'C': (2.00),
        'C-': (1.67),
        'D+': (1.33),
        'D': (1.00),
        'D-': (0.67),
        'F': (0.00)
    }
    return conversion.get(grade.strip(), 0.0)   # not found = 0


def get_section(df, section_name):     # Extracts GPA data for section from the dataframe
    
    section_df = df[df['Section'] == section_name]      # Placeholder sectionname
    gpas = section_df['Grade'].apply(grade_to_gpa).tolist()
    return gpas



def perform_z_test(num1, num2):    #Performs z-test 

    mean1 = np.mean(num1)
    mean2 = np.mean(num2)
    
    std1 = np.std(num1, ddof=1)
    std2 = np.std(num2, ddof=1)
    
    n1 = len(num1) 
    n2 = len(num2)
    
    se = np.sqrt((std1**2 / n1) + (std2**2 / n2))   # standard error calculation
    
    if se == 0:
        return (0.0, 1.0)   # handling zero error
    
    # z score calculation
    z = (mean1 - mean2) / se     
            
    # p value calculation
    p_value = 2 * (1 - stats.norm.cdf(abs(z))) 
    
    return z, p_value

def is_significant_difference(df, section1, section2, significance=0.05):
    # Finds if the GPA difference between two sections is statistically significant 
    
    gpas1 = get_section(df, section1)
    gpas2 = get_section(df, section2)
    
    # Empty data error handling
    if not gpas1 or not gpas2:
        print(f"ERROR: Section(s) have no data...")
        return False
    
    #performing z test
    z_score, p_value = perform_z_test(gpas1, gpas2)    
    print(f"Z-Score: {z_score}, P-Value: {p_value:.4f}")
    
    if p_value < significance:
        return True

    else: 
        print("Value is not significant.")
        return False
    
def calculateZScores(df, course_dict, gpa_df):
    result = []

    for course, sections in course_dict.items():
        course_df = gpa_df[gpa_df['Class'] == course]
        
        course_avg = course_df['Average'].mean()
        course_std = course_df['Average'].std()

        result.append([course, 'Course Average', course_avg, None])

        for section in sections:
            section_df = course_df[course_df['Section'] == section]
            
            section_avg = section_df['Average'].values[0]
            
            if course_std > 0:
                section_zscore = (section_avg - course_avg) / course_std
            else:
                section_zscore = None

            result.append([course, section, section_avg, section_zscore])

    result_df = pd.DataFrame(result, columns=['Class', 'Section', 'GPA', 'Z-Score'])
    
    return result_df
