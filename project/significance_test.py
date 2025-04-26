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
import matplotlib.pyplot as plt
import itertools
import textwrap

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

def createZScoreGraph(df):
    # Drop rows where Z-Score is NaN (e.g., Course Averages)
    df = df.dropna(subset=["Z-Score"])

    # Prepare labels and data
    x_labels = []
    z_scores = []
    colors = []

    color_cycle = itertools.cycle(plt.cm.tab10.colors)
    class_colors = {}

    for _, row in df.iterrows():
        course = row["Class"]
        section = row["Section"]
        z = row["Z-Score"]

        # Wrap label text for readability
        label = '\n'.join(textwrap.wrap(f"{course}\n{section}", 12))
        x_labels.append(label)
        z_scores.append(z)

        # Assign consistent color per course
        if course not in class_colors:
            class_colors[course] = next(color_cycle)
        colors.append(class_colors[course])

    # Dynamically adjust width
    fig_width = max(12, len(x_labels) * 0.6)
    fig, ax = plt.subplots(figsize=(fig_width, 6))

    # Bar chart
    bars = ax.bar(x_labels, z_scores, color=colors, alpha=0.85)

    # Add horizontal line at Z = 0
    ax.axhline(0, color='black', linestyle='--', linewidth=1)

    # Format plot
    ax.set_title('Z-Scores by Course Section')
    ax.set_ylabel('Z-Score')
    ax.set_xlabel('Course and Section')
    ax.tick_params(axis='x', rotation=75)
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    # Legend
    legend_patches = [
        plt.Line2D([0], [0], marker='s', color='w',
                   label=cls, markerfacecolor=col, markersize=10)
        for cls, col in class_colors.items()
    ]
    ax.legend(handles=legend_patches, title="Class")

    fig.tight_layout()
    plt.close(fig)
    return fig
