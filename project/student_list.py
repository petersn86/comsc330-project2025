#---------------------------student_list.py--------------------------
#
# Identifies students who qualify for the Good or Work list.
# Tracks historical data to determine past appearances.
# @Author: Emma Bolduc
#
#--------------------------------------------------------------------
import pandas as pd
import matplotlib.pyplot as plt
import itertools
import textwrap
import math

# Create Good and Work lists from raw data frame
def classify_students(df, sections_dict):
    good_grades = {'A', 'A-'}
    work_grades = {'D+', 'D', 'D-', 'F'}
    
    good_list = []
    work_list = []
    
    for course, sections in sections_dict.items():
        filtered_df = df[df['Section'].isin(sections)]
        
        for _, row in filtered_df[filtered_df['Grade'].isin(good_grades)].iterrows():
            good_list.append((row['Name'], row['ID'], row['Grade'], course))
        
        for _, row in filtered_df[filtered_df['Grade'].isin(work_grades)].iterrows():
            work_list.append((row['Name'], row['ID'], row['Grade'], course))

    good_df = pd.DataFrame(good_list, columns=['Name', 'ID',  'Grade', 'Class'])
    work_df = pd.DataFrame(work_list, columns=['Name', 'ID',  'Grade', 'Class'])

    good_df['Category'] = 'Good'
    work_df['Category'] = 'Work'

    return good_df, work_df

# Find duplicate students
def merge_duplicate_students(df):
    grouped = df.groupby('ID')

    good_list = []
    work_list = []

    for student_id, group in grouped:
        categories = set(group['Category'])

        # Skip students in multiple categories
        if len(categories) > 1:
            continue

        name = group.iloc[0]['Name']
        category = group.iloc[0]['Category']
        grade = group.iloc[0]['Grade']  # You could also choose the "best" grade here
        classes = ', '.join(sorted(set(group['Class'])))

        row = {
            'Name': name,
            'ID': student_id,
            'Grade': grade,
            'Class': classes,
            'Category': category
        }

        if category == 'Good':
            good_list.append(row)
        else:
            work_list.append(row)

    # Combine and return in order
    good_df = pd.DataFrame(good_list)
    work_df = pd.DataFrame(work_list)
    return pd.concat([good_df, work_df], ignore_index=True)

# Creates graph for Students List dataframe
def plotStudentCharts(df):
    df = df.assign(Class=df['Class'].str.split(', ')).explode('Class')

    grouped = df.groupby(['Class', 'Category']).size().unstack(fill_value=0)

    num_classes = len(grouped)
    cols = 3
    rows = math.ceil(num_classes / cols)

    fig, axes = plt.subplots(rows, cols, figsize=(5 * cols, 5 * rows))
    axes = axes.flatten()

    for ax, (cls, counts) in zip(axes, grouped.iterrows()):
        labels = [f"{cat}: {count}" for cat, count in counts.items()]
        ax.pie(counts,
               labels=labels,
               startangle=90,
               labeldistance=1.1,
               colors=['#66bb6a', '#ef5350'])
        ax.set_title(f"{cls}", fontsize=12, y=1.05, ha='center')  # Center title above pie

    for ax in axes[num_classes:]:
        ax.axis('off')

    plt.tight_layout(rect=[0, 0, 1, 0.88])  # Increased space at the top
    fig.suptitle('Good vs Work Counts per Class', fontsize=16, ha='center')
    plt.close(fig)
    return fig