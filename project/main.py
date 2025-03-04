#
# Calls the necessary modules in order.
# Provides user options for specific analyses.
#

import data_extraction

classes = data_extraction.extractClasses()
print(classes)

sections = data_extraction.extractSections(classes)
print(sections)

df = data_extraction.createDataFrame(sections)
print(df)