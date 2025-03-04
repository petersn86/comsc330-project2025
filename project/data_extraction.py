#
# Loads student grade data
# Cleans and structures the data for further analysis.
#

import pandas as pd
import csv
from collections import defaultdict

# Variables
dir         = 'test_data\\'                                                         # directory path                        (will be dynamically selected later)
semester    = 'SPRING25'                                                            # semester                              (will be dynamically selected later)

# Open RUN file and extract classes
def extractClasses():
    classes = []
    with open(dir + semester + '.RUN', 'r', encoding= "utf-8") as file:
        next(file)
        for line in file:
            classes.append(line.strip())
    file.close()
    return classes

# Open GRP files and extract sections
def extractSections(classes):
    sections = defaultdict(list)
    for i in range(len(classes)):
        with open(dir + classes[i], 'r', encoding ="utf-8") as file:
            next(file)
            for line in file:
                sections[(classes[i])[:-4]].append(line.strip())
    file.close()
    return sections

# Open SEC files and store data into dataframes
def createDataFrame(sections):
    df = pd.DataFrame(columns=["Name", "ID", "Class", "Section", "Grade"]) 
    for key in sections.keys():
        for sec_files in sections[key]:
            with open(dir + sec_files, 'r', encoding= "utf-8") as file:
                next(file)
                reader = csv.reader(file)
                for line in file:
                    parts           = line.replace('"','').split(',')
                    name            = parts[0].strip() + ', ' + parts[1].strip()
                    studentId       = parts[2].strip()
                    grade           = parts[3].strip()
                    df.loc[len(df)] = [name, studentId, key, sec_files[:-4], grade]
    file.close()
    return df