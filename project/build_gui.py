#----------------------------build_gui.py---------------------------
#
# Formulates Tkinter frames and windows
# Front end for software
# @Author: Peter Nolan
#
#--------------------------------------------------------------------
import tkinter as tk
from tkinter import filedialog, Frame, Tk, Canvas, Button, PhotoImage, StringVar, OptionMenu, ttk, messagebox
import sys, os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict

# Get absolute path to resource with Pyinstaller
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller sets this
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Variables:
assetPath                   = resource_path('project/assets')
runList                     = []
state                       = {"state": False}

course_vars                 = {}                    # Store main course checkboxes' states
section_vars                = defaultdict(list)     # Store section checkboxes' states

ticked_courses              = []
ticked_sections             = {}
current                     = []

# Save Data Frame
def downloadDataFrame(df):
    global folderPath
    filename = "dataframe.csv"

    # Join directory path with filename
    full_filename            = os.path.join(folderPath, filename)

    # Check if the file already exists
    base_filename, extension = os.path.splitext(full_filename)
    counter                  = 1
    new_filename             = full_filename

    while os.path.exists(new_filename):
        new_filename         = f"{base_filename}({counter}){extension}"
        counter              += 1

    # Save the dataframe as a CSV
    df.to_csv(new_filename, index=False)
    messagebox.showinfo("Save Successful", f"DataFrame has been saved as {new_filename}")

# Open folder to select working directory
def openFolder(frame):
    global folderPath
    folderPath               = filedialog.askdirectory()
    if folderPath:
        frame.canvas.itemconfig(frame.selected_path, text=f"Selected Path: {folderPath}")   # config text
        frame.button_2.place(x=329.0, y=486.0, width=122.0, height=44.0)                    # for button_2

# Close Starting Window
def closeWindow(window):
    if any(file.endswith('.RUN') for file in os.listdir(folderPath)):
        window.destroy()
        state["state"]       = True
    else:
        messagebox.showinfo("Stop!", "No RUN Files Detected... Please Select Another Directory")

# Show Data Frame in frame (using tree view)
def showDataframe(frame, df):

    clearFrame(frame.frame_child)
    container                   = tk.Frame(frame.frame_child)
    container.pack(fill="both", expand=True)

    tree                        = ttk.Treeview(container, columns=list(df.columns), show="headings")

    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center", stretch=tk.YES)

    for index, row in df.iterrows():
        tree.insert("", "end", values=list(row))

    tree.pack(fill="both", expand=True, side="left")

    hsb                         = tk.Scrollbar(frame.frame_child, orient="horizontal", command=tree.xview)
    tree.configure(xscrollcommand=hsb.set)

    vsb                         = tk.Scrollbar(container, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)

    vsb.place(relx=0.97, rely=0, relwidth=0.03, relheight=1.0)
    hsb.place(x=0, rely=1.0, relwidth=1.0, anchor="sw")

    frame.button_4.config(command=lambda: downloadDataFrame(df))

# Search for RUN files
def searchPath(dir, runList):
    try:
        files = os.listdir(dir)
        for file in files:
            if file.endswith('.RUN'):
                runList.append(file)
    except FileNotFoundError:
        print(f"Error: The directory '{dir}' was not found.")
    except PermissionError:
        print(f"Error: Permission denied to access the directory '{dir}'.")
    return runList

# Build a frame in a window
def buildFrame(window):
    frame = Frame(window, bg="#FFFFFF")
    return frame

# Clear all widgets in a frame
def clearFrame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

# Handles Starting Frame Fill
def frameFill_START(frame):
    global runList
    # Fill frame with canvas
    frame.canvas = Canvas(
        frame,
        bg="#FFFFFF",
        height=600,
        width=800,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    frame.canvas.place(x=0, y=0)
    frame.canvas.create_rectangle(
        0.0, 0.0, 819.0, 111.0, fill="#D9D9D9", outline=""
    )

    # Fill canvas with text
    frame.canvas.create_text(
        21.0, 21.0, anchor="nw", text="Welcome to GPA Analyzer!",
        fill="#000000", font=("Inter SemiBold", 33 * -1)
    )

    frame.canvas.create_text(
        35.0, 65.0, anchor="nw",
        text="Provided by MEEP Software Solutions™",
        fill="#000000", font=("Inter SemiBoldItalic", 10 * -1)
    )

    frame.canvas.create_text(
        224.0, 150.0, anchor="nw", text="Please Select a Folder",
        fill="#000000", font=("Inter SemiBold", 30 * -1)
    )

    # Set a text to file path
    frame.selected_path = frame.canvas.create_text(
        225.0, 290.0, anchor="nw", text="Selected Path: ...",
        fill="#817D7D", font=("Inter SemiBoldItalic", 10 * -1)
    )

    frame.canvas.create_text(
        305.0, 188.0, anchor="nw",
        text="(all files should be in a single folder)",
        fill="#000000", font=("Inter SemiBold", 10 * -1)
    )

    # BUTTON 1 (handles folder path selection)
    frame.button_image_1 = PhotoImage(file=os.path.join(assetPath, 'button_1.png'))
    frame.button_1 = Button(
        frame, image=frame.button_image_1, borderwidth=0, highlightthickness=0,
        bg="#FFFFFF", command= lambda: openFolder(frame), relief="flat"
    )
    frame.button_1.place(x=304.0, y=218.0, width=179.0, height=67.0)

    # BUTTON 2 (handles transition to primary frame)
    frame.button_image_2 = PhotoImage(file=os.path.join(assetPath, 'button_2.png'))
    frame.button_2 = Button(
        frame, image=frame.button_image_2, borderwidth=0, highlightthickness=0,
        bg="#FFFFFF", command= lambda: (searchPath(folderPath, runList), closeWindow(frame.winfo_toplevel())), relief="flat"
    )

# Handles Primary Frame Fill
def frameFill_PRIMARY(frame):
    global runList

    # Fill frame with canvas
    frame.canvas = Canvas(
        frame, bg="#FFFFFF", height=1080, width=1920, bd=0,
        highlightthickness=0, relief="ridge", scrollregion=(0, 0, 2000, 1080) # Make canvas scrollable
    )

    frame.canvas.place(x=0, y=0)

    frame.canvas.create_rectangle(
        0.0, 0.0, 20000.0, 111.0, fill="#D9D9D9", outline=""
    )

    # Fill canvas with text
    frame.canvas.create_text(
        21.0, 21.0, anchor="nw", text="GPA Analyzer",
        fill="#000000", font=("Inter SemiBold", 33 * -1)
    )

    frame.canvas.create_text(
        35.0, 65.0, anchor="nw",
        text="Provided by MEEP Software Solutions™",
        fill="#000000", font=("Inter SemiBoldItalic", 10 * -1)
    )

    frame.canvas.create_text(
        24.0, 129.0, anchor="nw", text="Select RUN File",
        fill="#000000", font=("Inter SemiBold", 30 * -1)
    )

    frame.dropdown_var = StringVar()
    frame.dropdown_var.set("Options")

    if runList:
        frame.dropdown_menu = OptionMenu(
            frame.canvas,  # Place on the canvas
            frame.dropdown_var,
            *runList
        )

        frame.dropdown_menu.config(
            font=("Arial", 12),
            bg="#F0F0F0",
            fg="#333333",
            activebackground="#545454",
            activeforeground="white",
            relief="flat",
            highlightthickness=0,
            bd=2,
            width=10
        )

        frame.canvas.create_window(30.0, 180.0, window=frame.dropdown_menu, anchor="nw") # Place using create_window

    frame.dropdown_var_2 = StringVar()
    frame.dropdown_var_2.set("Action")

    options = ["Display-GPA", "Z-Test", "Student-List", "Distribution"]
    frame.dropdown_menu_2 = OptionMenu(
        frame.canvas, 
        frame.dropdown_var_2,
        *options
    )

    frame.dropdown_menu_2.config(
        font=("Arial", 8),
        bg="#F0F0F0",
        fg="#333333",
        activebackground="#545454",
        activeforeground="white",
        relief="flat",
        highlightthickness=0,
        bd=2,
        width=10
    )

    frame.canvas.create_window(910.0, 70.0, window=frame.dropdown_menu_2, anchor="nw") # Place using create_window

    frame.dropdown_var_3 = StringVar()
    frame.dropdown_var_3.set("Advanced")

    advanced_options = ["View Graph", "Manage History"]
    frame.dropdown_menu_3 = OptionMenu(
        frame.canvas, 
        frame.dropdown_var_3,
        *advanced_options
    )

    frame.dropdown_menu_3.config(
        font=("Arial", 8),
        bg="#F0F0F0",
        fg="#333333",
        activebackground="#545454",
        activeforeground="white",
        relief="flat",
        highlightthickness=0,
        bd=2,
        width=8
    )

    frame.canvas.create_window(910.0, 20.0, window=frame.dropdown_menu_3, anchor="nw") 


    frame.image_ref     = PhotoImage(file=os.path.join(assetPath, 'image_1.png'))
    frame.canvas.create_image(252.0, 450.0, image=frame.image_ref)

    frame.image_frame   = tk.Frame(frame.canvas, width=440, height=430, bg="#D9D9D9")
    frame.canvas.create_window(32.0, 235.0, window=frame.image_frame, anchor="nw")

    frame.frame_child   = tk.Frame(frame.canvas, bg="#D9D9D9", width=500, height=540)
    frame.frame_child.propagate(False)
    frame.canvas.create_window(550.0, 135.0, window=frame.frame_child, anchor="nw")

    # BUTTON 4 (handles dataframe download)
    frame.button_image_4 = PhotoImage(file=os.path.join(assetPath, 'button_4.png'))
    frame.button_4 = Button(
        frame.canvas, image=frame.button_image_4, borderwidth=0, highlightthickness=0,
        bg="#FFFFFF", command= None, relief="flat"
    )

    frame.canvas.create_window(450 + 500 - frame.button_4.winfo_width(), 130 + 540 + 10, window=frame.button_4, anchor="nw")

# Show Groups in frame from RUN file
def showGroups(frame, sections):
    frame.config(bg="#D9D9D9")

    clearFrame(frame)

    style       = ttk.Style()
    style.configure("TCheckbutton", font=("Arial", 13), background="#D9D9D9")
    style.configure("TCheckbutton", indicatorbackground="#D9D9D9", indicatorforeground="#D9D9D9")
    style.configure("Vertical.TScrollbar", troughcolor="#D9D9D9", background="#D9D9D9", arrowcolor="#D9D9D9")

    def toggle_sections(course):
        state   = course_vars[course].get()
        for var in section_vars[course]:
            var.set(state)

    def update_course_checkbox(course):
        if any(var.get() for var in section_vars[course]):
            course_vars[course].set(1)
        else:
            course_vars[course].set(0)

    # Create a Canvas widget and a vertical Scrollbar
    canvas      = tk.Canvas(frame, height=430, width=420, bg="#D9D9D9", highlightthickness=0)
    scrollbar   = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)

    scrollbar.pack(side="right", fill="y", pady=5)
    canvas.pack(side="left", fill="both", expand=True)

    container   = tk.Frame(canvas, bg="#D9D9D9")

    canvas.create_window((0, 0), window=container, anchor="nw")

    def on_frame_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"), bg="#D9D9D9")

    container.bind("<Configure>", on_frame_configure)

    for course, section_list in sections.items():
        course_vars[course] = tk.IntVar()
        section_vars[course] = []

        course_chk = ttk.Checkbutton(
            container, text=course, variable=course_vars[course],
            command=lambda c=course: toggle_sections(c)
        )
        course_chk.pack(anchor="w", pady=2)

        # Section-level checkboxes
        for section in section_list:
            # Remove the ".sec" suffix from the section name
            section_name = section.removesuffix(".sec")

            section_var = tk.IntVar()
            section_vars[course].append(section_var)

            def make_callback(c=course, v=section_var):
                def callback():
                    update_course_checkbox(c)
                return callback

            section_chk = ttk.Checkbutton(
                container, text=section_name, variable=section_var,
                command=make_callback()
            )
            section_chk.pack(anchor="w", padx=20)

    canvas.configure(yscrollcommand=scrollbar.set)

def unselectAll():
    for course in course_vars:
        course_vars[course].set(0)
        for var in section_vars[course]:
            var.set(0)

def checkTicked(section_dict):
    for course, var in course_vars.items():
        if var.get() == 1:  # If the course is ticked
            ticked_courses.append(course)
            ticked_sections[course] = [] 
            if course in section_dict:
                for i, section_name in enumerate(section_dict[course]):
                    section_var = section_vars.get(course, [])[i]
                    if section_var and section_var.get() == 1:
                        ticked_sections[course].append(section_name[:-4])


# Shake animation for Data Frame
def shakeFrame(frame, intensity=5, duration=300):
    canvas          = frame.canvas
    widget          = frame.frame_child
    original_x      = 550
    original_y      = 135

    if not hasattr(frame, "window_id"):
        frame.window_id = canvas.create_window(original_x, original_y, window=widget, anchor="nw")

    window_id       = frame.window_id

    shake_interval  = 50
    shakes          = duration // shake_interval
    directions      = [intensity, -intensity] * (shakes // 2)

    def shake(index=0):
        if index < len(directions):
            dx = directions[index]
            canvas.coords(window_id, original_x + dx, original_y)
            canvas.after(shake_interval, shake, index + 1)
        else:
            canvas.coords(window_id, original_x, original_y)  # Just reset position

    shake()

# Show Graph in a frame
def showGraph(frame, fig):
    clearFrame(frame)
    fig_canvas      = FigureCanvasTkAgg(fig, master=frame)
    fig_widget      = fig_canvas.get_tk_widget()
    fig_widget.pack(fill="both", expand=True)
    fig_canvas.draw()

def openGraphWindow(window):
    if current:
        sub = tk.Toplevel(window)
        sub.iconbitmap(file=os.path.join(assetPath, 'logo.jpg'))
        sub.title("View Graph")
        sub.geometry("1080x700")

        graph_frame   = tk.Frame(sub, bg="#D9D9D9", width= 1020, height= 600)
        graph_frame.place(relx=0.5, rely=0.5, anchor="center")
        showGraph(graph_frame, current[0])
    else:
        messagebox.showinfo("Stop!", "Please Select an Action")


