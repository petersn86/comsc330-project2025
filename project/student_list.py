#
# Identifies students who qualify for the Good or Work list.
# Tracks historical data to determine past appearances.
#

import pandas as pd

def classifiy_students(df):
    # define grade categories
    good_grades = {'A', 'A-'}
    work_grades = {'D+', 'D', 'D-', 'F'}

    # Filter students based on their grades into lists
    good_list = df[df['Grade'].isin(good_grades)]['Name'].tolist()
    work_list = df[df['Grade'].isin(good_grades)]['Name'].tolist()

    # Return the lists
    return good_list, work_list

