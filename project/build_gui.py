import tkinter as tk
from tkinter import filedialog, Frame, Tk, Canvas, Button, PhotoImage, StringVar, OptionMenu
import os

assetPath   = 'project\\assets'
folderPath  = ''
runList     = []

def openFolder(frame):
    global folderPath
    folderPath = filedialog.askdirectory()
    if folderPath:
        frame.canvas.itemconfig(frame.selected_path, text=f"Selected Path: {folderPath}")   # config text
        frame.button_2.place(x=329.0, y=486.0, width=122.0, height=44.0)                    # for button_2

def closeWindow(window):
    window.destroy()

# Search directory for RUN files
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

def buildFrame(window):
    frame = Frame(window, bg="#FFFFFF")
    return frame

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
    frame.button_image_1 = PhotoImage(file=assetPath + '\\button_1.png')
    frame.button_1 = Button(
        frame, image=frame.button_image_1, borderwidth=0, highlightthickness=0,
        bg="#FFFFFF", command= lambda: openFolder(frame), relief="flat"
    )
    frame.button_1.place(x=304.0, y=218.0, width=179.0, height=67.0)

    # BUTTON 2 (handles transition to primary frame)
    frame.button_image_2 = PhotoImage(file=assetPath + '\\button_2.png')
    frame.button_2 = Button(
        frame, image=frame.button_image_2, borderwidth=0, highlightthickness=0,
        bg="#FFFFFF", command= lambda: (searchPath(folderPath, runList), closeWindow(frame.winfo_toplevel())), relief="flat"
    )

def frameFill_PRIMARY(frame):
    global runList
    
    # Fill frame with canvas
    frame.canvas = Canvas(
        frame, bg="#FFFFFF", height=1080, width=1920, bd=0,
        highlightthickness=0, relief="ridge"
    )

    frame.canvas.place(x=0, y=0)
    frame.canvas.create_rectangle(
        0.0, 0.0, 2000.0, 111.0, fill="#D9D9D9", outline=""
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

    dropdown_var = StringVar()
    dropdown_var.set("Options")

    if runList:
        dropdown_menu = OptionMenu(
            frame,
            dropdown_var,
            *runList
        )

        dropdown_menu.config(
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
        
        dropdown_menu.place(x=30.0, y=180.0)

    dropdown_var_2 = StringVar()
    dropdown_var_2.set("Action")

    options = ["Option 1", "Option 2", "Option 3", "Option 4"]
    dropdown_menu = OptionMenu(
        frame, 
        dropdown_var_2,
        *options
    )

    dropdown_menu.config(
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

    dropdown_menu.place(x=910.0, y=70.0)

def frameSet_GROUPS(frame):

    frame.image_ref = PhotoImage(file=assetPath + '\\image_1.png')
    frame.canvas.create_image(252.0, 450.0, image=frame.image_ref)

    frame_child = tk.Frame(frame, bg ="#D9D9D9", width=500, height=540)
    frame_child.place(x=550, y=135)