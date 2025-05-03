#------------------------------main.py-------------------------------
#
# Driver file for software
# Connects modules into a single program
# @Author(s): Peter Nolan, Eric Tech, Emma Bolduc, Mike Giles
#
#--------------------------------------------------------------------
import parser
import build_gui
import gpa_calculator
import student_list
import significance_test
import pandas   as    pd
from build_gui import Tk, messagebox, defaultdict, os, tk


# Cache Handling------------------------------------------------------------
def getCacheDir():
    cache_dir       = os.path.join(os.path.expanduser("~"), ".gpa_analyzer_cache")
    os.makedirs(cache_dir, exist_ok=True)
    return cache_dir

def getCachePath(run_name: str) -> str:
    safe_name       = run_name.replace(" ", "_").replace("/", "_")
    return os.path.join(getCacheDir(), f"{safe_name}.parquet")

def cacheDataFrame(df: pd.DataFrame, run_name: str):
    df.to_parquet(getCachePath(run_name))

def loadDataframe(run_name: str)-> pd.DataFrame | None:
    path            = getCachePath(run_name)
    if os.path.exists(path):
        return pd.read_parquet(path)
    return None

def deleteCache(run_name: str):
    path            = getCachePath(run_name)
    if os.path.exists(path):
        os.remove(path)
        return True
    return False

def deleteCacheAll():
    cache_dir       = getCacheDir()
    for filename in os.listdir(cache_dir):
        if filename.endswith(".parquet"):
            file_path = os.path.join(cache_dir, filename)
            os.remove(file_path)

def cacheWindow(window):
    sub             = tk.Toplevel(window)
    sub.title("Cache Handler")
    sub.geometry("300x350")
    cache_dir = getCacheDir()

    lbl                     = tk.Label(sub, text="Cached Files:", font=("Inter SemiBold", 14))
    lbl.pack(pady=(10, 0))
    
    listbox                 = tk.Listbox(sub, selectmode=tk.SINGLE, width=40, height=8)
    listbox.pack(pady=5)

    def load_list():
        listbox.delete(0, tk.END)
        for filename in os.listdir(cache_dir):
            if filename.endswith(".parquet"):
                run_name      = filename.replace(".parquet", "")
                listbox.insert(tk.END, run_name)

    def delete_selected():
        sel                   = listbox.curselection()
        if not sel:
            messagebox.showinfo("No Selection", "Please select a run to delete.")
            return
        run_name              = listbox.get(sel[0])
        if deleteCache(run_name):
            messagebox.showinfo("Deleted", f"Cache for '{run_name}' removed.")
        else:
            messagebox.showwarning("Not Found", f"No cache found for '{run_name}'.")
        load_list()

    def clear_all():
        if messagebox.askyesno("Confirm", "Delete ALL cached runs?"):
            deleteCacheAll()
            load_list()

    btn_frame                   = tk.Frame(sub)
    btn_frame.pack(pady=10)
    
    del_btn                     = tk.Button(btn_frame, text="Delete Selected", command=delete_selected)
    del_btn.grid(row=0, column=0, padx=5)
    
    clear_btn                   = tk.Button(btn_frame, text="Clear All", command=clear_all)
    clear_btn.grid(row=0, column=1, padx=5)
    
    close_btn                   = tk.Button(sub, text="Close", command=sub.destroy)
    close_btn.pack(pady=(0,10))

    load_list()

# --------------------------------------------------------------------------

# Build Starting Window
window_start                    = Tk()
frame_1                         = build_gui.buildFrame(window_start)
build_gui.folderPath            = ''
sections                        = {}

window_start.geometry("800x600")
window_start.configure(bg="#FFFFFF")
window_start.resizable(False, False)
frame_1.pack(fill="both", expand=True)
build_gui.frameFill_START(frame_1)

window_start.title("Welcome!")
window_start.mainloop()

# Build Main Window (after RUN selection)
window_main                     = Tk()
frame_2                         = build_gui.buildFrame(window_main)

window_main.geometry("1080x740")
window_main.configure(bg="#FFFFFF")
frame_2.pack(fill="both", expand=True)
build_gui.frameFill_PRIMARY(frame_2)

# Setup RUN Select functionality
def runSelect(*args):
    global df
    global sections
    build_gui.unselectAll()

    run_name                       = frame_2.dropdown_var.get()
    df                             = loadDataframe(run_name)

    if df is not None:
        classes                     = parser.extractClasses(build_gui.folderPath, run_name)
        sections                    = parser.extractSections(build_gui.folderPath, classes)
    else:
        classes                     = parser.extractClasses(build_gui.folderPath, frame_2.dropdown_var.get())
        sections                    = parser.extractSections(build_gui.folderPath, classes)
        df                          = parser.createDataFrame(build_gui.folderPath, sections)
        cacheDataFrame(df, run_name)

    build_gui.showGroups(frame_2.image_frame, sections)
    build_gui.showDataframe(frame_2, df)
    frame_2.dropdown_var_2.set("Action")
    frame_2.dropdown_var_3.set("Advanced")
    build_gui.current.clear()
    build_gui.shakeFrame(frame_2)

# Setup GPA Calculator functionality
def runGPACalc():
    build_gui.ticked_courses    = []
    build_gui.ticked_sections   = {}
    selected_count = sum(var.get() for course in build_gui.section_vars for var in build_gui.section_vars[course])
    if selected_count == 0:
        messagebox.showinfo("Stop!", "Please Select One of the Sections for this Action")
        return
    build_gui.checkTicked(sections)
    gpa_df                      = gpa_calculator.calcGPA(df, build_gui.ticked_sections)
    fig                         = gpa_calculator.createGPAGraph(gpa_df)
    build_gui.showDataframe(frame_2, gpa_df)
    build_gui.current.clear()
    build_gui.current.append(fig)
    build_gui.shakeFrame(frame_2)

# Setup Student List functionality
def runStudentList():
    good_grades                 = {"A", "A-"}
    work_grades                 = {"D+", "D", "D-", "F"}
    current_run                 = frame_2.dropdown_var.get()
    build_gui.ticked_courses    = []
    build_gui.ticked_sections   = {}
    cache_dir                   = getCacheDir()
    cache_runs                  = []
    selected_count = sum(var.get() for course in build_gui.section_vars for var in build_gui.section_vars[course])
    if selected_count == 0:
            messagebox.showinfo("Stop!", "Please Select One of the Sections for this Action")
            return
    build_gui.checkTicked(sections)
    good_df, work_df            = student_list.classify_students(df, build_gui.ticked_sections)
    concat                      = pd.concat([good_df, work_df], ignore_index=True)
    final                       = student_list.merge_duplicate_students(concat)
    fig                         = student_list.plotStudentCharts(final)

    # Find all the runs in the cache, then check if there are repeated "Good" & "Work" students
    for filename in os.listdir(cache_dir):
        if filename.endswith(".parquet"):
            run_name = filename.replace(".parquet", "")
            cache_runs.append(run_name)

    final["Other Runs"] = ""

    for run_name in cache_runs:
        if run_name == current_run:
            continue

        try:
            cached_df = pd.read_parquet(getCachePath(run_name))
        except Exception as e:
            print(f"Error loading cache for {run_name}: {e}")
            continue

        if not all(col in cached_df.columns for col in ["ID", "Class", "Grade"]):
            continue

        grouped = cached_df.groupby("ID")

        for idx, row in final.iterrows():
            student_id = row.get("ID")
            current_grade = row.get("Grade")
            current_class = row.get("Class")

            if pd.isna(student_id) or pd.isna(current_grade):
                continue

            try:
                student_records = grouped.get_group(student_id)
            except KeyError:
                continue

            match_found = False

            for _, cached_row in student_records.iterrows():
                cached_grade = cached_row.get("Grade")
                cached_class = cached_row.get("Class")

            if (
                current_grade in good_grades and cached_grade in good_grades
            ) or (
                current_grade in work_grades and cached_grade in work_grades
            ):
                if pd.notna(cached_class):
                    existing_classes = set(str(current_class).split(", "))
                    if cached_class not in existing_classes:
                        combined = existing_classes | {cached_class}
                        final.at[idx, "Class"] = ", ".join(sorted(combined))
                        match_found = True

            if match_found:
                existing = final.at[idx, "Other Runs"]
                updated = f"{existing}, {run_name}" if existing else run_name
                final.at[idx, "Other Runs"] = ", ".join(sorted(set(updated.split(", "))))

    build_gui.showDataframe(frame_2, final)
    build_gui.shakeFrame(frame_2)
    build_gui.current.clear()
    build_gui.current.append(fig)

# Setup Z-Test functionality
def runZTest():
    build_gui.ticked_courses    = []
    build_gui.ticked_sections   = {}
    selected_count = sum(var.get() for course in build_gui.section_vars for var in build_gui.section_vars[course])
    if selected_count == 0:
        messagebox.showinfo("Stop!", "Please Select One of the Sections for this Action")
        return
    build_gui.checkTicked(sections)
    gpa_df                      = gpa_calculator.calcGPA(df, build_gui.ticked_sections)
    z_df                        = significance_test.calculateZScores(df, build_gui.ticked_sections, gpa_df)
    fig                         = significance_test.createZScoreGraph(z_df)
    build_gui.showDataframe(frame_2, z_df)
    build_gui.current.clear()
    build_gui.current.append(fig)
    build_gui.shakeFrame(frame_2)

# Setup Distribution functionality
def runDistribution():
    build_gui.ticked_courses    = []
    build_gui.ticked_sections   = {}
    selected_count              = sum(var.get() for course in build_gui.section_vars for var in build_gui.section_vars[course])
    if selected_count == 0:
        messagebox.showinfo("Stop!", "Please Select One of the Sections for this Action")
        return
    build_gui.checkTicked(sections)
    dist_df                     = gpa_calculator.calcGradeDistribution(df, build_gui.ticked_sections)
    fig                         = gpa_calculator.createGradeDistributionGraph(dist_df)
    build_gui.showDataframe(frame_2, dist_df)
    build_gui.current.clear()
    build_gui.current.append(fig)
    build_gui.shakeFrame(frame_2)
    
# Set functionalities into single function
def runAction(*args):
    if   frame_2.dropdown_var_2.get() == "Z-Test":
        runZTest()
    elif frame_2.dropdown_var_2.get() == "Display-GPA":
        runGPACalc()
    elif frame_2.dropdown_var_2.get() == "Student-List":
        runStudentList()
    elif frame_2.dropdown_var_2.get() == "Distribution":
        runDistribution()

# Set advanced functionalities into single function
def runAdvanced(*args):
    if  frame_2.dropdown_var_3.get() == "View Graph":
        frame_2.dropdown_var_3.set("Advanced")
        build_gui.openGraphWindow(window_main)
    if  frame_2.dropdown_var_3.get() ==  "Manage History":
        cacheWindow(window_main)
        frame_2.dropdown_var_3.set("Advanced")

# Set RUN functionality into RUN Dropdown
frame_2.dropdown_var.trace("w", runSelect)

# Set ACTION functionality into ACTIONS dropdown
frame_2.dropdown_var_2.trace("w", runAction)

# Set ADVANCED functionality into ADVANCED dropdown
frame_2.dropdown_var_3.trace("w", runAdvanced)

# Condition to move to main window
if build_gui.state["state"] == True: 
    window_main.title("GPA Analyzer")
    window_main.mainloop()
