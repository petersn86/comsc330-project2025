#
# Identifies students who qualify for the Good or Work list.
# Tracks historical data to determine past appearances.
#

import pandas as pd

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

