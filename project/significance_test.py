#------------------------significance_test.py------------------------
#
# Checks if section/group GPA differences are statistically significant
# Uses z-tests for comparisons.
# @Author: Eric Tech
#
#--------------------------------------------------------------------
import numpy as np
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt
import itertools
import textwrap

# Converts letter grade to raw GPA
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
    
# Calculates z-score from raw dataframe & GPA dataframe
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

# Creates graph for z-score dataframe
def createZScoreGraph(df):
    df = df.dropna(subset=["Z-Score"])

    x_labels = []
    z_scores = []
    colors = []

    color_cycle = itertools.cycle(plt.cm.tab10.colors)
    class_colors = {}

    for _, row in df.iterrows():
        course = row["Class"]
        section = row["Section"]
        z = row["Z-Score"]

        label = '\n'.join(textwrap.wrap(f"{course}\n{section}", 12))
        x_labels.append(label)
        z_scores.append(z)

        if course not in class_colors:
            class_colors[course] = next(color_cycle)
        colors.append(class_colors[course])

    fig_width = max(12, len(x_labels) * 0.6)
    fig, ax = plt.subplots(figsize=(fig_width, 6))

    bars = ax.bar(x_labels, z_scores, color=colors, alpha=0.85)

    ax.axhline(0, color='black', linestyle='--', linewidth=1)

    ax.set_title('Z-Scores by Course Section')
    ax.set_ylabel('Z-Score')
    ax.set_xlabel('Course and Section')
    ax.tick_params(axis='x', rotation=75)
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    legend_patches = [
        plt.Line2D([0], [0], marker='s', color='w',
                   label=cls, markerfacecolor=col, markersize=10)
        for cls, col in class_colors.items()
    ]
    ax.legend(handles=legend_patches, title="Class")

    fig.tight_layout()
    plt.close(fig)
    return fig
