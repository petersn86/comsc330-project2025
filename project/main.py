import parser
import build_gui
import gpa_calculator
import student_list
import pandas   as    pd
from build_gui import Tk, messagebox, defaultdict

window_start            = Tk()
frame_1                 = build_gui.buildFrame(window_start)
build_gui.folderPath    = ''
sections                = {}

window_start.geometry("800x600")
window_start.configure(bg="#FFFFFF")
window_start.resizable(False, False)
frame_1.pack(fill="both", expand=True)
build_gui.frameFill_START(frame_1)

window_start.mainloop()

window_main             = Tk()
frame_2                 = build_gui.buildFrame(window_main)

window_main.geometry("1080x740")
window_main.configure(bg="#FFFFFF")
frame_2.pack(fill="both", expand=True)
build_gui.frameFill_PRIMARY(frame_2)

def runSelect(*args):
    global df
    global sections
    build_gui.unselectAll()
    classes                     = parser.extractClasses(build_gui.folderPath, frame_2.dropdown_var.get())
    sections                    = parser.extractSections(build_gui.folderPath, classes)
    df                          = parser.createDataFrame(build_gui.folderPath, sections)

    build_gui.showGroups(frame_2.image_frame, sections)
    build_gui.showDataframe(frame_2, df)

def runZTest():
    selected_count = sum(var.get() for course in build_gui.section_vars for var in build_gui.section_vars[course])
    if selected_count != 1:
        if selected_count == 0:
            messagebox.showinfo("Stop!", "Please Select One of the Sections for this Action")
            return
        else:
            messagebox.showinfo("Stop!", "You Can Only Select One Section for this Action")
            return
    messagebox.showinfo("Continue")

def runGPACalc():
    build_gui.ticked_courses    = []
    build_gui.ticked_sections   = {}
    selected_count = sum(var.get() for course in build_gui.section_vars for var in build_gui.section_vars[course])
    if selected_count == 0:
        messagebox.showinfo("Stop!", "Please Select One of the Sections for this Action")
        return
    build_gui.checkTicked(sections)
    gpa_df = gpa_calculator.calcGPA(df, build_gui.ticked_sections)
    build_gui.showDataframe(frame_2, gpa_df)

def runStudentList():
    build_gui.ticked_courses    = []
    build_gui.ticked_sections   = {}
    selected_count = sum(var.get() for course in build_gui.section_vars for var in build_gui.section_vars[course])
    if selected_count == 0:
            messagebox.showinfo("Stop!", "Please Select One of the Sections for this Action")
            return
    build_gui.checkTicked(sections)
    good_df, work_df = student_list.classify_students(df, build_gui.ticked_sections)
    concat = pd.concat([good_df, work_df], ignore_index=True)
    build_gui.showDataframe(frame_2, concat)

def runAction(*args):
    if   frame_2.dropdown_var_2.get() == "Z-Test":
        runZTest()
    elif frame_2.dropdown_var_2.get() == "Display-GPA":
        runGPACalc()
    elif frame_2.dropdown_var_2.get() == "Student-List":
        runStudentList()

frame_2.dropdown_var.trace("w", runSelect)

frame_2.dropdown_var_2.trace("w", runAction)

if build_gui.state["state"] == True: 
    window_main.mainloop()

build_gui.checkTicked(sections)
print(build_gui.ticked_sections)