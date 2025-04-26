#
# Calculates the GPA for individual sections.
# Groups sections and calculates group GPAs.
# @Author: Mike Giles
#

import pandas as pd
import matplotlib.pyplot as plt
import itertools
import textwrap

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
        course_df = temp[(temp['Class'] == course) & (temp['Section'].isin(sections))]

        course_avg = course_df['GPA'].mean()
        result.append([course, 'Course Average', course_avg])

        for section in sections:
            section_df = course_df[course_df['Section'] == section]
            section_avg = section_df['GPA'].mean()
            result.append([course, section, section_avg])

    result_df = pd.DataFrame(result, columns=['Class', 'Section', 'Average'])

    return result_df

def createGPAGraph(df):
    # Prepare data containers
    x_labels = []
    heights = []
    colors = []
    class_labels = []

    # Generate colors dynamically
    color_cycle = itertools.cycle(plt.cm.tab10.colors)

    # Build ordered data
    for course in df['Class'].unique():
        course_df = df[df['Class'] == course]
        course_df_sorted = pd.concat([
            course_df[course_df['Section'] == 'Course Average'],
            course_df[course_df['Section'] != 'Course Average']
        ])

        color = next(color_cycle)

        for _, row in course_df_sorted.iterrows():
            label = f"{course}\n{row['Section']}" if row['Section'] != 'Course Average' else f"{course}\nAvg"
            # Wrap label to max 12 characters per line
            wrapped_label = '\n'.join(textwrap.wrap(label, width=12))
            x_labels.append(wrapped_label)
            heights.append(row['Average'])
            colors.append(color)
            class_labels.append(course)

    # Dynamically adjust figure width based on number of labels
    fig_width = max(12, len(x_labels) * 0.6)
    fig, ax = plt.subplots(figsize=(fig_width, 6))

    # Create bar plot
    bars = ax.bar(x_labels, heights, color=colors, alpha=0.85)

    # Format chart
    ax.set_title('GPA Averages by Course and Section')
    ax.set_ylabel('Average GPA')
    ax.set_ylim(0, 4)
    ax.set_xlabel('Course and Section')
    ax.tick_params(axis='x', rotation=75)
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    # Create legend using unique class labels and colors
    unique_classes = list(df['Class'].unique())
    legend_patches = [
        plt.Line2D([0], [0], marker='s', color='w',
                   label=cls, markerfacecolor=col, markersize=10)
        for cls, col in zip(unique_classes, itertools.islice(itertools.cycle(plt.cm.tab10.colors), len(unique_classes)))
    ]
    ax.legend(handles=legend_patches, title="Class")

    fig.tight_layout()
    plt.close(fig)
    return fig