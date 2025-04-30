#-------------------------gpa_calculator.py--------------------------
#
# Calculates the GPA for individual sections.
# Groups sections and calculates group GPAs.
# @Author: Mike Giles
#
#--------------------------------------------------------------------
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

# Calculate GPA averages from raw dataframe
def calcGPA(df, course_dict):
    temp                    = df.copy()
    
    temp['GPA']             = temp['Grade'].apply(grade_to_gpa)

    result = []

    for course, sections in course_dict.items():
        course_df           = temp[(temp['Class'] == course) & (temp['Section'].isin(sections))]

        course_avg          = course_df['GPA'].mean()
        result.append([course, 'Course Average', course_avg])

        for section in sections:
            section_df      = course_df[course_df['Section'] == section]
            section_avg     = section_df['GPA'].mean()
            result.append([course, section, section_avg])

    result_df = pd.DataFrame(result, columns=['Class', 'Section', 'Average'])

    return result_df

# Creates graph for GPA dataframe
def createGPAGraph(df):
    # Prepare data containers
    x_labels        = []
    heights         = []
    colors          = []
    class_labels    = []

    color_cycle     = itertools.cycle(plt.cm.tab10.colors)

    for course in df['Class'].unique():
        course_df = df[df['Class'] == course]
        course_df_sorted = pd.concat([
            course_df[course_df['Section'] == 'Course Average'],
            course_df[course_df['Section'] != 'Course Average']
        ])

        color = next(color_cycle)

        for _, row in course_df_sorted.iterrows():
            label = f"{course}\n{row['Section']}" if row['Section'] != 'Course Average' else f"{course}\nAvg"
            wrapped_label = '\n'.join(textwrap.wrap(label, width=12))
            x_labels.append(wrapped_label)
            heights.append(row['Average'])
            colors.append(color)
            class_labels.append(course)


    fig_width   = max(12, len(x_labels) * 0.6)
    fig, ax     = plt.subplots(figsize=(fig_width, 6))

    bars        = ax.bar(x_labels, heights, color=colors, alpha=0.85)

    # Format chart
    ax.set_title('GPA Averages by Course and Section')
    ax.set_ylabel('Average GPA')
    ax.set_ylim(0, 4)
    ax.set_xlabel('Course and Section')
    ax.tick_params(axis='x', rotation=75)
    ax.grid(axis='y', linestyle='--', alpha=0.5)

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

# Calculate Grade Distribution of students
def calcGradeDistribution(df, course_dict):
    temp                = df.copy()

    temp['Valid GPA']   = temp['Grade'].apply(grade_to_gpa)

    temp                = temp[temp['Valid GPA'].notnull()]

    result              = []

    for course, sections in course_dict.items():
        course_df = temp[(temp['Class'] == course) & (temp['Section'].isin(sections))]

        for section in sections:
            section_df = course_df[course_df['Section'] == section]

            grade_counts = section_df['Grade'].value_counts().sort_index()

            for grade, count in grade_counts.items():
                result.append([course, section, grade, count])

    result_df = pd.DataFrame(result, columns=['Class', 'Section', 'Grade', 'Student Count'])

    return result_df

# Creates graph for Students Distribution dataframe
def createGradeDistributionGraph(df):
    # Define grade order
    grade_order     = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D', 'D-', 'F']
    classes         = df['Class'].unique()
    class_colors    = dict(zip(classes, itertools.islice(itertools.cycle(plt.cm.tab10.colors), len(classes))))

    pivot_df        = df.pivot_table(index='Grade', columns='Class', values='Student Count', aggfunc='sum').reindex(grade_order).fillna(0)

    bar_width       = 0.35
    x               = range(len(grade_order))
    fig, ax         = plt.subplots(figsize=(12, 6))

    total_classes   = len(classes)
    offsets         = [(i - total_classes / 2) * bar_width for i in range(total_classes)]

    for offset, cls in zip(offsets, classes):
        ax.bar(
            [i + offset for i in x],
            pivot_df[cls],
            width=bar_width,
            label=cls,
            color=class_colors[cls],
            edgecolor='black'
        )

    # Formatting
    ax.set_title('Grade Distribution by Class')
    ax.set_xlabel('Letter Grade')
    ax.set_ylabel('Number of Students')
    ax.set_xticks(list(x))
    ax.set_xticklabels(grade_order)
    ax.legend(title="Class")
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    fig.tight_layout()
    plt.close(fig)
    return fig