import tkinter as tk
from tkinter import filedialog, Frame, Tk, Canvas, Button, PhotoImage
import os

assetPath   = 'project\\assets'
states      = []
stateIndex  = 0
folderPath  = ''

def openFolder(frame):
    global folderPath
    folderPath = filedialog.askdirectory()
    if folderPath:
        frame.canvas.itemconfig(frame.selected_path, text=f"Selected Path: {folderPath}")   # config text
        frame.button_2.place(x=329.0, y=486.0, width=122.0, height=44.0)                    # for button_2

def nextFrame():
    global stateIndex
    states[stateIndex].pack_forget()
    stateIndex += 1
    states[stateIndex].pack(fill="both", expand=True)

# Search directory for RUN files
def searchPath(dir, runList):
    for roots, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith('.RUN'):
                runList.append(file)
    return runList


def buildFrame(window):
    frame = Frame(window, bg="#FFFFFF")
    return frame

def frameFill_START(frame, runList):

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
        21.0, 21.0, anchor="nw", text="Welcome to GPA Analyzer",
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
        bg="#FFFFFF", command= lambda: (searchPath(folderPath, runList), nextFrame()), relief="flat"
    )

def frameFill_PRIMARY(frame, runList):

    # Fill frame with canvas
    frame.canvas = Canvas(
        frame, bg="#FFFFFF", height=600, width=800, bd=0,
        highlightthickness=0, relief="ridge"
    )

    frame.canvas.place(x=0, y=0)
    frame.canvas.create_rectangle(
        0.0, 0.0, 819.0, 111.0, fill="#D9D9D9", outline=""
    )

    # Fill canvas with text
    frame.canvas.create_text(
        21.0, 21.0, anchor="nw", text="Welcome to GPA Analyzer",
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


