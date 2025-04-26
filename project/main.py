import parser
import build_gui
import gpa_calculator
import student_list
import significance_test
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

window_start.title("Welcome!")
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
    build_gui.clearFrame(frame_2.graph_frame)
    build_gui.shakeFrame(frame_2)

def runGPACalc():
    build_gui.ticked_courses    = []
    build_gui.ticked_sections   = {}
    selected_count = sum(var.get() for course in build_gui.section_vars for var in build_gui.section_vars[course])
    if selected_count == 0:
        messagebox.showinfo("Stop!", "Please Select One of the Sections for this Action")
        return
    build_gui.checkTicked(sections)
    gpa_df = gpa_calculator.calcGPA(df, build_gui.ticked_sections)
    fig    = gpa_calculator.createGPAGraph(gpa_df)
    build_gui.showDataframe(frame_2, gpa_df)
    build_gui.showGraph(frame_2.graph_frame, fig)
    build_gui.shakeFrame(frame_2)

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
    final  = student_list.merge_duplicate_students(concat)
    fig    = student_list.plotStudentCharts(final)
    build_gui.showDataframe(frame_2, final)
    build_gui.shakeFrame(frame_2)
    build_gui.showGraph(frame_2.graph_frame, fig)

def runZTest():
    build_gui.ticked_courses    = []
    build_gui.ticked_sections   = {}
    selected_count = sum(var.get() for course in build_gui.section_vars for var in build_gui.section_vars[course])
    if selected_count == 0:
        messagebox.showinfo("Stop!", "Please Select One of the Sections for this Action")
        return
    build_gui.checkTicked(sections)
    gpa_df = gpa_calculator.calcGPA(df, build_gui.ticked_sections)
    z_df   = significance_test.calculateZScores(df, build_gui.ticked_sections, gpa_df)
    fig    = significance_test.createZScoreGraph(z_df)
    build_gui.showDataframe(frame_2, z_df)
    build_gui.showGraph(frame_2.graph_frame, fig)
    build_gui.shakeFrame(frame_2)
    

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
    window_main.title("GPA Analyzer")
    window_main.mainloop()
